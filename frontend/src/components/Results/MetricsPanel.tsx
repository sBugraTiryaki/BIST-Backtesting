import { Card, CardContent } from '@/components/ui/card';
import type { Metrics } from '../../types';

interface Props {
  metrics: Metrics;
}

const fmt = new Intl.NumberFormat('tr-TR', { minimumFractionDigits: 2, maximumFractionDigits: 2 });

function MetricCard({ label, value, suffix = '', positive, sub, integer }: {
  label: string;
  value: number;
  suffix?: string;
  positive?: boolean;
  sub?: string;
  integer?: boolean;
}) {
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
          {integer ? value : fmt.format(value)}{suffix}
        </p>
        {sub && <p className="text-[10px] text-muted-foreground mt-0.5">{sub}</p>}
      </CardContent>
    </Card>
  );
}

export function MetricsPanel({ metrics }: Props) {
  const beatsBuyHold = metrics.total_return_pct > metrics.buy_hold_return_pct;
  const diff = metrics.total_return_pct - metrics.buy_hold_return_pct;

  return (
    <div>
      <h3 className="mb-3 text-sm font-medium text-muted-foreground">Performans</h3>
      <div className="grid grid-cols-2 gap-2 lg:grid-cols-4">
        <MetricCard
          label="Strateji Getirisi"
          value={metrics.total_return_pct}
          suffix="%"
          positive={metrics.total_return_pct > 0}
        />
        <MetricCard
          label="Al-Tut Getirisi"
          value={metrics.buy_hold_return_pct}
          suffix="%"
          positive={metrics.buy_hold_return_pct > 0}
          sub={`Strateji ${beatsBuyHold ? '+' : ''}${fmt.format(diff)} puan ${beatsBuyHold ? 'önde' : 'geride'}`}
        />
        <MetricCard
          label="Kârlı İşlem Oranı"
          value={metrics.win_rate_pct}
          suffix="%"
          positive={metrics.win_rate_pct > 50}
          sub={`${metrics.total_trades} işlemden ${metrics.winning_trades} tanesi kârlı`}
        />
        <MetricCard
          label="İşlem Sayısı"
          value={metrics.total_trades}
          integer
          sub={`${metrics.winning_trades} kârlı · ${metrics.losing_trades} zararlı`}
        />
      </div>
    </div>
  );
}
