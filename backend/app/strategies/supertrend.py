import numpy as np
import pandas as pd

from app.strategies.base import BaseStrategy


class Supertrend(BaseStrategy):
    def generate_signals(self, df: pd.DataFrame, **params) -> pd.DataFrame:
        atr_period = int(params.get("atr_periyot", 10))
        multiplier = float(params.get("carpan", 3.0))

        df = df.copy()
        supertrend, direction = self._compute_supertrend(df, atr_period, multiplier)
        df["supertrend"] = supertrend
        df["st_direction"] = direction

        df["signal"] = 0
        # Trend yukarı dönerse -> AL
        cross_up = (df["st_direction"] == 1) & (df["st_direction"].shift(1) == -1)
        # Trend aşağı dönerse -> SAT
        cross_down = (df["st_direction"] == -1) & (df["st_direction"].shift(1) == 1)

        df.loc[cross_up, "signal"] = 1
        df.loc[cross_down, "signal"] = -1

        return df

    def _compute_supertrend(
        self, df: pd.DataFrame, atr_period: int, multiplier: float
    ) -> tuple[pd.Series, pd.Series]:
        high = df["High"].values
        low = df["Low"].values
        close = df["Close"].values
        n = len(close)

        # ATR hesapla
        tr = np.zeros(n)
        tr[0] = high[0] - low[0]
        for i in range(1, n):
            tr[i] = max(
                high[i] - low[i],
                abs(high[i] - close[i - 1]),
                abs(low[i] - close[i - 1]),
            )
        atr = pd.Series(tr).rolling(window=atr_period).mean().values

        hl2 = (high + low) / 2
        basic_upper = hl2 + multiplier * atr
        basic_lower = hl2 - multiplier * atr

        final_upper = np.zeros(n)
        final_lower = np.zeros(n)
        supertrend = np.zeros(n)
        direction = np.zeros(n)

        final_upper[0] = basic_upper[0]
        final_lower[0] = basic_lower[0]
        direction[0] = 1

        for i in range(1, n):
            if np.isnan(atr[i]):
                final_upper[i] = basic_upper[i] if not np.isnan(basic_upper[i]) else 0
                final_lower[i] = basic_lower[i] if not np.isnan(basic_lower[i]) else 0
                direction[i] = direction[i - 1]
                supertrend[i] = final_lower[i] if direction[i] == 1 else final_upper[i]
                continue

            final_upper[i] = (
                min(basic_upper[i], final_upper[i - 1])
                if close[i - 1] <= final_upper[i - 1]
                else basic_upper[i]
            )
            final_lower[i] = (
                max(basic_lower[i], final_lower[i - 1])
                if close[i - 1] >= final_lower[i - 1]
                else basic_lower[i]
            )

            if direction[i - 1] == 1:
                direction[i] = -1 if close[i] < final_lower[i] else 1
            else:
                direction[i] = 1 if close[i] > final_upper[i] else -1

            supertrend[i] = final_lower[i] if direction[i] == 1 else final_upper[i]

        return pd.Series(supertrend, index=df.index), pd.Series(direction, index=df.index)

    def get_indicator_data(self, df: pd.DataFrame, **params) -> list[dict]:
        atr_period = int(params.get("atr_periyot", 10))
        multiplier = float(params.get("carpan", 3.0))

        supertrend, _ = self._compute_supertrend(df, atr_period, multiplier)
        # ATR periyodundan sonrasını al (ilk değerler anlamsız)
        valid = supertrend.iloc[atr_period:]

        return [
            {
                "name": "Supertrend",
                "values": [
                    {"date": str(date.date()), "value": round(val, 2)}
                    for date, val in valid.items()
                    if not np.isnan(val) and val > 0
                ],
            },
        ]
