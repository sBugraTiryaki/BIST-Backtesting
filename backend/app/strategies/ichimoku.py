import numpy as np
import pandas as pd

from app.strategies.base import BaseStrategy


class IchimokuCloud(BaseStrategy):
    def generate_signals(self, df: pd.DataFrame, **params) -> pd.DataFrame:
        tenkan_period = int(params.get("tenkan", 9))
        kijun_period = int(params.get("kijun", 26))
        senkou_b_period = int(params.get("senkou_b", 52))

        df = df.copy()
        df["tenkan_sen"] = (
            df["High"].rolling(window=tenkan_period).max()
            + df["Low"].rolling(window=tenkan_period).min()
        ) / 2
        df["kijun_sen"] = (
            df["High"].rolling(window=kijun_period).max()
            + df["Low"].rolling(window=kijun_period).min()
        ) / 2
        df["senkou_a"] = (df["tenkan_sen"] + df["kijun_sen"]) / 2
        df["senkou_b_line"] = (
            df["High"].rolling(window=senkou_b_period).max()
            + df["Low"].rolling(window=senkou_b_period).min()
        ) / 2

        # Bulutun üst sınırı
        cloud_top = df[["senkou_a", "senkou_b_line"]].max(axis=1)
        cloud_bottom = df[["senkou_a", "senkou_b_line"]].min(axis=1)

        df["signal"] = 0
        # Tenkan Kijun'u yukarı keserse ve fiyat bulutun üstündeyse -> AL
        tk_cross_up = (df["tenkan_sen"] > df["kijun_sen"]) & (
            df["tenkan_sen"].shift(1) <= df["kijun_sen"].shift(1)
        )
        above_cloud = df["Close"] > cloud_top

        # Tenkan Kijun'u aşağı keserse ve fiyat bulutun altındaysa -> SAT
        tk_cross_down = (df["tenkan_sen"] < df["kijun_sen"]) & (
            df["tenkan_sen"].shift(1) >= df["kijun_sen"].shift(1)
        )
        below_cloud = df["Close"] < cloud_bottom

        df.loc[tk_cross_up & above_cloud, "signal"] = 1
        df.loc[tk_cross_down & below_cloud, "signal"] = -1

        return df

    def get_indicator_data(self, df: pd.DataFrame, **params) -> list[dict]:
        tenkan_period = int(params.get("tenkan", 9))
        kijun_period = int(params.get("kijun", 26))
        senkou_b_period = int(params.get("senkou_b", 52))

        tenkan_sen = (
            df["High"].rolling(window=tenkan_period).max()
            + df["Low"].rolling(window=tenkan_period).min()
        ) / 2
        kijun_sen = (
            df["High"].rolling(window=kijun_period).max()
            + df["Low"].rolling(window=kijun_period).min()
        ) / 2
        senkou_a = (tenkan_sen + kijun_sen) / 2
        senkou_b = (
            df["High"].rolling(window=senkou_b_period).max()
            + df["Low"].rolling(window=senkou_b_period).min()
        ) / 2

        return [
            {
                "name": f"Tenkan-sen ({tenkan_period})",
                "values": [
                    {"date": str(date.date()), "value": round(val, 2)}
                    for date, val in tenkan_sen.dropna().items()
                ],
            },
            {
                "name": f"Kijun-sen ({kijun_period})",
                "values": [
                    {"date": str(date.date()), "value": round(val, 2)}
                    for date, val in kijun_sen.dropna().items()
                ],
            },
            {
                "name": "Senkou A",
                "values": [
                    {"date": str(date.date()), "value": round(val, 2)}
                    for date, val in senkou_a.dropna().items()
                ],
            },
            {
                "name": "Senkou B",
                "values": [
                    {"date": str(date.date()), "value": round(val, 2)}
                    for date, val in senkou_b.dropna().items()
                ],
            },
        ]
