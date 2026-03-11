import numpy as np
import pandas as pd

from app.strategies.base import BaseStrategy


class WilliamsR(BaseStrategy):
    def generate_signals(self, df: pd.DataFrame, **params) -> pd.DataFrame:
        period = int(params.get("periyot", 14))
        overbought = float(params.get("asiri_alim", -20))
        oversold = float(params.get("asiri_satim", -80))

        df = df.copy()
        highest_high = df["High"].rolling(window=period).max()
        lowest_low = df["Low"].rolling(window=period).min()
        df["williams_r"] = -100 * (highest_high - df["Close"]) / (highest_high - lowest_low)

        df["signal"] = 0
        # %R oversold bölgesinden yukarı çıkarsa -> AL
        cross_up = (df["williams_r"] > oversold) & (df["williams_r"].shift(1) <= oversold)
        # %R overbought bölgesinden aşağı düşerse -> SAT
        cross_down = (df["williams_r"] < overbought) & (
            df["williams_r"].shift(1) >= overbought
        )

        df.loc[cross_up, "signal"] = 1
        df.loc[cross_down, "signal"] = -1

        return df

    def get_indicator_data(self, df: pd.DataFrame, **params) -> list[dict]:
        period = int(params.get("periyot", 14))
        overbought = float(params.get("asiri_alim", -20))
        oversold = float(params.get("asiri_satim", -80))

        highest_high = df["High"].rolling(window=period).max()
        lowest_low = df["Low"].rolling(window=period).min()
        williams_r = -100 * (highest_high - df["Close"]) / (highest_high - lowest_low)

        dates = [str(date.date()) for date in williams_r.dropna().index]

        return [
            {
                "name": f"Williams %R ({period})",
                "overlay": False,
                "values": [
                    {"date": str(date.date()), "value": round(val, 2)}
                    for date, val in williams_r.dropna().items()
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
