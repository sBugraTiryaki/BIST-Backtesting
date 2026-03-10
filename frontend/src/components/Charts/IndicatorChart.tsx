import { useEffect, useRef } from 'react';
import { createChart, type IChartApi, ColorType, LineSeries } from 'lightweight-charts';
import type { IndicatorData } from '../../types';

interface Props {
  indicators: IndicatorData[];
  onChartReady?: (chart: IChartApi) => void;
}

const COLORS = [
  '#3b82f6',                    // blue — ana çizgi
  'rgba(239,68,68,0.5)',        // red — seviye çizgisi
  'rgba(34,197,94,0.5)',        // green — seviye çizgisi
  'rgba(245,158,11,0.7)',       // amber
];

export function IndicatorChart({ indicators, onChartReady }: Props) {
  const containerRef = useRef<HTMLDivElement>(null);
  const chartRef = useRef<IChartApi | null>(null);

  useEffect(() => {
    if (!containerRef.current || indicators.length === 0) return;

    const chart = createChart(containerRef.current, {
      layout: {
        background: { type: ColorType.Solid, color: 'transparent' },
        textColor: '#9ca3af',
      },
      grid: {
        vertLines: { color: 'rgba(255,255,255,0.06)' },
        horzLines: { color: 'rgba(255,255,255,0.06)' },
      },
      width: containerRef.current.clientWidth,
      height: 150,
      timeScale: { borderColor: 'rgba(255,255,255,0.1)' },
      rightPriceScale: { borderColor: 'rgba(255,255,255,0.1)' },
    });
    chartRef.current = chart;

    indicators.forEach((ind, i) => {
      const isLevel = ind.name.startsWith('Aşırı');
      const lineSeries = chart.addSeries(LineSeries, {
        color: COLORS[i % COLORS.length],
        lineWidth: isLevel ? 1 : 2,
        lineStyle: isLevel ? 2 : 0, // 2 = dashed
        title: ind.name,
        lastValueVisible: !isLevel,
        priceLineVisible: false,
        crosshairMarkerVisible: !isLevel,
      });
      lineSeries.setData(
        ind.values.map((v) => ({ time: v.date, value: v.value }))
      );
    });

    chart.timeScale().fitContent();
    onChartReady?.(chart);

    const handleResize = () => {
      if (containerRef.current) {
        chart.applyOptions({ width: containerRef.current.clientWidth });
      }
    };
    window.addEventListener('resize', handleResize);

    return () => {
      window.removeEventListener('resize', handleResize);
      chart.remove();
      chartRef.current = null;
    };
  }, [indicators]);

  return <div ref={containerRef} className="rounded-lg" />;
}
