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
- 3 strateji icin overkill, bellek yogun
- Saf pandas/numpy ile SMA/RSI/MACD 10-15 satir kodla yazilabilir

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

## BIST-100 Hisse Listesi
Hardcoded config.py'de (30 BIST-30 + 69 ek = 99 hisse). Yahoo Finance suffix: `.IS` (ornek: THYAO.IS)

## Onemli Dosyalar
- `backend/app/config.py` — BIST-100 listesi, cache ayarlari
- `backend/app/services/backtester.py` — Portfoy simulasyon motoru
- `backend/app/strategies/` — Strateji implementasyonlari
- `frontend/src/hooks/useBacktest.ts` — Ana state yonetimi
- `frontend/src/components/Charts/PriceChart.tsx` — Candlestick grafik

## Backtest Mantigi
- Baslangic sermayesi: 100.000 TL
- Long-only, AL sinyalinde tum nakitle al, SAT sinyalinde tum hisseyi sat
- Fiyat: close (kapanis)
- Equity curve: her gun nakit + (hisse * close)
