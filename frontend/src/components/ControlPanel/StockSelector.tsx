import { useState } from 'react';
import { Popover, PopoverContent, PopoverTrigger } from '@/components/ui/popover';
import { Command, CommandEmpty, CommandGroup, CommandInput, CommandItem, CommandList } from '@/components/ui/command';
import { Button } from '@/components/ui/button';
import { Label } from '@/components/ui/label';
import { ChevronsUpDown, Check } from 'lucide-react';
import type { StockInfo } from '../../types';

interface Props {
  stocks: StockInfo[];
  value: string;
  onChange: (symbol: string) => void;
}

export function StockSelector({ stocks, value, onChange }: Props) {
  const [open, setOpen] = useState(false);
  const selected = stocks.find((s) => s.symbol === value);

  return (
    <div className="space-y-2">
      <Label className="text-xs text-muted-foreground">Hisse Senedi</Label>
      <Popover open={open} onOpenChange={setOpen}>
        <PopoverTrigger
          render={<Button variant="outline" />}
          role="combobox"
          aria-expanded={open}
          className="w-full justify-between font-normal"
        >
            {selected ? (
              <span>
                <span className="font-semibold text-green-400">{selected.symbol}</span>
                <span className="ml-2 text-muted-foreground">{selected.name}</span>
              </span>
            ) : (
              <span className="text-muted-foreground">Hisse seçin...</span>
            )}
            <ChevronsUpDown className="ml-2 h-4 w-4 shrink-0 opacity-50" />
        </PopoverTrigger>
        <PopoverContent className="w-[280px] p-0" align="start">
          <Command>
            <CommandInput placeholder="Ara..." />
            <CommandList>
              <CommandEmpty>Sonuç bulunamadı.</CommandEmpty>
              <CommandGroup>
                {stocks.map((s) => (
                  <CommandItem
                    key={s.symbol}
                    value={`${s.symbol} ${s.name}`}
                    onSelect={() => {
                      onChange(s.symbol);
                      setOpen(false);
                    }}
                  >
                    <Check className={`mr-2 h-4 w-4 ${value === s.symbol ? 'opacity-100' : 'opacity-0'}`} />
                    <span className="font-mono font-semibold">{s.symbol}</span>
                    <span className="ml-2 text-muted-foreground">{s.name}</span>
                  </CommandItem>
                ))}
              </CommandGroup>
            </CommandList>
          </Command>
        </PopoverContent>
      </Popover>
    </div>
  );
}
