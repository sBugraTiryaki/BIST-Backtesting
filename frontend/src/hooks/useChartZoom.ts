import { useEffect, useRef, useState } from 'react';
import type { IChartApi } from 'lightweight-charts';

const isTouchDevice = 'ontouchstart' in globalThis || navigator.maxTouchPoints > 0;
const isMac = !isTouchDevice && navigator.platform.toUpperCase().includes('MAC');

export const ZOOM_HINT = isTouchDevice
  ? 'Yakınlaştırmak için iki parmakla sıkıştırın'
  : isMac
    ? 'Yakınlaştırmak için ⌘ + scroll kullanın'
    : 'Yakınlaştırmak için Ctrl + scroll kullanın';

export function useChartZoom(
  wrapperRef: React.RefObject<HTMLDivElement | null>,
  chartRef: React.RefObject<IChartApi | null>
) {
  const [showHint, setShowHint] = useState(false);
  const hintTimeout = useRef<number>(undefined);

  useEffect(() => {
    const wrapper = wrapperRef.current;
    if (!wrapper || isTouchDevice) return;

    const handleWheel = (e: WheelEvent) => {
      const modifierPressed = isMac ? e.metaKey : e.ctrlKey;

      if (modifierPressed && chartRef.current) {
        e.preventDefault();
        const range = chartRef.current.timeScale().getVisibleLogicalRange();
        if (range) {
          const factor = e.deltaY > 0 ? 0.03 : -0.03;
          const width = range.to - range.from;
          chartRef.current.timeScale().setVisibleLogicalRange({
            from: range.from - factor * width / 2,
            to: range.to + factor * width / 2,
          });
        }
      } else {
        setShowHint(true);
        clearTimeout(hintTimeout.current);
        hintTimeout.current = window.setTimeout(() => setShowHint(false), 1500);
      }
    };

    wrapper.addEventListener('wheel', handleWheel, { passive: false });
    return () => {
      wrapper.removeEventListener('wheel', handleWheel);
      clearTimeout(hintTimeout.current);
    };
  }, [wrapperRef, chartRef]);

  return showHint;
}
