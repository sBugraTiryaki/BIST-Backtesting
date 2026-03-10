import json
import time
from pathlib import Path

import pandas as pd
import yfinance as yf

from app.config import BIST30, CACHE_DIR, CACHE_TTL_SECONDS


def _get_yahoo_symbol(symbol: str) -> str:
    for stock in BIST30:
        if stock["symbol"] == symbol.upper():
            return stock["yahoo_symbol"]
    raise ValueError(f"Bilinmeyen sembol: {symbol}")


def _cache_path(symbol: str, start: str, end: str) -> Path:
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    return CACHE_DIR / f"{symbol}_{start}_{end}.json"


def _is_cache_valid(path: Path) -> bool:
    if not path.exists():
        return False
    age = time.time() - path.stat().st_mtime
    return age < CACHE_TTL_SECONDS


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
            df = yf.download(yahoo_symbol, start=start_date, end=end_date, progress=False)
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

    # Cache'e yaz
    cache_data = df.reset_index().copy()
    cache_data["Date"] = cache_data["Date"].astype(str)
    with open(cache_file, "w") as f:
        json.dump(cache_data.to_dict(orient="records"), f)

    return df
