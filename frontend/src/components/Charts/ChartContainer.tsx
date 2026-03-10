import { useCallback, useRef } from 'react';
import type { IChartApi, LogicalRange } from 'lightweight-charts';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import type { BacktestResult } from '../../types';
import { PriceChart } from './PriceChart';
import { IndicatorChart } from './IndicatorChart';
import { EquityCurve } from './EquityCurve';

interface Props {
  result: BacktestResult;
}

export function ChartContainer({ result }: Props) {
  const chartsRef = useRef<IChartApi[]>([]);
  const isSyncing = useRef(false);

  const syncAll = useCallback((source: IChartApi) => {
    source.timeScale().subscribeVisibleLogicalRangeChange((range: LogicalRange | null) => {
      if (isSyncing.current || !range) return;
      isSyncing.current = true;
      for (const chart of chartsRef.current) {
        if (chart !== source) {
          chart.timeScale().setVisibleLogicalRange(range);
        }
      }
      isSyncing.current = false;
    });
  }, []);

  const registerChart = useCallback((chart: IChartApi) => {
    chartsRef.current.push(chart);
    syncAll(chart);
  }, [syncAll]);

  // Overlay indikatörler (SMA gibi) fiyat grafiğinin üstüne
  const overlayIndicators = result.indicator_data.filter((ind) => ind.overlay !== false);
  // Osilatör indikatörler (RSI, MACD) ayrı panelde
  const oscillatorIndicators = result.indicator_data.filter((ind) => ind.overlay === false);

  // Osilatör paneli başlığı
  const oscillatorTitle = oscillatorIndicators.length > 0
    ? oscillatorIndicators[0].name.split(' ')[0] // "RSI 14" -> "RSI", "MACD" -> "MACD"
    : '';

  return (
    <div className="space-y-4">
      <Card>
        <CardHeader className="pb-2">
          <CardTitle className="text-sm font-medium text-muted-foreground">Fiyat Grafiği</CardTitle>
        </CardHeader>
        <CardContent className="p-2">
          <PriceChart
            priceData={result.price_data}
            indicators={overlayIndicators}
            signals={result.signals}
            onChartReady={registerChart}
          />
        </CardContent>
      </Card>

      {oscillatorIndicators.length > 0 && (
        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium text-muted-foreground">{oscillatorTitle}</CardTitle>
          </CardHeader>
          <CardContent className="p-2">
            <IndicatorChart
              indicators={oscillatorIndicators}
              onChartReady={registerChart}
            />
          </CardContent>
        </Card>
      )}

      <Card>
        <CardHeader className="pb-2">
          <CardTitle className="text-sm font-medium text-muted-foreground">Portföy Değeri</CardTitle>
        </CardHeader>
        <CardContent className="p-2">
          <EquityCurve
            data={result.equity_curve}
            onChartReady={registerChart}
          />
        </CardContent>
      </Card>
    </div>
  );
}
