from pydantic import BaseModel, Field


class BacktestRequest(BaseModel):
    symbol: str = Field(..., description="BIST hisse sembolü, ör: THYAO")
    start_date: str = Field(..., description="Başlangıç tarihi, ör: 2023-01-01")
    end_date: str = Field(..., description="Bitiş tarihi, ör: 2024-01-01")
    strategy: str = Field(..., description="Strateji adı: sma_crossover, rsi, macd")
    parameters: dict = Field(default_factory=dict, description="Strateji parametreleri")
    initial_capital: float = Field(default=100_000.0, description="Başlangıç sermayesi (TL)")
