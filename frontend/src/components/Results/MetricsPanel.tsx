import { useState, useRef } from 'react';
import { Card, CardContent } from '@/components/ui/card';
import { Info } from 'lucide-react';
import type { Metrics } from '../../types';

interface Props {
  metrics: Metrics;
}

const fmt = new Intl.NumberFormat('tr-TR', { minimumFractionDigits: 2, maximumFractionDigits: 2 });

function MetricCard({ label, value, suffix = '', positive, sub, integer, tooltip }: {
  label: string;
  value: number;
  suffix?: string;
  positive?: boolean;
  sub?: string;
  integer?: boolean;
  tooltip?: string;
}) {
  const [showTooltip, setShowTooltip] = useState(false);
  const hoverTimer = useRef<number>(undefined);
  const color = positive === undefined
    ? 'text-foreground'
    : positive
      ? 'text-green-400'
      : 'text-red-400';

  return (
    <Card>
      <CardContent className="p-3">
        <div className="flex items-center gap-1">
          <p className="text-[11px] text-muted-foreground">{label}</p>
          {tooltip && (
            <div
              className="relative"
              onMouseEnter={() => { hoverTimer.current = window.setTimeout(() => setShowTooltip(true), 400); }}
              onMouseLeave={() => { clearTimeout(hoverTimer.current); setShowTooltip(false); }}
            >
              <button
                onClick={() => setShowTooltip((v) => !v)}
                className="text-muted-foreground/50 hover:text-muted-foreground transition-colors"
              >
                <Info className="h-3 w-3" />
              </button>
              {showTooltip && (
                <div className="absolute left-0 top-full mt-1.5 w-56 rounded-lg bg-popover border border-border p-2.5 text-[11px] leading-relaxed text-muted-foreground shadow-lg z-20">
                  {tooltip}
                </div>
              )}
            </div>
          )}
        </div>
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
          label="Sharpe Oranı"
          value={metrics.sharpe_ratio}
          positive={metrics.sharpe_ratio > 0}
          sub={metrics.sharpe_ratio >= 2 ? 'Çok iyi' : metrics.sharpe_ratio >= 1 ? 'İyi' : metrics.sharpe_ratio >= 0 ? 'Düşük' : 'Negatif'}
          tooltip="Getirinin riske oranını ölçer. Yüksek getiri + düşük dalgalanma = yüksek Sharpe. 1 üzeri iyi, 2 üzeri çok iyi sayılır."
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
