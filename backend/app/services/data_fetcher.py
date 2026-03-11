import json
import time
from pathlib import Path

import numpy as np
import pandas as pd
import requests
import yfinance as yf

from app.config import BIST100, CACHE_DIR, CACHE_TTL_SECONDS

ISYATIRIM_URL = (
    "https://www.isyatirim.com.tr/_layouts/15/"
    "Isyatirim.Website/Common/Data.aspx/HisseTekil"
)


def _get_yahoo_symbol(symbol: str) -> str:
    for stock in BIST100:
        if stock["symbol"] == symbol.upper():
            return stock["yahoo_symbol"]
    return f"{symbol.upper()}.IS"


def _get_bist_symbol(yahoo_symbol: str) -> str:
    """THYAO.IS -> THYAO"""
    return yahoo_symbol.replace(".IS", "")


def _cache_path(symbol: str, start: str, end: str) -> Path:
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    return CACHE_DIR / f"{symbol}_{start}_{end}.json"


def _is_cache_valid(path: Path) -> bool:
    if not path.exists():
        return False
    age = time.time() - path.stat().st_mtime
    return age < CACHE_TTL_SECONDS


def _fetch_isyatirim_adjusted(symbol: str, start: str, end: str) -> pd.Series | None:
    """İş Yatırım'dan split-adjusted kapanış fiyatlarını çek.

    Returns: DatetimeIndex'li Series (HG_KAPANIS) veya None (hata durumunda).
    """
    try:
        # YYYY-MM-DD -> DD-MM-YYYY
        s = pd.Timestamp(start)
        e = pd.Timestamp(end)
        params = {
            "hisse": symbol,
            "startdate": s.strftime("%d-%m-%Y"),
            "enddate": e.strftime("%d-%m-%Y"),
        }
        resp = requests.get(ISYATIRIM_URL, params=params, timeout=15)
        resp.raise_for_status()
        data = resp.json()

        rows = data.get("value", [])
        if not rows:
            return None

        records = []
        for row in rows:
            date_str = row["HGDG_TARIH"]
            hgdg_close = row.get("HGDG_KAPANIS")
            if hgdg_close is not None:
                records.append({"Date": pd.to_datetime(date_str, dayfirst=True), "Adj_Close": float(hgdg_close)})

        if not records:
            return None

        ref = pd.DataFrame(records).set_index("Date").sort_index()
        return ref["Adj_Close"]
    except Exception:
        return None


def _adjust_with_isyatirim(df: pd.DataFrame, yahoo_symbol: str, start: str, end: str) -> pd.DataFrame:
    """İş Yatırım HGDG_KAPANIS referansıyla yfinance split hatalarını düzelt.

    HGDG_KAPANIS split-düzeltmeli sürekli seridir.
    yfinance Close / HGDG Close oranı ~1.0'dan farklıysa split düzeltme hatası vardır.
    Pre-split günlerdeki tüm OHLC fiyatlar bu oranla bölünerek düzeltilir.
    """
    bist_symbol = _get_bist_symbol(yahoo_symbol)
    ref = _fetch_isyatirim_adjusted(bist_symbol, start, end)

    if ref is None or ref.empty:
        return df

    # Timezone'ları temizle
    if df.index.tz is not None:
        df.index = df.index.tz_localize(None)
    if ref.index.tz is not None:
        ref.index = ref.index.tz_localize(None)

    # Ortak tarihleri bul
    common_dates = df.index.intersection(ref.index)
    if common_dates.empty:
        return df

    # yfinance Close / İş Yatırım HGDG Close
    # Doğru günlerde ~1.0, split hatası olan günlerde >1.0 (yfinance fazla yüksek)
    ratios = df.loc[common_dates, "Close"] / ref[common_dates]

    # Tolerans: %5
    wrong_mask = (ratios - 1.0).abs() > 0.05
    if not wrong_mask.any():
        return df

    wrong_dates = wrong_mask[wrong_mask].index
    correct_dates = wrong_mask[~wrong_mask].index

    if wrong_dates.empty or correct_dates.empty:
        return df

    # Split oranı: yfinance pre-split günlerde kaç kat fazla gösteriyor
    split_ratio = ratios[wrong_dates].median()

    # Split noktası: son hatalı günün ertesi
    last_wrong = wrong_dates[-1]
    split_day_candidates = correct_dates[correct_dates > last_wrong]
    if split_day_candidates.empty:
        return df
    split_day = split_day_candidates[0]

    # Pre-split günleri düzelt: orana böl
    mask = df.index < split_day
    df.loc[mask, ["Open", "High", "Low", "Close"]] /= split_ratio
    df.loc[mask, "Volume"] = (df.loc[mask, "Volume"] * split_ratio).astype(np.int64)

    return df


def fetch_price_data(symbol: str, start_date: str, end_date: str) -> pd.DataFrame:
    yahoo_symbol = _get_yahoo_symbol(symbol)
    cache_file = _cache_path(symbol, start_date, end_date)

    if _is_cache_valid(cache_file):
        with open(cache_file) as f:
            data = json.load(f)
        df = pd.DataFrame(data)
        df["Date"] = pd.to_datetime(df["Date"])
        df = df.set_index("Date")
        return df

    # Retry mekanizması (Yahoo rate limit için)
    last_err = None
    for attempt in range(3):
        try:
            df = yf.download(
                yahoo_symbol,
                start=start_date,
                end=end_date,
                progress=False,
                auto_adjust=True,
            )
            if not df.empty:
                break
        except Exception as e:
            last_err = e
        if attempt < 2:
            time.sleep(2 ** attempt)
    else:
        if df.empty:
            detail = f" ({last_err})" if last_err else ""
            raise ValueError(
                f"{symbol} için veri bulunamadı ({start_date} - {end_date}).{detail} "
                "Yahoo Finance geçici olarak erişilemiyor olabilir, birkaç dakika sonra tekrar deneyin."
            )

    # yfinance MultiIndex fix
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)

    df = df[["Open", "High", "Low", "Close", "Volume"]].copy()
    df.columns = ["Open", "High", "Low", "Close", "Volume"]

    # Split düzeltmesi: İş Yatırım referansıyla
    df = _adjust_with_isyatirim(df, yahoo_symbol, start_date, end_date)

    # Cache'e yaz
    cache_data = df.reset_index().copy()
    cache_data["Date"] = cache_data["Date"].astype(str)
    with open(cache_file, "w") as f:
        json.dump(cache_data.to_dict(orient="records"), f)

    return df
