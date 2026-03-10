import type { ReactNode } from 'react';
import { Menu, X } from 'lucide-react';

interface Props {
  sidebar: ReactNode;
  children: ReactNode;
  sidebarOpen: boolean;
  onSidebarToggle: (open: boolean) => void;
}

export function Dashboard({ sidebar, children, sidebarOpen, onSidebarToggle }: Props) {
  return (
    <div className="flex h-screen overflow-hidden bg-background">
      {/* Mobile hamburger button */}
      <button
        onClick={() => onSidebarToggle(true)}
        className="fixed top-3 left-3 z-40 flex h-10 w-10 items-center justify-center rounded-lg bg-card border border-border md:hidden"
      >
        <Menu className="h-5 w-5" />
      </button>

      {/* Mobile overlay */}
      {sidebarOpen && (
        <div
          className="fixed inset-0 z-40 bg-black/60 md:hidden"
          onClick={() => onSidebarToggle(false)}
        />
      )}

      {/* Sidebar */}
      <div
        className={`
          fixed inset-y-0 left-0 z-50 w-80 transform transition-transform duration-200 ease-in-out
          md:relative md:translate-x-0
          ${sidebarOpen ? 'translate-x-0' : '-translate-x-full'}
        `}
      >
        {/* Mobile close button */}
        <button
          onClick={() => onSidebarToggle(false)}
          className="absolute top-3 right-3 z-10 flex h-8 w-8 items-center justify-center rounded-lg bg-muted/80 md:hidden"
        >
          <X className="h-4 w-4" />
        </button>
        {sidebar}
      </div>

      <main className="flex-1 overflow-y-auto p-4 pt-16 md:p-6 md:pt-6">
        {children}
      </main>
    </div>
  );
}
