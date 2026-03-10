import type { ReactNode } from 'react';

interface Props {
  sidebar: ReactNode;
  children: ReactNode;
}

export function Dashboard({ sidebar, children }: Props) {
  return (
    <div className="flex h-screen overflow-hidden bg-background">
      {sidebar}
      <main className="flex-1 overflow-y-auto p-6">
        {children}
      </main>
    </div>
  );
}
