import { ZOOM_HINT } from '../../hooks/useChartZoom';

interface Props {
  visible: boolean;
}

export function ChartZoomHint({ visible }: Props) {
  if (!visible) return null;

  return (
    <div className="absolute inset-0 z-10 flex items-center justify-center pointer-events-none">
      <span className="text-xs text-white/90 bg-black/60 backdrop-blur-sm px-3 py-1.5 rounded-full">
        {ZOOM_HINT}
      </span>
    </div>
  );
}
