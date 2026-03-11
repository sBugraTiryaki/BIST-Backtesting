import { Label } from '@/components/ui/label';
import type { StrategyInfo } from '../../types';
import { cn } from '@/lib/utils';

interface Props {
  strategies: StrategyInfo[];
  value: string;
  onChange: (id: string) => void;
}

export function StrategySelector({ strategies, value, onChange }: Props) {
  return (
    <div className="space-y-2">
      <Label className="text-xs text-muted-foreground">Strateji</Label>
      <div className="max-h-64 overflow-y-auto rounded-lg border border-border p-1 space-y-1.5">
        {strategies.map((s) => (
          <button
            key={s.id}
            onClick={() => onChange(s.id)}
            className={cn(
              'w-full rounded-lg border px-3 py-2.5 text-left transition-all',
              s.id === value
                ? 'border-green-500/50 bg-green-500/10 text-green-400'
                : 'border-border bg-card text-card-foreground hover:bg-accent'
            )}
          >
            <span className="text-sm font-medium">{s.name}</span>
            <p className="mt-0.5 text-[11px] leading-tight text-muted-foreground">{s.description}</p>
          </button>
        ))}
      </div>
    </div>
  );
}
