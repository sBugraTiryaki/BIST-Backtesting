import { useState } from 'react';
import { Popover, PopoverContent, PopoverTrigger } from '@/components/ui/popover';
import { Command, CommandEmpty, CommandGroup, CommandInput, CommandItem, CommandList } from '@/components/ui/command';
import { Button } from '@/components/ui/button';
import { Label } from '@/components/ui/label';
import { ChevronsUpDown, Check, Search } from 'lucide-react';
import type { StockInfo } from '../../types';

interface Props {
  stocks: StockInfo[];
  value: string;
  onChange: (symbol: string) => void;
}

export function StockSelector({ stocks, value, onChange }: Props) {
  const [open, setOpen] = useState(false);
  const [search, setSearch] = useState('');
  const selected = stocks.find((s) => s.symbol === value);

  const searchUpper = search.trim().toUpperCase();
  const isCustomSymbol = searchUpper.length >= 2 && !stocks.some(
    (s) => s.symbol === searchUpper || s.name.toUpperCase().includes(searchUpper)
  );

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
            ) : value ? (
              <span>
                <span className="font-semibold text-green-400">{value}</span>
                <span className="ml-2 text-muted-foreground">Özel sembol</span>
              </span>
            ) : (
              <span className="text-muted-foreground">Hisse seçin...</span>
            )}
            <ChevronsUpDown className="ml-2 h-4 w-4 shrink-0 opacity-50" />
        </PopoverTrigger>
        <PopoverContent className="w-[280px] p-0" align="start">
          <Command>
            <CommandInput placeholder="Ara veya sembol yaz..." value={search} onValueChange={setSearch} />
            <CommandList>
              <CommandEmpty>
                {searchUpper.length >= 2 ? (
                  <button
                    className="flex w-full items-center gap-2 px-2 py-1.5 text-sm cursor-pointer hover:bg-accent rounded"
                    onClick={() => {
                      onChange(searchUpper);
                      setSearch('');
                      setOpen(false);
                    }}
                  >
                    <Search className="h-4 w-4 text-green-400" />
                    <span className="font-mono font-semibold text-green-400">{searchUpper}</span>
                    <span className="text-muted-foreground">dene</span>
                  </button>
                ) : (
                  'Sonuç bulunamadı.'
                )}
              </CommandEmpty>
              <CommandGroup>
                {isCustomSymbol && (
                  <CommandItem
                    value={`_custom_${searchUpper}`}
                    onSelect={() => {
                      onChange(searchUpper);
                      setSearch('');
                      setOpen(false);
                    }}
                  >
                    <Search className="mr-2 h-4 w-4 text-green-400" />
                    <span className="font-mono font-semibold text-green-400">{searchUpper}</span>
                    <span className="ml-2 text-muted-foreground">dene</span>
                  </CommandItem>
                )}
                {stocks.map((s) => (
                  <CommandItem
                    key={s.symbol}
                    value={`${s.symbol} ${s.name}`}
                    onSelect={() => {
                      onChange(s.symbol);
                      setSearch('');
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
