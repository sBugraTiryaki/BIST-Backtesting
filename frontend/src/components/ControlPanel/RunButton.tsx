import { Button } from '@/components/ui/button';
import { Play, Loader2 } from 'lucide-react';

interface Props {
  onClick: () => void;
  loading: boolean;
  disabled: boolean;
}

export function RunButton({ onClick, loading, disabled }: Props) {
  return (
    <Button
      onClick={onClick}
      disabled={disabled || loading}
      className="w-full bg-green-600 text-white hover:bg-green-500 shadow-lg shadow-green-600/20"
      size="lg"
    >
      {loading ? (
        <>
          <Loader2 className="mr-2 h-4 w-4 animate-spin" />
          Hesaplanıyor...
        </>
      ) : (
        <>
          <Play className="mr-2 h-4 w-4" />
          Backtest Başlat
        </>
      )}
    </Button>
  );
}
