import { Label } from '@/components/ui/label';
import { Slider } from '@/components/ui/slider';
import { Badge } from '@/components/ui/badge';
import type { StrategyParam } from '../../types';

interface Props {
  params: StrategyParam[];
  values: Record<string, number>;
  onChange: (key: string, value: number) => void;
}

export function ParameterSliders({ params, values, onChange }: Props) {
  if (params.length === 0) return null;

  return (
    <div className="space-y-3">
      <Label className="text-xs text-muted-foreground">Parametreler</Label>
      {params.map((p) => {
        const val = values[p.key] ?? p.default;
        return (
          <div key={p.key} className="rounded-lg border border-border bg-card p-3 space-y-2">
            <div className="flex items-center justify-between">
              <span className="text-xs text-muted-foreground">{p.label}</span>
              <Badge variant="secondary" className="font-mono text-xs text-green-400">{val}</Badge>
            </div>
            {p.description && (
              <p className="text-[10px] leading-tight text-muted-foreground">{p.description}</p>
            )}
            <Slider
              min={p.min}
              max={p.max}
              step={p.step}
              value={val}
              onValueChange={(v) => onChange(p.key, Array.isArray(v) ? v[0] : v)}
            />
            <div className="flex justify-between text-[10px] text-muted-foreground">
              <span>{p.min}</span>
              <span>{p.max}</span>
            </div>
          </div>
        );
      })}
    </div>
  );
}
