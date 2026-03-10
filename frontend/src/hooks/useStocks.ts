import { useEffect, useState } from 'react';
import { getStocks, getStrategies } from '../api/client';
import type { StockInfo, StrategyInfo } from '../types';

export function useStocks() {
  const [stocks, setStocks] = useState<StockInfo[]>([]);
  const [strategies, setStrategies] = useState<StrategyInfo[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function load() {
      try {
        const [stocksData, strategiesData] = await Promise.all([
          getStocks(),
          getStrategies(),
        ]);
        setStocks(stocksData);
        setStrategies(strategiesData);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Veri yüklenemedi');
      } finally {
        setLoading(false);
      }
    }
    load();
  }, []);

  return { stocks, strategies, loading, error };
}
