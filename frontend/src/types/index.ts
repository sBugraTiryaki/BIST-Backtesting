export interface StockInfo {
  symbol: string;
  name: string;
  yahoo_symbol: string;
}

export interface OHLCV {
  date: string;
  open: number;
  high: number;
  low: number;
  close: number;
  volume: number;
}

export interface StrategyParam {
  key: string;
  label: string;
  type: string;
  min: number;
  max: number;
  default: number;
  step: number;
  description?: string;
}

export interface StrategyInfo {
  id: string;
  name: string;
  description: string;
  parameters: StrategyParam[];
}

export interface TradeRecord {
  entry_date: string;
  exit_date: string;
  entry_price: number;
  exit_price: number;
  shares: number;
  pnl: number;
  return_pct: number;
}

export interface Metrics {
  total_return_pct: number;
  buy_hold_return_pct: number;
  max_drawdown_pct: number;
  sharpe_ratio: number;
  win_rate_pct: number;
  total_trades: number;
  winning_trades: number;
  losing_trades: number;
  avg_trade_return_pct: number;
  profit_factor: number;
}

export interface EquityPoint {
  date: string;
  value: number;
}

export interface SignalPoint {
  date: string;
  type: 'AL' | 'SAT';
  price: number;
}

export interface IndicatorData {
  name: string;
  values: { date: string; value: number }[];
  overlay?: boolean; // true: fiyat grafiği üzerine, false: ayrı panel
}

export interface BacktestResult {
  price_data: OHLCV[];
  indicator_data: IndicatorData[];
  signals: SignalPoint[];
  equity_curve: EquityPoint[];
  metrics: Metrics;
  trades: TradeRecord[];
}

export interface BacktestRequest {
  symbol: string;
  start_date: string;
  end_date: string;
  strategy: string;
  parameters: Record<string, number>;
  initial_capital: number;
}
