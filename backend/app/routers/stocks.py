from fastapi import APIRouter, HTTPException, Query

from app.config import BIST100
from app.models.responses import OHLCV, PriceResponse, StockInfo, StocksResponse
from app.services.data_fetcher import fetch_price_data

router = APIRouter(prefix="/api/stocks", tags=["stocks"])


@router.get("", response_model=StocksResponse)
async def get_stocks():
    return StocksResponse(
        stocks=[StockInfo(**stock) for stock in BIST100]
    )


@router.get("/{symbol}/price", response_model=PriceResponse)
async def get_price(
    symbol: str,
    start_date: str = Query(..., description="Başlangıç tarihi (YYYY-MM-DD)"),
    end_date: str = Query(..., description="Bitiş tarihi (YYYY-MM-DD)"),
):
    try:
        df = fetch_price_data(symbol.upper(), start_date, end_date)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

    data = [
        OHLCV(
            date=str(date.date()),
            open=round(row["Open"], 2),
            high=round(row["High"], 2),
            low=round(row["Low"], 2),
            close=round(row["Close"], 2),
            volume=int(row["Volume"]),
        )
        for date, row in df.iterrows()
    ]

    return PriceResponse(symbol=symbol.upper(), data=data)
