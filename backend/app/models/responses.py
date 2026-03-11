from pydantic import BaseModel


class StockInfo(BaseModel):
    symbol: str
    name: str
    yahoo_symbol: str


class StocksResponse(BaseModel):
    stocks: list[StockInfo]


class OHLCV(BaseModel):
    date: str
    open: float
    high: float
    low: float
    close: float
    volume: int


class PriceResponse(BaseModel):
    symbol: str
    data: list[OHLCV]


class StrategyParam(BaseModel):
    key: str
    label: str
    type: str = "int"
    min: float
    max: float
    default: float
    step: float = 1
    description: str = ""


class StrategyInfo(BaseModel):
    id: str
    name: str
    description: str
    parameters: list[StrategyParam]


class StrategiesResponse(BaseModel):
    strategies: list[StrategyInfo]


class TradeRecord(BaseModel):
    entry_date: str
    exit_date: str
    entry_price: float
    exit_price: float
    shares: float
    pnl: float
    return_pct: float


class Metrics(BaseModel):
    total_return_pct: float
    buy_hold_return_pct: float
    max_drawdown_pct: float
    sharpe_ratio: float
    win_rate_pct: float
    total_trades: int
    winning_trades: int
    losing_trades: int
    avg_trade_return_pct: float
    profit_factor: float


class EquityPoint(BaseModel):
    date: str
    value: float


class SignalPoint(BaseModel):
    date: str
    type: str  # "AL" veya "SAT"
    price: float


class IndicatorData(BaseModel):
    name: str
    values: list[dict]
    overlay: bool = True  # True: fiyat grafigi uzerine, False: ayri panel


class BacktestResponse(BaseModel):
    price_data: list[OHLCV]
    indicator_data: list[IndicatorData]
    signals: list[SignalPoint]
    equity_curve: list[EquityPoint]
    metrics: Metrics
    trades: list[TradeRecord]
