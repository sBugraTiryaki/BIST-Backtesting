import { useEffect, useRef } from 'react';
import { createChart, type IChartApi, ColorType, AreaSeries } from 'lightweight-charts';
import type { EquityPoint } from '../../types';
import { useChartZoom } from '../../hooks/useChartZoom';
import { ChartZoomHint } from './ChartZoomHint';

interface Props {
  data: EquityPoint[];
  onChartReady?: (chart: IChartApi) => void;
}

export function EquityCurve({ data, onChartReady }: Props) {
  const wrapperRef = useRef<HTMLDivElement>(null);
  const containerRef = useRef<HTMLDivElement>(null);
  const chartRef = useRef<IChartApi | null>(null);
  const showHint = useChartZoom(wrapperRef, chartRef);

  useEffect(() => {
    if (!containerRef.current || data.length === 0) return;

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
      height: 200,
      handleScroll: { mouseWheel: false, vertTouchDrag: false },
      handleScale: { mouseWheel: false, pinch: true },
      timeScale: { borderColor: 'rgba(255,255,255,0.1)' },
      rightPriceScale: { borderColor: 'rgba(255,255,255,0.1)' },
    });
    chartRef.current = chart;

    // v5 API
    const areaSeries = chart.addSeries(AreaSeries, {
      topColor: 'rgba(34, 197, 94, 0.4)',
      bottomColor: 'rgba(34, 197, 94, 0.0)',
      lineColor: '#22c55e',
      lineWidth: 2,
    });

    areaSeries.setData(
      data.map((d) => ({ time: d.date, value: d.value }))
    );

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
  }, [data]);

  return (
    <div ref={wrapperRef} className="relative">
      <div ref={containerRef} className="rounded-lg" />
      <ChartZoomHint visible={showHint} />
    </div>
  );
}
