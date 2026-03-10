import numpy as np
import pandas as pd
import pytest

from app.services.backtester import run_backtest
from app.services.metrics import calculate_metrics
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


class TestBacktester:
    def test_run_backtest_returns_correct_structure(self):
        prices = list(range(50, 60)) + list(range(60, 80)) + list(range(80, 100))
        df = make_price_df(prices)
        strategy = SMACrossover()

        result = run_backtest(df, strategy, {"kisa_periyot": 5, "uzun_periyot": 10}, 100_000)

        assert "price_data" in result
        assert "indicator_data" in result
        assert "signals" in result
        assert "equity_curve" in result
        assert "metrics" in result
        assert "trades" in result
        assert len(result["price_data"]) == len(prices)
        assert len(result["equity_curve"]) == len(prices)

    def test_initial_capital_preserved_without_trades(self):
        # Sabit fiyat -> SMA'lar esit -> sinyal yok -> sermaye degismemeli
        prices = [100.0] * 100
        df = make_price_df(prices)
        strategy = SMACrossover()

        result = run_backtest(df, strategy, {"kisa_periyot": 5, "uzun_periyot": 10}, 100_000)

        assert result["equity_curve"][-1]["value"] == 100_000
        assert len(result["trades"]) == 0


class TestMetrics:
    def test_positive_return(self):
        equity = pd.Series([100_000, 105_000, 110_000, 115_000, 120_000])
        trades = [
            {"pnl": 10_000, "return_pct": 10},
            {"pnl": 10_000, "return_pct": 10},
        ]
        df = make_price_df([100, 105, 110, 115, 120])

        metrics = calculate_metrics(equity, trades, 100_000, df)

        assert metrics["total_return_pct"] == 20.0
        assert metrics["total_trades"] == 2
        assert metrics["winning_trades"] == 2
        assert metrics["losing_trades"] == 0
        assert metrics["win_rate_pct"] == 100.0

    def test_max_drawdown(self):
        equity = pd.Series([100_000, 110_000, 90_000, 95_000])
        trades = []
        df = make_price_df([100, 110, 90, 95])

        metrics = calculate_metrics(equity, trades, 100_000, df)

        # 110k -> 90k = %18.18 drawdown
        expected_dd = (110_000 - 90_000) / 110_000 * 100
        assert abs(metrics["max_drawdown_pct"] - expected_dd) < 0.1

    def test_no_trades(self):
        equity = pd.Series([100_000, 100_000])
        metrics = calculate_metrics(equity, [], 100_000, make_price_df([100, 100]))

        assert metrics["total_trades"] == 0
        assert metrics["win_rate_pct"] == 0.0
        assert metrics["avg_trade_return_pct"] == 0.0
