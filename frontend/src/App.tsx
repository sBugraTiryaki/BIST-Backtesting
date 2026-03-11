import { useState } from 'react';
import { Dashboard } from './components/Layout/Dashboard';
import { ControlPanel } from './components/ControlPanel/ControlPanel';
import { ChartContainer } from './components/Charts/ChartContainer';
import { MetricsPanel } from './components/Results/MetricsPanel';
import { TradeTable } from './components/Results/TradeTable';
import { Spinner } from './components/common/Spinner';
import { ErrorAlert } from './components/common/ErrorAlert';
import { useStocks } from './hooks/useStocks';
import { useBacktest } from './hooks/useBacktest';
import { TrendingUp } from 'lucide-react';
import type { BacktestRequest } from './types';

function App() {
  const { stocks, strategies, loading: dataLoading, error: dataError } = useStocks();
  const { loading, error, result, execute } = useBacktest();
  const [sidebarOpen, setSidebarOpen] = useState(false);

  function handleRun(request: BacktestRequest) {
    setSidebarOpen(false);
    execute(request);
  }

  const sidebar = (
    <ControlPanel
      stocks={stocks}
      strategies={strategies}
      loading={loading}
      onRun={handleRun}
    />
  );

  return (
    <Dashboard sidebar={sidebar} sidebarOpen={sidebarOpen} onSidebarToggle={setSidebarOpen}>
      {dataLoading && <Spinner />}
      {dataError && <ErrorAlert message={dataError} />}
      {error && <ErrorAlert message={error} />}
      {loading && <Spinner />}

      {result && (
        <div className="space-y-6">
          <MetricsPanel metrics={result.metrics} />
          <ChartContainer result={result} />
          <TradeTable trades={result.trades} />
        </div>
      )}

      {!result && !loading && !error && !dataLoading && (
        <div className="flex h-full items-center justify-center">
          <div className="text-center space-y-3">
            <div className="mx-auto flex h-12 w-12 items-center justify-center rounded-full bg-muted">
              <TrendingUp className="h-6 w-6 text-muted-foreground" />
            </div>
            <div>
              <p className="text-sm text-muted-foreground">Hisse senedi ve strateji seçip</p>
              <p className="text-sm text-muted-foreground">"Backtest Başlat" butonuna basın.</p>
            </div>
          </div>
        </div>
      )}
    </Dashboard>
  );
}

export default App;
