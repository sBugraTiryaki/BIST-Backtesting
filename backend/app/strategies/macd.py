import numpy as np
import pandas as pd

from app.strategies.base import BaseStrategy


class MACDStrategy(BaseStrategy):
    def generate_signals(self, df: pd.DataFrame, **params) -> pd.DataFrame:
        fast = int(params.get("hizli", 12))
        slow = int(params.get("yavas", 26))
        signal_period = int(params.get("sinyal", 9))

        df = df.copy()
        ema_fast = df["Close"].ewm(span=fast, adjust=False).mean()
        ema_slow = df["Close"].ewm(span=slow, adjust=False).mean()

        df["macd_line"] = ema_fast - ema_slow
        df["signal_line"] = df["macd_line"].ewm(span=signal_period, adjust=False).mean()
        df["macd_histogram"] = df["macd_line"] - df["signal_line"]

        df["signal"] = 0
        # MACD sinyal cizgisini yukari keserse -> AL
        cross_up = (df["macd_line"] > df["signal_line"]) & (
            df["macd_line"].shift(1) <= df["signal_line"].shift(1)
        )
        # MACD sinyal cizgisini asagi keserse -> SAT
        cross_down = (df["macd_line"] < df["signal_line"]) & (
            df["macd_line"].shift(1) >= df["signal_line"].shift(1)
        )

        df.loc[cross_up, "signal"] = 1
        df.loc[cross_down, "signal"] = -1

        return df

    def get_indicator_data(self, df: pd.DataFrame, **params) -> list[dict]:
        fast = int(params.get("hizli", 12))
        slow = int(params.get("yavas", 26))
        signal_period = int(params.get("sinyal", 9))

        ema_fast = df["Close"].ewm(span=fast, adjust=False).mean()
        ema_slow = df["Close"].ewm(span=slow, adjust=False).mean()
        macd_line = ema_fast - ema_slow
        signal_line = macd_line.ewm(span=signal_period, adjust=False).mean()

        return [
            {
                "name": "MACD",
                "overlay": False,
                "values": [
                    {"date": str(date.date()), "value": round(val, 4)}
                    for date, val in macd_line.dropna().items()
                ],
            },
            {
                "name": "Sinyal",
                "overlay": False,
                "values": [
                    {"date": str(date.date()), "value": round(val, 4)}
                    for date, val in signal_line.dropna().items()
                ],
            },
        ]
