import json
import time
from pathlib import Path

import numpy as np
import pandas as pd
import yfinance as yf

from app.config import BIST100, CACHE_DIR, CACHE_TTL_SECONDS


def _get_yahoo_symbol(symbol: str) -> str:
    for stock in BIST100:
        if stock["symbol"] == symbol.upper():
            return stock["yahoo_symbol"]
    # BIST-100 dışı semboller için de .IS suffix ile dene
    return f"{symbol.upper()}.IS"


def _cache_path(symbol: str, start: str, end: str) -> Path:
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    return CACHE_DIR / f"{symbol}_{start}_{end}.json"


def _is_cache_valid(path: Path) -> bool:
    if not path.exists():
        return False
    age = time.time() - path.stat().st_mtime
    return age < CACHE_TTL_SECONDS


def _adjust_for_splits(df: pd.DataFrame, yahoo_symbol: str) -> pd.DataFrame:
    """Yahoo Finance BIST split düzeltmesi yapmayabiliyor. Manuel düzelt."""
    ticker = yf.Ticker(yahoo_symbol)
    splits = ticker.splits
    if splits.empty:
        return df

    daily_ratio = df["Close"] / df["Close"].shift(1)

    for split_date, ratio in splits.items():
        if ratio <= 1:
            continue

        split_dt = split_date.tz_localize(None) if split_date.tzinfo else split_date

        # Sadece veri aralığımızdaki split'leri işle (±30 gün tampon)
        if split_dt < df.index[0] - pd.Timedelta(days=30):
            continue
        if split_dt > df.index[-1] + pd.Timedelta(days=30):
            continue

        # Split noktasında beklenen günlük oran: ~1/ratio (ör. 11:1 split → ~0.09)
        expected = 1.0 / ratio

        # Bildirilen tarih etrafında ±30 gün pencerede ara
        window_start = split_dt - pd.Timedelta(days=30)
        window_end = split_dt + pd.Timedelta(days=30)
        window = daily_ratio[
            (daily_ratio.index >= window_start) & (daily_ratio.index <= window_end)
        ]

        # Beklenen orana yakın günü bul (%30 tolerans)
        candidates = window[
            (window > expected * 0.7) & (window < expected * 1.3)
        ]

        if candidates.empty:
            continue

        actual_split_day = candidates.index[0]
        mask = df.index < actual_split_day
        df.loc[mask, ["Open", "High", "Low", "Close"]] /= ratio
        df.loc[mask, "Volume"] = (df.loc[mask, "Volume"] * ratio).astype(np.int64)

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

    # Stock split düzeltmesi
    df = _adjust_for_splits(df, yahoo_symbol)

    # Cache'e yaz
    cache_data = df.reset_index().copy()
    cache_data["Date"] = cache_data["Date"].astype(str)
    with open(cache_file, "w") as f:
        json.dump(cache_data.to_dict(orient="records"), f)

    return df
