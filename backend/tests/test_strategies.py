import numpy as np
import pandas as pd
import pytest

from app.strategies.macd import MACDStrategy
from app.strategies.rsi import RSIStrategy, compute_rsi
from app.strategies.sma_crossover import SMACrossover


def make_price_df(prices: list[float]) -> pd.DataFrame:
    dates = pd.date_range("2023-01-01", periods=len(prices), freq="B")
    return pd.DataFrame(
        {
            "Open": prices,
            "High": [p * 1.02 for p in prices],
            "Low": [p * 0.98 for p in prices],
            "Close": prices,
            "Volume": [1000000] * len(prices),
        },
        index=dates,
    )


class TestSMACrossover:
    def test_signal_generation(self):
        # Dusus -> yukselis -> dusus: SMA kesisimi olusturur
        prices = [100 - i for i in range(20)] + [80 + i * 2 for i in range(30)]
        df = make_price_df(prices)
        strategy = SMACrossover()
        result = strategy.generate_signals(df, kisa_periyot=5, uzun_periyot=10)

        assert "signal" in result.columns
        assert "sma_short" in result.columns
        assert "sma_long" in result.columns
        # En az bir sinyal olmali
        assert (result["signal"] != 0).any()

    def test_indicator_data(self):
        prices = list(range(50, 100))
        df = make_price_df(prices)
        strategy = SMACrossover()
        result = strategy.generate_signals(df, kisa_periyot=5, uzun_periyot=10)
        indicators = strategy.get_indicator_data(df, kisa_periyot=5, uzun_periyot=10)

        assert len(indicators) == 2
        assert indicators[0]["name"] == "SMA 5"
        assert indicators[1]["name"] == "SMA 10"


class TestRSI:
    def test_compute_rsi_range(self):
        prices = [100 + np.sin(i * 0.5) * 10 for i in range(100)]
        series = pd.Series(prices)
        rsi = compute_rsi(series, 14)

        valid_rsi = rsi.dropna()
        assert (valid_rsi >= 0).all()
        assert (valid_rsi <= 100).all()

    def test_signal_generation(self):
        # Dalgali fiyat -> RSI sinyalleri uretmeli
        prices = [100 + np.sin(i * 0.3) * 20 for i in range(200)]
        df = make_price_df(prices)
        strategy = RSIStrategy()
        result = strategy.generate_signals(df, periyot=14, asiri_alim=70, asiri_satim=30)

        assert "signal" in result.columns
        assert "rsi" in result.columns


class TestMACD:
    def test_signal_generation(self):
        prices = [100 + np.sin(i * 0.2) * 15 for i in range(200)]
        df = make_price_df(prices)
        strategy = MACDStrategy()
        result = strategy.generate_signals(df, hizli=12, yavas=26, sinyal=9)

        assert "signal" in result.columns
        assert "macd_line" in result.columns
        assert "signal_line" in result.columns

    def test_indicator_data(self):
        prices = [100 + np.sin(i * 0.2) * 15 for i in range(200)]
        df = make_price_df(prices)
        strategy = MACDStrategy()
        indicators = strategy.get_indicator_data(df, hizli=12, yavas=26, sinyal=9)

        assert len(indicators) == 2
        assert indicators[0]["name"] == "MACD"
        assert indicators[1]["name"] == "Sinyal"
