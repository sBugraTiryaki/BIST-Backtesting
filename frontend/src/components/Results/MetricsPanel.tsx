import { Card, CardContent } from '@/components/ui/card';
import type { Metrics } from '../../types';

interface Props {
  metrics: Metrics;
}

const fmt = new Intl.NumberFormat('tr-TR', { minimumFractionDigits: 2, maximumFractionDigits: 2 });

function MetricCard({ label, value, suffix = '', positive }: { label: string; value: number; suffix?: string; positive?: boolean }) {
  const color = positive === undefined
    ? 'text-foreground'
    : positive
      ? 'text-green-400'
      : 'text-red-400';

  return (
    <Card>
      <CardContent className="p-3">
        <p className="text-[11px] text-muted-foreground">{label}</p>
        <p className={`mt-1 text-lg font-semibold tabular-nums ${color}`}>
          {fmt.format(value)}{suffix}
        </p>
      </CardContent>
    </Card>
  );
}

export function MetricsPanel({ metrics }: Props) {
  return (
    <div>
      <h3 className="mb-3 text-sm font-medium text-muted-foreground">Performans Metrikleri</h3>
      <div className="grid grid-cols-2 gap-2 lg:grid-cols-3 xl:grid-cols-5">
        <MetricCard label="Toplam Getiri" value={metrics.total_return_pct} suffix="%" positive={metrics.total_return_pct > 0} />
        <MetricCard label="Al-Tut Getirisi" value={metrics.buy_hold_return_pct} suffix="%" positive={metrics.buy_hold_return_pct > 0} />
        <MetricCard label="Maks. Düşüş" value={-metrics.max_drawdown_pct} suffix="%" positive={false} />
        <MetricCard label="Sharpe Oranı" value={metrics.sharpe_ratio} positive={metrics.sharpe_ratio > 0} />
        <MetricCard label="Kazanma Oranı" value={metrics.win_rate_pct} suffix="%" positive={metrics.win_rate_pct > 50} />
        <MetricCard label="Toplam İşlem" value={metrics.total_trades} />
        <MetricCard label="Kazanan" value={metrics.winning_trades} positive={true} />
        <MetricCard label="Kaybeden" value={metrics.losing_trades} positive={false} />
        <MetricCard label="Ort. İşlem Getirisi" value={metrics.avg_trade_return_pct} suffix="%" positive={metrics.avg_trade_return_pct > 0} />
        <MetricCard label="Kâr Faktörü" value={metrics.profit_factor} positive={metrics.profit_factor > 1} />
      </div>
    </div>
  );
}
