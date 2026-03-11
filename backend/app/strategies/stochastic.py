import numpy as np
import pandas as pd

from app.strategies.base import BaseStrategy


class StochasticOscillator(BaseStrategy):
    def generate_signals(self, df: pd.DataFrame, **params) -> pd.DataFrame:
        k_period = int(params.get("k_periyot", 14))
        d_period = int(params.get("d_periyot", 3))
        overbought = float(params.get("asiri_alim", 80))
        oversold = float(params.get("asiri_satim", 20))

        df = df.copy()
        lowest_low = df["Low"].rolling(window=k_period).min()
        highest_high = df["High"].rolling(window=k_period).max()

        df["stoch_k"] = 100 * (df["Close"] - lowest_low) / (highest_high - lowest_low)
        df["stoch_d"] = df["stoch_k"].rolling(window=d_period).mean()

        df["signal"] = 0
        # %K oversold bölgesinden yukarı çıkarsa ve %K > %D -> AL
        cross_up = (
            (df["stoch_k"] > df["stoch_d"])
            & (df["stoch_k"].shift(1) <= df["stoch_d"].shift(1))
            & (df["stoch_k"] < oversold)
        )
        # %K overbought bölgesinden aşağı düşerse ve %K < %D -> SAT
        cross_down = (
            (df["stoch_k"] < df["stoch_d"])
            & (df["stoch_k"].shift(1) >= df["stoch_d"].shift(1))
            & (df["stoch_k"] > overbought)
        )

        df.loc[cross_up, "signal"] = 1
        df.loc[cross_down, "signal"] = -1

        return df

    def get_indicator_data(self, df: pd.DataFrame, **params) -> list[dict]:
        k_period = int(params.get("k_periyot", 14))
        d_period = int(params.get("d_periyot", 3))
        overbought = float(params.get("asiri_alim", 80))
        oversold = float(params.get("asiri_satim", 20))

        lowest_low = df["Low"].rolling(window=k_period).min()
        highest_high = df["High"].rolling(window=k_period).max()
        stoch_k = 100 * (df["Close"] - lowest_low) / (highest_high - lowest_low)
        stoch_d = stoch_k.rolling(window=d_period).mean()

        dates = [str(date.date()) for date in stoch_k.dropna().index]

        return [
            {
                "name": f"Stochastic %K ({k_period})",
                "overlay": False,
                "values": [
                    {"date": str(date.date()), "value": round(val, 2)}
                    for date, val in stoch_k.dropna().items()
                ],
            },
            {
                "name": f"Stochastic %D ({d_period})",
                "overlay": False,
                "values": [
                    {"date": str(date.date()), "value": round(val, 2)}
                    for date, val in stoch_d.dropna().items()
                ],
            },
            {
                "name": f"Aşırı Alım ({int(overbought)})",
                "overlay": False,
                "values": [{"date": d, "value": overbought} for d in dates],
            },
            {
                "name": f"Aşırı Satım ({int(oversold)})",
                "overlay": False,
                "values": [{"date": d, "value": oversold} for d in dates],
            },
        ]
