import pandas as pd

from app.services.metrics import calculate_metrics
from app.strategies.base import BaseStrategy


def run_backtest(
    df: pd.DataFrame,
    strategy: BaseStrategy,
    params: dict,
    initial_capital: float = 100_000.0,
) -> dict:
    df = strategy.generate_signals(df, **params)
    indicator_data = strategy.get_indicator_data(df, **params)

    cash = initial_capital
    shares = 0.0
    entry_price = 0.0
    entry_date = None
    trades: list[dict] = []
    equity: list[float] = []
    signals: list[dict] = []

    for date, row in df.iterrows():
        date_str = str(date.date()) if hasattr(date, "date") else str(date)

        if row["signal"] == 1 and shares == 0:
            # AL: tüm nakitle hisse al
            shares = cash / row["Close"]
            entry_price = row["Close"]
            entry_date = date_str
            cash = 0.0
            signals.append({"date": date_str, "type": "AL", "price": round(row["Close"], 2)})

        elif row["signal"] == -1 and shares > 0:
            # SAT: tüm hisseleri sat
            cash = shares * row["Close"]
            pnl = (row["Close"] - entry_price) * shares
            return_pct = ((row["Close"] - entry_price) / entry_price) * 100
            trades.append(
                {
                    "entry_date": entry_date,
                    "exit_date": date_str,
                    "entry_price": round(entry_price, 2),
                    "exit_price": round(row["Close"], 2),
                    "shares": round(shares, 2),
                    "pnl": round(pnl, 2),
                    "return_pct": round(return_pct, 2),
                }
            )
            shares = 0.0
            signals.append({"date": date_str, "type": "SAT", "price": round(row["Close"], 2)})

        # Günlük portföy değeri
        portfolio_value = cash + (shares * row["Close"])
        equity.append(portfolio_value)

    equity_series = pd.Series(equity, index=df.index)

    metrics = calculate_metrics(equity_series, trades, initial_capital, df)

    # Response için formatlama
    price_data = [
        {
            "date": str(date.date()) if hasattr(date, "date") else str(date),
            "open": round(row["Open"], 2),
            "high": round(row["High"], 2),
            "low": round(row["Low"], 2),
            "close": round(row["Close"], 2),
            "volume": int(row["Volume"]),
        }
        for date, row in df.iterrows()
    ]

    equity_curve = [
        {
            "date": str(date.date()) if hasattr(date, "date") else str(date),
            "value": round(val, 2),
        }
        for date, val in equity_series.items()
    ]

    return {
        "price_data": price_data,
        "indicator_data": indicator_data,
        "signals": signals,
        "equity_curve": equity_curve,
        "metrics": metrics,
        "trades": trades,
    }
