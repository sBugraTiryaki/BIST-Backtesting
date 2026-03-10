import { format } from 'date-fns';
import { tr } from 'date-fns/locale';
import { CalendarIcon } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Calendar } from '@/components/ui/calendar';
import { Label } from '@/components/ui/label';
import { Popover, PopoverContent, PopoverTrigger } from '@/components/ui/popover';

interface Props {
  startDate: string;
  endDate: string;
  onStartChange: (date: string) => void;
  onEndChange: (date: string) => void;
}

const PRESETS = [
  { label: '6A', months: 6 },
  { label: '1Y', months: 12 },
  { label: '2Y', months: 24 },
  { label: '5Y', months: 60 },
];

function toISO(date: Date) {
  return date.toISOString().split('T')[0];
}

function DateButton({ label, date, onSelect }: { label: string; date: string; onSelect: (d: Date) => void }) {
  const parsed = date ? new Date(date + 'T00:00:00') : undefined;
  return (
    <div className="flex-1 space-y-1">
      <span className="text-[11px] text-muted-foreground">{label}</span>
      <Popover>
        <PopoverTrigger
          render={<Button variant="outline" />}
          className="w-full justify-start text-left text-xs font-mono"
        >
          <CalendarIcon className="mr-2 h-3.5 w-3.5 opacity-50" />
          {parsed ? format(parsed, 'dd MMM yyyy', { locale: tr }) : 'Seç...'}
        </PopoverTrigger>
        <PopoverContent className="w-auto p-0" align="start">
          <Calendar
            mode="single"
            selected={parsed}
            onSelect={(d) => d && onSelect(d)}
            locale={tr}
            initialFocus
          />
        </PopoverContent>
      </Popover>
    </div>
  );
}

export function DateRangePicker({ startDate, endDate, onStartChange, onEndChange }: Props) {
  return (
    <div className="space-y-2">
      <Label className="text-xs text-muted-foreground">Tarih Aralığı</Label>

      {/* Preset butonlari */}
      <div className="flex gap-1">
        {PRESETS.map((p) => (
          <Button
            key={p.label}
            variant="outline"
            size="sm"
            className="flex-1 text-xs"
            onClick={() => {
              const end = new Date();
              const start = new Date();
              start.setMonth(start.getMonth() - p.months);
              onStartChange(toISO(start));
              onEndChange(toISO(end));
            }}
          >
            {p.label}
          </Button>
        ))}
      </div>

      {/* Takvim popover'lari */}
      <div className="flex gap-2">
        <DateButton label="Başlangıç" date={startDate} onSelect={(d) => onStartChange(toISO(d))} />
        <DateButton label="Bitiş" date={endDate} onSelect={(d) => onEndChange(toISO(d))} />
      </div>
    </div>
  );
}
