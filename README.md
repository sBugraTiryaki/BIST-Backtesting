# BIST-Backtesting — Strateji Test Aracı

BIST hisse senetleri için 10 popüler stratejiyi al-unut (buy & hold) sistemiyle karşılaştıran web tabanlı backtesting aracı. Kod yazmadan teknik analiz stratejilerini geçmiş veriler üzerinde test edin.

<!-- TODO: Ekran görüntüsü ekle -->
<!-- ![BIST-Backtesting Ekran Görüntüsü](docs/screenshot.png) -->

## Özellikler

- **10 Hazır Strateji**: SMA Kesişim, RSI, MACD, Bollinger Bantları, Stochastic, Supertrend, EMA Kesişim, Parabolic SAR, Ichimoku Bulutu, Williams %R
- **Eğitici Açıklamalar**: Her strateji ve parametre için Türkçe açıklama — kullanırken öğrenin
- **BIST-100 + Serbest Sembol**: 100 hazır hisse ve istediğiniz BIST sembolünü yazabilme
- **İnteraktif Grafikler**: TradingView Lightweight Charts ile mum grafiği, indikatör overlay ve AL/SAT sinyalleri
- **Senkronize Grafikler**: Fiyat, osilatör ve portföy grafikleri eşanlı hareket eder
- **Performans Karşılaştırması**: Strateji getirisi vs al-unut getirisi yan yana
- **Ayarlanabilir Parametreler**: Slider'lar ile strateji parametrelerini değiştirin, açıklamalı
- **Hybrid Veri Kaynağı**: yfinance OHLCV + İş Yatırım split-düzeltme referansı
- **Mobil Uyumlu**: Responsive tasarım, hamburger menü, touch-friendly grafikler
- **Dark Tema**: Profesyonel, göz yormayan karanlık arayüz
- **Türkçe Arayüz**: Tüm arayüz, metrikler ve tarihler Türkçe

## Stratejiler

| # | Strateji | Tip | Açıklama |
|---|----------|-----|----------|
| 1 | **SMA Kesişim** | Trend Takip | Kısa ve uzun hareketli ortalama kesişimi |
| 2 | **RSI** | Momentum | Aşırı alım/satım bölgelerinde dönüş sinyali |
| 3 | **MACD** | Trend + Momentum | MACD ve sinyal çizgisi kesişimi |
| 4 | **Bollinger Bantları** | Mean Reversion | Fiyatın istatistiksel bantlara göre konumu |
| 5 | **Stochastic Osilatör** | Momentum | %K/%D kesişimi ile dönüş noktaları |
| 6 | **Supertrend** | Trend Takip | ATR bazlı trend takip (Matriks'te popüler) |
| 7 | **EMA Kesişim** | Trend Takip | Üstel hareketli ortalama kesişimi (SMA'dan hızlı) |
| 8 | **Parabolic SAR** | Trend Takip | Dur ve Dönüş noktaları (Wilder formülü) |
| 9 | **Ichimoku Bulutu** | Trend + Momentum | Tenkan/Kijun kesişimi + bulut filtresi |
| 10 | **Williams %R** | Momentum | Fiyatın dönem aralığındaki konumu |

## Teknoloji Stack

### Backend
- **FastAPI** + Python 3.12
- **pandas** / **numpy** — indikatör hesaplamaları (saf, ta-lib bağımlılığı yok)
- **yfinance** — BIST OHLCV verileri
- **İş Yatırım API** — split/bedelsiz düzeltme referansı
- **Pydantic v2** — veri doğrulama

### Frontend
- **React 19** + TypeScript
- **Vite** — hızlı geliştirme ve build
- **Tailwind CSS v4** + **shadcn/ui** — modern, tutarlı arayüz
- **TradingView Lightweight Charts v5** — profesyonel finansal grafikler

### Altyapı
- **Docker Compose** — tek komutla çalıştırma
- **Nginx** — frontend static dosya sunumu

## Hızlı Başlangıç

### Önkoşullar
- Python 3.12+
- Node.js 18+
- npm

### Lokal Geliştirme

**Backend:**
```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

**Frontend:**
```bash
cd frontend
npm install
npm run dev
```

Tarayıcıda `http://localhost:5173` adresini açın.

### Docker ile Çalıştırma

```bash
docker compose up --build
```

Tarayıcıda `http://localhost:3000` adresini açın.

## Kullanım

1. Sol panelden **hisse senedi** seçin veya yazın
2. **Tarih aralığı** belirleyin
3. **Strateji** seçin — açıklamayı okuyarak nasıl çalıştığını öğrenin
4. **Parametreleri** slider'lar ile ayarlayın — her birinin ne yaptığı açıklanır
5. **Backtest Başlat** butonuna basın
6. Sonuçları inceleyin: strateji getirisi vs al-unut karşılaştırması, grafikler ve işlem tablosu

## Veri Kaynağı ve Split Düzeltme

Fiyat verisi iki kaynağın birleşimiyle oluşturulur:

| | yfinance | İş Yatırım |
|---|---------|-----------|
| Open | ✅ | ❌ |
| High/Low/Close | ✅ | ✅ |
| Split düzeltme | ❌ Güvenilmez | ✅ Doğru |

**Neden hybrid?** yfinance BIST hisselerinde bedelsiz sermaye artırımlarını doğru düzeltmiyor. İş Yatırım'ın `HGDG_KAPANIS` verisi split-adjusted sürekli seri sağlıyor ama Open fiyatı yok. İkisi birlikte kullanılarak hem candlestick grafik çizilebiliyor hem de split düzeltmesi doğru yapılıyor.

## Backtest Mantığı

- **Başlangıç sermayesi**: Varsayılan 100.000 ₺
- **Pozisyon**: Long-only (sadece alış)
- **AL sinyali**: Tüm nakit ile kapanış fiyatından hisse al
- **SAT sinyali**: Tüm hisseleri kapanış fiyatından sat
- **Equity curve**: Her gün portföy değeri = nakit + (hisse adedi × kapanış)
- **Veri cache**: 4 saatlik dosya bazlı JSON cache

## Proje Yapısı

```
BIST-Backtesting/
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI uygulama, CORS, router
│   │   ├── config.py            # BIST-100 listesi, cache ayarları
│   │   ├── routers/
│   │   │   ├── stocks.py        # GET /api/stocks
│   │   │   └── backtest.py      # POST /api/backtest, GET /api/strategies
│   │   ├── models/
│   │   │   ├── requests.py      # Pydantic request modelleri
│   │   │   └── responses.py     # Pydantic response modelleri
│   │   ├── services/
│   │   │   ├── data_fetcher.py  # yfinance + İş Yatırım hybrid veri
│   │   │   ├── backtester.py    # Portföy simülasyon motoru
│   │   │   └── metrics.py       # Performans metrikleri
│   │   └── strategies/          # 10 strateji implementasyonu
│   │       ├── base.py          # Soyut strateji arayüzü
│   │       ├── sma_crossover.py # SMA Kesişim
│   │       ├── rsi.py           # RSI
│   │       ├── macd.py          # MACD
│   │       ├── bollinger_bands.py
│   │       ├── stochastic.py
│   │       ├── supertrend.py
│   │       ├── ema_crossover.py
│   │       ├── parabolic_sar.py
│   │       ├── ichimoku.py
│   │       └── williams_r.py
│   ├── tests/
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── App.tsx
│   │   ├── components/
│   │   │   ├── Charts/          # TradingView grafik bileşenleri
│   │   │   ├── ControlPanel/    # Sol panel kontrolleri
│   │   │   ├── Results/         # Metrik kartları ve işlem tablosu
│   │   │   └── common/          # Spinner, ErrorAlert
│   │   ├── hooks/               # useBacktest, useStocks, useChartZoom
│   │   ├── api/client.ts        # API istekleri
│   │   └── types/index.ts       # TypeScript tipleri
│   ├── Dockerfile
│   └── nginx.conf
├── docker-compose.yaml
├── CLAUDE.md
└── LICENSE (MIT)
```

## API

Backend Swagger dokümantasyonu: `http://localhost:8000/docs`

| Endpoint | Metot | Açıklama |
|----------|-------|----------|
| `/api/stocks` | GET | BIST-100 hisse listesi |
| `/api/strategies` | GET | 10 strateji ve parametreleri |
| `/api/backtest` | POST | Backtest çalıştır |

## Lisans

Bu proje [MIT Lisansı](LICENSE) ile lisanslanmıştır.
