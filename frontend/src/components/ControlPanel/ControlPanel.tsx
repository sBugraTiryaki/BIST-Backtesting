import { useState, useEffect } from 'react';
import type { StockInfo, StrategyInfo, BacktestRequest } from '../../types';
import { StockSelector } from './StockSelector';
import { DateRangePicker } from './DateRangePicker';
import { StrategySelector } from './StrategySelector';
import { ParameterSliders } from './ParameterSliders';
import { RunButton } from './RunButton';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Separator } from '@/components/ui/separator';
import { TrendingUp } from 'lucide-react';

interface Props {
  stocks: StockInfo[];
  strategies: StrategyInfo[];
  loading: boolean;
  onRun: (request: BacktestRequest) => void;
}

export function ControlPanel({ stocks, strategies, loading, onRun }: Props) {
  const [symbol, setSymbol] = useState('');
  const [strategyId, setStrategyId] = useState('');
  const [startDate, setStartDate] = useState('2024-01-01');
  const [endDate, setEndDate] = useState('2025-01-01');
  const [params, setParams] = useState<Record<string, number>>({});
  const [capital, setCapital] = useState(100_000);

  const selectedStrategy = strategies.find((s) => s.id === strategyId);

  useEffect(() => {
    if (selectedStrategy) {
      const defaults: Record<string, number> = {};
      for (const p of selectedStrategy.parameters) {
        defaults[p.key] = p.default;
      }
      setParams(defaults);
    }
  }, [strategyId]);

  const canRun = symbol && strategyId && startDate && endDate;

  function handleRun() {
    if (!canRun) return;
    onRun({
      symbol,
      start_date: startDate,
      end_date: endDate,
      strategy: strategyId,
      parameters: params,
      initial_capital: capital,
    });
  }

  return (
    <aside className="flex h-full w-80 shrink-0 flex-col overflow-hidden border-r border-border bg-card">
      {/* Header */}
      <div className="flex items-center gap-2.5 border-b border-border px-5 py-4">
        <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-green-500/15">
          <TrendingUp className="h-4 w-4 text-green-400" />
        </div>
        <div>
          <h1 className="text-sm font-bold">BIST-Backtesting</h1>
          <p className="text-[10px] text-muted-foreground">Strateji test aracı</p>
        </div>
      </div>

      {/* Scrollable form */}
      <div className="min-h-0 flex-1 overflow-y-auto">
        <div className="flex flex-col gap-5 p-5">
          <StockSelector stocks={stocks} value={symbol} onChange={setSymbol} />
          <Separator />
          <DateRangePicker
            startDate={startDate}
            endDate={endDate}
            onStartChange={setStartDate}
            onEndChange={setEndDate}
          />
          <Separator />
          <StrategySelector strategies={strategies} value={strategyId} onChange={setStrategyId} />

          {selectedStrategy && (
            <>
              <Separator />
              <ParameterSliders
                params={selectedStrategy.parameters}
                values={params}
                onChange={(key, val) => setParams((prev) => ({ ...prev, [key]: val }))}
              />
            </>
          )}

          <Separator />
          <div className="space-y-2">
            <Label className="text-xs text-muted-foreground">Başlangıç Sermayesi</Label>
            <div className="relative">
              <span className="absolute left-3 top-1/2 -translate-y-1/2 text-xs text-muted-foreground">₺</span>
              <Input
                type="number"
                value={capital}
                onChange={(e) => setCapital(Number(e.target.value))}
                className="pl-7 font-mono"
              />
            </div>
          </div>
        </div>
      </div>

      {/* Sticky button */}
      <div className="border-t border-border p-4">
        <RunButton onClick={handleRun} loading={loading} disabled={!canRun} />
      </div>
    </aside>
  );
}
