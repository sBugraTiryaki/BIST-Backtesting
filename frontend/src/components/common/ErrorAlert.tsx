import { AlertCircle } from 'lucide-react';
import { Card, CardContent } from '@/components/ui/card';

interface Props {
  message: string;
}

export function ErrorAlert({ message }: Props) {
  return (
    <Card className="border-destructive/50 bg-destructive/10">
      <CardContent className="flex items-center gap-2 p-4">
        <AlertCircle className="h-4 w-4 text-destructive" />
        <p className="text-sm text-destructive">{message}</p>
      </CardContent>
    </Card>
  );
}
