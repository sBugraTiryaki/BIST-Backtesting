import numpy as np
import pandas as pd

from app.strategies.base import BaseStrategy


class ParabolicSAR(BaseStrategy):
    def generate_signals(self, df: pd.DataFrame, **params) -> pd.DataFrame:
        af_start = float(params.get("af_baslangic", 0.02))
        af_step = float(params.get("af_artis", 0.02))
        af_max = float(params.get("af_maks", 0.2))

        df = df.copy()
        sar, direction = self._compute_psar(df, af_start, af_step, af_max)
        df["psar"] = sar
        df["psar_direction"] = direction

        df["signal"] = 0
        # Trend yukarı dönerse -> AL
        cross_up = (df["psar_direction"] == 1) & (df["psar_direction"].shift(1) == -1)
        # Trend aşağı dönerse -> SAT
        cross_down = (df["psar_direction"] == -1) & (df["psar_direction"].shift(1) == 1)

        df.loc[cross_up, "signal"] = 1
        df.loc[cross_down, "signal"] = -1

        return df

    def _compute_psar(
        self, df: pd.DataFrame, af_start: float, af_step: float, af_max: float
    ) -> tuple[pd.Series, pd.Series]:
        high = df["High"].values
        low = df["Low"].values
        n = len(high)

        sar = np.zeros(n)
        direction = np.zeros(n)

        # İlk değerleri belirle
        is_uptrend = True
        af = af_start
        sar[0] = low[0]
        ep = high[0]
        direction[0] = 1

        for i in range(1, n):
            prev_sar = sar[i - 1]

            if is_uptrend:
                sar[i] = prev_sar + af * (ep - prev_sar)
                # SAR son 2 barın low'unun üstüne çıkamaz
                if i >= 2:
                    sar[i] = min(sar[i], low[i - 1], low[i - 2])
                else:
                    sar[i] = min(sar[i], low[i - 1])

                if low[i] < sar[i]:
                    # Trend dönüşü -> düşüş
                    is_uptrend = False
                    sar[i] = ep
                    ep = low[i]
                    af = af_start
                else:
                    if high[i] > ep:
                        ep = high[i]
                        af = min(af + af_step, af_max)
            else:
                sar[i] = prev_sar + af * (ep - prev_sar)
                # SAR son 2 barın high'ının altına düşemez
                if i >= 2:
                    sar[i] = max(sar[i], high[i - 1], high[i - 2])
                else:
                    sar[i] = max(sar[i], high[i - 1])

                if high[i] > sar[i]:
                    # Trend dönüşü -> yükseliş
                    is_uptrend = True
                    sar[i] = ep
                    ep = high[i]
                    af = af_start
                else:
                    if low[i] < ep:
                        ep = low[i]
                        af = min(af + af_step, af_max)

            direction[i] = 1 if is_uptrend else -1

        return pd.Series(sar, index=df.index), pd.Series(direction, index=df.index)

    def get_indicator_data(self, df: pd.DataFrame, **params) -> list[dict]:
        af_start = float(params.get("af_baslangic", 0.02))
        af_step = float(params.get("af_artis", 0.02))
        af_max = float(params.get("af_maks", 0.2))

        sar, _ = self._compute_psar(df, af_start, af_step, af_max)

        return [
            {
                "name": "Parabolic SAR",
                "values": [
                    {"date": str(date.date()), "value": round(val, 2)}
                    for date, val in sar.items()
                ],
            },
        ]
