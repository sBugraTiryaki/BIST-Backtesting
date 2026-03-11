import numpy as np
import pandas as pd

from app.strategies.base import BaseStrategy


class EMACrossover(BaseStrategy):
    def generate_signals(self, df: pd.DataFrame, **params) -> pd.DataFrame:
        short_period = int(params.get("kisa_periyot", 12))
        long_period = int(params.get("uzun_periyot", 26))

        df = df.copy()
        df["ema_short"] = df["Close"].ewm(span=short_period, adjust=False).mean()
        df["ema_long"] = df["Close"].ewm(span=long_period, adjust=False).mean()

        df["signal"] = 0
        cross_up = (df["ema_short"] > df["ema_long"]) & (
            df["ema_short"].shift(1) <= df["ema_long"].shift(1)
        )
        cross_down = (df["ema_short"] < df["ema_long"]) & (
            df["ema_short"].shift(1) >= df["ema_long"].shift(1)
        )

        df.loc[cross_up, "signal"] = 1
        df.loc[cross_down, "signal"] = -1

        return df

    def get_indicator_data(self, df: pd.DataFrame, **params) -> list[dict]:
        short_period = int(params.get("kisa_periyot", 12))
        long_period = int(params.get("uzun_periyot", 26))

        ema_short = df["Close"].ewm(span=short_period, adjust=False).mean()
        ema_long = df["Close"].ewm(span=long_period, adjust=False).mean()

        return [
            {
                "name": f"EMA {short_period}",
                "values": [
                    {"date": str(date.date()), "value": round(val, 2)}
                    for date, val in ema_short.dropna().items()
                ],
            },
            {
                "name": f"EMA {long_period}",
                "values": [
                    {"date": str(date.date()), "value": round(val, 2)}
                    for date, val in ema_long.dropna().items()
                ],
            },
        ]
