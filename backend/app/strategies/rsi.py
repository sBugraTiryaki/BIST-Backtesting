import numpy as np
import pandas as pd

from app.strategies.base import BaseStrategy


def compute_rsi(series: pd.Series, period: int = 14) -> pd.Series:
    delta = series.diff()
    gain = delta.where(delta > 0, 0.0)
    loss = (-delta).where(delta < 0, 0.0)

    avg_gain = gain.rolling(window=period).mean()
    avg_loss = loss.rolling(window=period).mean()

    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi


class RSIStrategy(BaseStrategy):
    def generate_signals(self, df: pd.DataFrame, **params) -> pd.DataFrame:
        period = int(params.get("periyot", 14))
        overbought = float(params.get("asiri_alim", 70))
        oversold = float(params.get("asiri_satim", 30))

        df = df.copy()
        df["rsi"] = compute_rsi(df["Close"], period)

        df["signal"] = 0
        # RSI aşırı satımdan yukarı çıkarsa -> AL
        cross_up = (df["rsi"] > oversold) & (df["rsi"].shift(1) <= oversold)
        # RSI aşırı alımdan aşağı düşerse -> SAT
        cross_down = (df["rsi"] < overbought) & (df["rsi"].shift(1) >= overbought)

        df.loc[cross_up, "signal"] = 1
        df.loc[cross_down, "signal"] = -1

        return df

    def get_indicator_data(self, df: pd.DataFrame, **params) -> list[dict]:
        period = int(params.get("periyot", 14))
        overbought = float(params.get("asiri_alim", 70))
        oversold = float(params.get("asiri_satim", 30))
        rsi = compute_rsi(df["Close"], period)

        dates = [str(date.date()) for date in rsi.dropna().index]

        return [
            {
                "name": f"RSI {period}",
                "overlay": False,
                "values": [
                    {"date": str(date.date()), "value": round(val, 2)}
                    for date, val in rsi.dropna().items()
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
