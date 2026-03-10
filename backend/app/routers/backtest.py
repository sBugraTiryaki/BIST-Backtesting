from fastapi import APIRouter, HTTPException

from app.models.requests import BacktestRequest
from app.models.responses import (
    BacktestResponse,
    StrategiesResponse,
    StrategyInfo,
    StrategyParam,
)
from app.services.backtester import run_backtest
from app.services.data_fetcher import fetch_price_data
from app.strategies.macd import MACDStrategy
from app.strategies.rsi import RSIStrategy
from app.strategies.sma_crossover import SMACrossover

router = APIRouter(prefix="/api", tags=["backtest"])

STRATEGIES = {
    "sma_crossover": SMACrossover(),
    "rsi": RSIStrategy(),
    "macd": MACDStrategy(),
}

STRATEGY_DEFINITIONS = [
    StrategyInfo(
        id="sma_crossover",
        name="SMA Kesişim",
        description="Kısa ve uzun hareketli ortalama kesişimi ile alış/satış sinyali üretir.",
        parameters=[
            StrategyParam(key="kisa_periyot", label="Kısa Periyot", min=5, max=50, default=20, step=1),
            StrategyParam(key="uzun_periyot", label="Uzun Periyot", min=10, max=200, default=50, step=1),
        ],
    ),
    StrategyInfo(
        id="rsi",
        name="RSI",
        description="RSI aşırı alım/satım bölgelerinde alış/satış sinyali üretir.",
        parameters=[
            StrategyParam(key="periyot", label="RSI Periyot", min=5, max=30, default=14, step=1),
            StrategyParam(key="asiri_alim", label="Aşırı Alım", min=60, max=90, default=70, step=5),
            StrategyParam(key="asiri_satim", label="Aşırı Satım", min=10, max=40, default=30, step=5),
        ],
    ),
    StrategyInfo(
        id="macd",
        name="MACD",
        description="MACD ve sinyal çizgisi kesişimi ile trend takibi yapar.",
        parameters=[
            StrategyParam(key="hizli", label="Hızlı EMA", min=5, max=20, default=12, step=1),
            StrategyParam(key="yavas", label="Yavaş EMA", min=15, max=40, default=26, step=1),
            StrategyParam(key="sinyal", label="Sinyal Periyot", min=5, max=15, default=9, step=1),
        ],
    ),
]


@router.get("/strategies", response_model=StrategiesResponse)
async def get_strategies():
    return StrategiesResponse(strategies=STRATEGY_DEFINITIONS)


@router.post("/backtest", response_model=BacktestResponse)
async def run_backtest_endpoint(request: BacktestRequest):
    if request.strategy not in STRATEGIES:
        raise HTTPException(
            status_code=400,
            detail=f"Bilinmeyen strateji: {request.strategy}. Geçerli stratejiler: {list(STRATEGIES.keys())}",
        )

    try:
        df = fetch_price_data(request.symbol, request.start_date, request.end_date)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

    strategy = STRATEGIES[request.strategy]
    result = run_backtest(df, strategy, request.parameters, request.initial_capital)

    return BacktestResponse(**result)
