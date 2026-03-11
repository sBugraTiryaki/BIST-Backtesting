import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import type { TradeRecord } from '../../types';

interface Props {
  trades: TradeRecord[];
}

const fmt = new Intl.NumberFormat('tr-TR', { minimumFractionDigits: 2, maximumFractionDigits: 2 });

function fmtDate(dateStr: string) {
  const [y, m, d] = dateStr.split('-');
  return `${d}.${m}.${y}`;
}

export function TradeTable({ trades }: Props) {
  if (trades.length === 0) {
    return (
      <Card>
        <CardContent className="py-6 text-center text-sm text-muted-foreground">
          Tamamlanmış işlem bulunamadı.
        </CardContent>
      </Card>
    );
  }

  return (
    <Card>
      <CardHeader className="pb-3">
        <CardTitle className="text-sm font-medium text-muted-foreground">İşlem Geçmişi</CardTitle>
      </CardHeader>
      <CardContent className="p-0">
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead>Giriş Tarihi</TableHead>
              <TableHead>Çıkış Tarihi</TableHead>
              <TableHead className="text-right">Giriş Fiyatı</TableHead>
              <TableHead className="text-right">Çıkış Fiyatı</TableHead>
              <TableHead className="text-right">Kâr/Zarar (₺)</TableHead>
              <TableHead className="text-right">Getiri (%)</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {trades.map((t, i) => (
              <TableRow key={i}>
                <TableCell className="font-mono text-xs">{fmtDate(t.entry_date)}</TableCell>
                <TableCell className="font-mono text-xs">{fmtDate(t.exit_date)}</TableCell>
                <TableCell className="text-right tabular-nums">{fmt.format(t.entry_price)}</TableCell>
                <TableCell className="text-right tabular-nums">{fmt.format(t.exit_price)}</TableCell>
                <TableCell className={`text-right font-medium tabular-nums ${t.pnl >= 0 ? 'text-green-400' : 'text-red-400'}`}>
                  {fmt.format(t.pnl)}
                </TableCell>
                <TableCell className={`text-right font-medium tabular-nums ${t.return_pct >= 0 ? 'text-green-400' : 'text-red-400'}`}>
                  {fmt.format(t.return_pct)}%
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </CardContent>
    </Card>
  );
}
