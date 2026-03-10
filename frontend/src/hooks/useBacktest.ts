import { useReducer } from 'react';
import { runBacktest } from '../api/client';
import type { BacktestRequest, BacktestResult } from '../types';

interface State {
  loading: boolean;
  error: string | null;
  result: BacktestResult | null;
}

type Action =
  | { type: 'START' }
  | { type: 'SUCCESS'; payload: BacktestResult }
  | { type: 'ERROR'; payload: string };

function reducer(_state: State, action: Action): State {
  switch (action.type) {
    case 'START':
      return { loading: true, error: null, result: null };
    case 'SUCCESS':
      return { loading: false, error: null, result: action.payload };
    case 'ERROR':
      return { loading: false, error: action.payload, result: null };
  }
}

export function useBacktest() {
  const [state, dispatch] = useReducer(reducer, {
    loading: false,
    error: null,
    result: null,
  });

  async function execute(request: BacktestRequest) {
    dispatch({ type: 'START' });
    try {
      const result = await runBacktest(request);
      dispatch({ type: 'SUCCESS', payload: result });
    } catch (err) {
      dispatch({
        type: 'ERROR',
        payload: err instanceof Error ? err.message : 'Backtest başarısız',
      });
    }
  }

  return { ...state, execute };
}
