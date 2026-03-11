import numpy as np
import pandas as pd

from app.strategies.base import BaseStrategy


class BollingerBands(BaseStrategy):
    def generate_signals(self, df: pd.DataFrame, **params) -> pd.DataFrame:
        period = int(params.get("periyot", 20))
        std_mult = float(params.get("std_carpani", 2.0))

        df = df.copy()
        df["bb_middle"] = df["Close"].rolling(window=period).mean()
        bb_std = df["Close"].rolling(window=period).std()
        df["bb_upper"] = df["bb_middle"] + std_mult * bb_std
        df["bb_lower"] = df["bb_middle"] - std_mult * bb_std

        df["signal"] = 0
        # Fiyat alt bandın altına düşüp geri çıkarsa -> AL
        cross_up = (df["Close"] > df["bb_lower"]) & (
            df["Close"].shift(1) <= df["bb_lower"].shift(1)
        )
        # Fiyat üst bandın üstüne çıkıp geri düşerse -> SAT
        cross_down = (df["Close"] < df["bb_upper"]) & (
            df["Close"].shift(1) >= df["bb_upper"].shift(1)
        )

        df.loc[cross_up, "signal"] = 1
        df.loc[cross_down, "signal"] = -1

        return df

    def get_indicator_data(self, df: pd.DataFrame, **params) -> list[dict]:
        period = int(params.get("periyot", 20))
        std_mult = float(params.get("std_carpani", 2.0))

        middle = df["Close"].rolling(window=period).mean()
        bb_std = df["Close"].rolling(window=period).std()
        upper = middle + std_mult * bb_std
        lower = middle - std_mult * bb_std

        return [
            {
                "name": f"BB Üst ({period})",
                "values": [
                    {"date": str(date.date()), "value": round(val, 2)}
                    for date, val in upper.dropna().items()
                ],
            },
            {
                "name": f"BB Orta ({period})",
                "values": [
                    {"date": str(date.date()), "value": round(val, 2)}
                    for date, val in middle.dropna().items()
                ],
            },
            {
                "name": f"BB Alt ({period})",
                "values": [
                    {"date": str(date.date()), "value": round(val, 2)}
                    for date, val in lower.dropna().items()
                ],
            },
        ]
