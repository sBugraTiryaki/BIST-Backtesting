from abc import ABC, abstractmethod

import pandas as pd


class BaseStrategy(ABC):
    @abstractmethod
    def generate_signals(self, df: pd.DataFrame, **params) -> pd.DataFrame:
        """
        df: OHLCV DataFrame (Date index, Open/High/Low/Close/Volume columns)
        Return: aynı df'e 'signal' kolonu eklenmiş hali
            signal = 1  -> AL
            signal = -1 -> SAT
            signal = 0  -> bekle
        """
        ...

    @abstractmethod
    def get_indicator_data(self, df: pd.DataFrame, **params) -> list[dict]:
        """
        Grafik overlay için indikatör verilerini döndürür.
        Her eleman: {"name": "SMA 20", "values": [{"date": ..., "value": ...}]}
        """
        ...
