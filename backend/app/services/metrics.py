import numpy as np
import pandas as pd


def calculate_metrics(
    equity_curve: pd.Series,
    trades: list[dict],
    initial_capital: float,
    price_data: pd.DataFrame,
) -> dict:
    # Toplam getiri
    final_value = equity_curve.iloc[-1]
    total_return_pct = ((final_value - initial_capital) / initial_capital) * 100

    # Buy & hold getirisi
    buy_hold_return_pct = (
        (price_data["Close"].iloc[-1] - price_data["Close"].iloc[0])
        / price_data["Close"].iloc[0]
        * 100
    )

    # Max drawdown
    running_max = equity_curve.cummax()
    drawdown = (equity_curve - running_max) / running_max
    max_drawdown_pct = abs(drawdown.min()) * 100

    # Sharpe oranı (yıllık, risk-free=0)
    daily_returns = equity_curve.pct_change().dropna()
    if daily_returns.std() > 0:
        sharpe_ratio = (daily_returns.mean() / daily_returns.std()) * np.sqrt(252)
    else:
        sharpe_ratio = 0.0

    # İşlem istatistikleri
    total_trades = len(trades)
    winning_trades = sum(1 for t in trades if t["pnl"] > 0)
    losing_trades = sum(1 for t in trades if t["pnl"] <= 0)
    win_rate_pct = (winning_trades / total_trades * 100) if total_trades > 0 else 0.0

    # Ortalama işlem getirisi
    avg_trade_return_pct = (
        np.mean([t["return_pct"] for t in trades]) if total_trades > 0 else 0.0
    )

    # Kâr faktörü
    gross_profit = sum(t["pnl"] for t in trades if t["pnl"] > 0)
    gross_loss = abs(sum(t["pnl"] for t in trades if t["pnl"] < 0))
    profit_factor = (gross_profit / gross_loss) if gross_loss > 0 else float("inf")
    if profit_factor == float("inf"):
        profit_factor = 0.0 if gross_profit == 0 else 99.99

    return {
        "total_return_pct": round(total_return_pct, 2),
        "buy_hold_return_pct": round(buy_hold_return_pct, 2),
        "max_drawdown_pct": round(max_drawdown_pct, 2),
        "sharpe_ratio": round(sharpe_ratio, 2),
        "win_rate_pct": round(win_rate_pct, 2),
        "total_trades": total_trades,
        "winning_trades": winning_trades,
        "losing_trades": losing_trades,
        "avg_trade_return_pct": round(avg_trade_return_pct, 2),
        "profit_factor": round(profit_factor, 2),
    }
