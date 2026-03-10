import type { BacktestRequest, BacktestResult, StockInfo, StrategyInfo } from '../types';

const BASE_URL = '/api';

async function fetchJSON<T>(url: string, options?: RequestInit): Promise<T> {
  const res = await fetch(`${BASE_URL}${url}`, {
    headers: { 'Content-Type': 'application/json' },
    ...options,
  });
  if (!res.ok) {
    const error = await res.json().catch(() => ({ detail: 'Bilinmeyen hata' }));
    throw new Error(error.detail || `HTTP ${res.status}`);
  }
  return res.json();
}

export async function getStocks(): Promise<StockInfo[]> {
  const data = await fetchJSON<{ stocks: StockInfo[] }>('/stocks');
  return data.stocks;
}

export async function getStrategies(): Promise<StrategyInfo[]> {
  const data = await fetchJSON<{ strategies: StrategyInfo[] }>('/strategies');
  return data.strategies;
}

export async function runBacktest(request: BacktestRequest): Promise<BacktestResult> {
  return fetchJSON<BacktestResult>('/backtest', {
    method: 'POST',
    body: JSON.stringify(request),
  });
}
