# BIST-Backtesting - Claude Code Rehberi

## Proje Ozeti
Borsa Istanbul (BIST) hisse senetleri icin web tabanli backtesting araci.
Hedef kitle: Kod bilmeyen Turk trader/yatirimcilar.

## Teknoloji Stack
- **Backend**: FastAPI + Python 3.12, pandas, numpy, yfinance
- **Frontend**: React + TypeScript + Vite, Tailwind CSS, TradingView Lightweight Charts
- **Deploy**: Docker Compose + Coolify (Hetzner)

## Komutlar

### Backend
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
pytest tests/ -v
```

### Frontend
```bash
cd frontend
npm install
npm run dev      # Development server (port 5173)
npm run build    # Production build
npm run preview  # Preview production build
```

### Docker
```bash
docker compose up --build        # Tum servisleri baslat
docker compose up backend -d     # Sadece backend
docker compose down              # Durdur
```

## Mimari Kararlar

### vectorbt Kullanmiyoruz
- Acik kaynak versiyonu bakimsiz (0.28.4'te dondu)
- 10 strateji icin bile overkill, bellek yogun
- Saf pandas/numpy ile indikatorler 10-20 satir kodla yazilabilir

### Indikatorler Saf pandas/numpy
- ta-lib Docker'da C derleme sorunu yaratir
- pandas-ta gereksiz bagimllik
- Formulleri elle yazmak ogretici ve hafif

### Cache: Dosya bazli JSON
- Veritabani gereksiz — tek kullanici senaryosu
- 4 saat TTL ile yfinance rate limit korunur
- backend/cache/ dizininde saklanir (.gitignore'da)

### State: useReducer + Context
- Tek sayfa uygulama, Redux/Zustand gereksiz
- useReducer backtest state'i icin yeterli

## Kod Kurallari
- Backend: Python 3.12, type hint kullan, Pydantic v2
- Frontend: TypeScript strict mode, fonksiyonel componentler
- UI dili: Turkce
- Commit mesajlari: Turkce
- Degisken/fonksiyon isimleri: Ingilizce (Python/TS standardi)
- Dosya/klasor isimleri: Ingilizce, snake_case (backend), camelCase (frontend)

## Hisse Listesi
Dropdown'da BIST-100 (config.py'de 100 hisse) gosterilir. Kullanici BIST-100 disinda herhangi bir sembol de yazabilir — backend `SEMBOL.IS` formatinda yfinance'a sorar.

### Hybrid Veri Kaynagi ve Split Duzeltme
yfinance BIST hisselerinde bedelsiz sermaye artirimlarini (split) guvenilir sekilde duzeltmiyor. Bu nedenle hybrid yaklasim kullaniliyor:
- **yfinance**: OHLCV verisi (Open dahil candlestick icin gerekli)
- **Is Yatirim API**: `HGDG_KAPANIS` split-adjusted surekli seri (referans)
- `data_fetcher.py`'de `_adjust_with_isyatirim()`: yfinance Close / HGDG Close oranini karsilastirir, %5'ten fazla sapma varsa split hatasi tespit eder ve pre-split OHLC fiyatlari median oranla boler
- Is Yatirim'da Open verisi yok, bu yuzden yfinance'tan alinir ve ayni oranla duzeltilir

## Onemli Dosyalar
- `backend/app/config.py` — BIST-100 listesi, cache ayarlari
- `backend/app/services/data_fetcher.py` — yfinance + Is Yatirim hybrid veri cekme, split duzeltme
- `backend/app/services/backtester.py` — Portfoy simulasyon motoru
- `backend/app/routers/backtest.py` — Strateji registry, STRATEGIES dict, STRATEGY_DEFINITIONS listesi
- `backend/app/strategies/` — 10 strateji implementasyonu (BaseStrategy inherit eder)
- `frontend/src/hooks/useBacktest.ts` — Ana state yonetimi
- `frontend/src/hooks/useChartZoom.ts` — Platform-aware Cmd/Ctrl+scroll zoom
- `frontend/src/components/Charts/PriceChart.tsx` — Candlestick grafik
- `frontend/src/components/Charts/IndicatorChart.tsx` — Osilatör grafigi (overlay=False stratejiler icin)
- `frontend/src/components/Results/MetricsPanel.tsx` — Performans kartlari

## Backtest Mantigi
- Baslangic sermayesi: 100.000 TL
- Long-only, AL sinyalinde tum nakitle al, SAT sinyalinde tum hisseyi sat
- Fiyat: close (kapanis)
- Equity curve: her gun nakit + (hisse * close)
