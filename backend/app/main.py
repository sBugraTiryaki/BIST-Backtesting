from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import backtest, stocks

app = FastAPI(
    title="BIST-Backtesting API",
    description="Borsa İstanbul hisse senetleri için backtesting aracı",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(stocks.router)
app.include_router(backtest.router)


@app.get("/")
async def root():
    return {"message": "BIST-Backtesting API", "docs": "/docs"}
