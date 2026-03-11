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

## Hisse Listesi
Dropdown'da BIST-100 (config.py'de 100 hisse) gosterilir. Kullanici BIST-100 disinda herhangi bir sembol de yazabilir — backend `SEMBOL.IS` formatinda yfinance'a sorar.

### yfinance Stock Split Sorunu
Yahoo Finance BIST hisselerinde split duzeltmesini guvenilir sekilde uygulamiyor. `auto_adjust=True` sadece temettu duzeltir, split'i duzeltmez. Bu nedenle `data_fetcher.py`'de `_adjust_for_splits()` fonksiyonu var: `yf.Ticker().splits` ile split bilgisini alip fiyat verisindeki kirillma noktasini tespit ederek pre-split fiyatlari orana boler. Is Yatirim (isyatirimhisse) verisiyle dogrulanmistir.

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
