import { useEffect, useRef } from 'react';
import { createChart, type IChartApi, ColorType, CandlestickSeries, LineSeries, createSeriesMarkers } from 'lightweight-charts';
import type { OHLCV, IndicatorData, SignalPoint } from '../../types';
import { useChartZoom } from '../../hooks/useChartZoom';
import { ChartZoomHint } from './ChartZoomHint';

interface Props {
  priceData: OHLCV[];
  indicators: IndicatorData[];
  signals: SignalPoint[];
  onChartReady?: (chart: IChartApi) => void;
}

const INDICATOR_COLORS = [
  'rgba(59,130,246,0.7)',   // blue
  'rgba(245,158,11,0.7)',   // amber
  'rgba(168,85,247,0.7)',   // purple
  'rgba(236,72,153,0.7)',   // pink
];

export function PriceChart({ priceData, indicators, signals, onChartReady }: Props) {
  const wrapperRef = useRef<HTMLDivElement>(null);
  const containerRef = useRef<HTMLDivElement>(null);
  const chartRef = useRef<IChartApi | null>(null);
  const showHint = useChartZoom(wrapperRef, chartRef);

  useEffect(() => {
    if (!containerRef.current || priceData.length === 0) return;

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
      height: 400,
      handleScroll: { mouseWheel: false, vertTouchDrag: false },
      handleScale: { mouseWheel: false, pinch: true },
      timeScale: { borderColor: 'rgba(255,255,255,0.1)' },
      rightPriceScale: { borderColor: 'rgba(255,255,255,0.1)' },
      crosshair: {
        vertLine: { labelBackgroundColor: '#374151' },
        horzLine: { labelBackgroundColor: '#374151' },
      },
    });
    chartRef.current = chart;

    // Candlestick (v5 API)
    const candleSeries = chart.addSeries(CandlestickSeries, {
      upColor: '#22c55e',
      downColor: '#ef4444',
      borderDownColor: '#ef4444',
      borderUpColor: '#22c55e',
      wickDownColor: '#ef4444',
      wickUpColor: '#22c55e',
      lastValueVisible: false,
      priceLineVisible: false,
    });

    candleSeries.setData(
      priceData.map((d) => ({
        time: d.date,
        open: d.open,
        high: d.high,
        low: d.low,
        close: d.close,
      }))
    );

    // Indikatör overlay'leri (v5 API)
    indicators.forEach((ind, i) => {
      const lineSeries = chart.addSeries(LineSeries, {
        color: INDICATOR_COLORS[i % INDICATOR_COLORS.length],
        lineWidth: 2,
        title: ind.name,
        lastValueVisible: true,
        priceLineVisible: false,
        crosshairMarkerVisible: false,
      });
      lineSeries.setData(
        ind.values.map((v) => ({ time: v.date, value: v.value }))
      );
    });

    // AL/SAT sinyalleri
    const buyMarkers = signals
      .filter((s) => s.type === 'AL')
      .map((s) => ({
        time: s.date,
        position: 'belowBar' as const,
        color: '#22c55e',
        shape: 'arrowUp' as const,
        text: 'AL',
      }));

    const sellMarkers = signals
      .filter((s) => s.type === 'SAT')
      .map((s) => ({
        time: s.date,
        position: 'aboveBar' as const,
        color: '#ef4444',
        shape: 'arrowDown' as const,
        text: 'SAT',
      }));

    createSeriesMarkers(candleSeries, [...buyMarkers, ...sellMarkers].sort((a, b) => (a.time > b.time ? 1 : -1)));

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
  }, [priceData, indicators, signals]);

  return (
    <div ref={wrapperRef} className="relative">
      <div ref={containerRef} className="rounded-lg" />
      <ChartZoomHint visible={showHint} />
    </div>
  );
}
