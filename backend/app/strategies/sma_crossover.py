import numpy as np
import pandas as pd

from app.strategies.base import BaseStrategy


class SMACrossover(BaseStrategy):
    def generate_signals(self, df: pd.DataFrame, **params) -> pd.DataFrame:
        short_period = int(params.get("kisa_periyot", 20))
        long_period = int(params.get("uzun_periyot", 50))

        df = df.copy()
        df["sma_short"] = df["Close"].rolling(window=short_period).mean()
        df["sma_long"] = df["Close"].rolling(window=long_period).mean()

        df["signal"] = 0
        # Kısa SMA uzun SMA'yı yukarı keserse -> AL
        cross_up = (df["sma_short"] > df["sma_long"]) & (
            df["sma_short"].shift(1) <= df["sma_long"].shift(1)
        )
        # Kısa SMA uzun SMA'yı aşağı keserse -> SAT
        cross_down = (df["sma_short"] < df["sma_long"]) & (
            df["sma_short"].shift(1) >= df["sma_long"].shift(1)
        )

        df.loc[cross_up, "signal"] = 1
        df.loc[cross_down, "signal"] = -1

        return df

    def get_indicator_data(self, df: pd.DataFrame, **params) -> list[dict]:
        short_period = int(params.get("kisa_periyot", 20))
        long_period = int(params.get("uzun_periyot", 50))

        sma_short = df["Close"].rolling(window=short_period).mean()
        sma_long = df["Close"].rolling(window=long_period).mean()

        return [
            {
                "name": f"SMA {short_period}",
                "values": [
                    {"date": str(date.date()), "value": round(val, 2)}
                    for date, val in sma_short.dropna().items()
                ],
            },
            {
                "name": f"SMA {long_period}",
                "values": [
                    {"date": str(date.date()), "value": round(val, 2)}
                    for date, val in sma_long.dropna().items()
                ],
            },
        ]
