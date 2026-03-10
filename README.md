# BIST-Backtesting — Strateji Test Aracı

Borsa İstanbul (BIST) hisse senetleri için web tabanlı backtesting aracı. Kod yazmadan teknik analiz stratejilerini geçmiş veriler üzerinde test edin.

<!-- TODO: Ekran görüntüsü ekle -->
<!-- ![BIST-Backtesting Ekran Görüntüsü](docs/screenshot.png) -->

## Özellikler

- **3 Hazır Strateji**: SMA Kesişim, RSI, MACD
- **BIST-30 Hisse Desteği**: Türkiye'nin en likit 30 hissesi
- **İnteraktif Grafikler**: TradingView Lightweight Charts ile mum grafiği, indikatör overlay ve AL/SAT sinyalleri
- **Senkronize Grafikler**: Fiyat ve portföy grafikleri eşanlı hareket eder
- **Detaylı Metrikler**: Toplam getiri, Sharpe oranı, maksimum düşüş, kazanma oranı ve daha fazlası
- **İşlem Geçmişi**: Her alışverişin detaylı tablosu
- **Ayarlanabilir Parametreler**: Slider'lar ile strateji parametrelerini değiştirin
- **Dark Tema**: Profesyonel, göz yormayan karanlık arayüz
- **Türkçe Arayüz**: Tüm arayüz ve metrikler Türkçe

## Teknoloji Stack

### Backend
- **FastAPI** + Python 3.12
- **pandas** / **numpy** — indikatör hesaplamaları
- **yfinance** — BIST fiyat verileri (Yahoo Finance)
- **Pydantic v2** — veri doğrulama

### Frontend
- **React 19** + TypeScript
- **Vite** — hızlı geliştirme ve build
- **Tailwind CSS v4** + **shadcn/ui** — modern, tutarlı arayüz
- **TradingView Lightweight Charts v5** — profesyonel finansal grafikler
- **date-fns** — tarih formatlama (Türkçe locale)

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

1. Sol panelden **hisse senedi** seçin (örneğin THYAO - Türk Hava Yolları)
2. **Tarih aralığı** belirleyin (hazır butonlar: 6A, 1Y, 2Y, 5Y)
3. **Strateji** seçin (SMA Kesişim, RSI veya MACD)
4. Strateji **parametrelerini** slider'lar ile ayarlayın
5. **Başlangıç sermayesi** girin (varsayılan: 100.000 ₺)
6. **Backtest Başlat** butonuna basın
7. Sonuçları inceleyin: grafikler, metrikler ve işlem tablosu

## Stratejiler

### SMA Kesişim
Kısa ve uzun hareketli ortalama kesişimi ile alış/satış sinyali üretir.
- **Kısa Periyot**: 5-50 (varsayılan: 20)
- **Uzun Periyot**: 10-200 (varsayılan: 50)

### RSI (Relative Strength Index)
Aşırı alım/satım bölgelerinde alış/satış sinyali üretir.
- **RSI Periyot**: 5-30 (varsayılan: 14)
- **Aşırı Alım**: 60-90 (varsayılan: 70)
- **Aşırı Satım**: 10-40 (varsayılan: 30)

### MACD (Moving Average Convergence Divergence)
MACD ve sinyal çizgisi kesişimi ile trend takibi yapar.
- **Hızlı EMA**: 5-20 (varsayılan: 12)
- **Yavaş EMA**: 15-40 (varsayılan: 26)
- **Sinyal Periyot**: 5-15 (varsayılan: 9)

## Performans Metrikleri

| Metrik | Açıklama |
|--------|----------|
| Toplam Getiri | Strateji toplam kâr/zarar yüzdesi |
| Al-Tut Getirisi | Hisseyi alıp bekletmenin getirisi (karşılaştırma) |
| Maks. Düşüş | Zirveden en büyük gerileme yüzdesi |
| Sharpe Oranı | Risk-getiri dengesi (yıllık, √252) |
| Kazanma Oranı | Kârlı işlem yüzdesi |
| İşlem Sayısı | Toplam tamamlanan işlem |
| Kâr Faktörü | Toplam kâr / toplam zarar |
| Ort. İşlem Getirisi | İşlem başına ortalama kâr/zarar |

## Proje Yapısı

```
BIST-Backtesting/
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI uygulama, CORS, router
│   │   ├── config.py            # BIST-30 listesi, cache ayarları
│   │   ├── routers/
│   │   │   ├── stocks.py        # GET /api/stocks
│   │   │   └── backtest.py      # POST /api/backtest, GET /api/strategies
│   │   ├── models/
│   │   │   ├── requests.py      # Pydantic request modelleri
│   │   │   └── responses.py     # Pydantic response modelleri
│   │   ├── services/
│   │   │   ├── data_fetcher.py  # yfinance wrapper + dosya cache
│   │   │   ├── backtester.py    # Portföy simülasyon motoru
│   │   │   └── metrics.py       # Performans metrikleri
│   │   └── strategies/
│   │       ├── base.py          # Soyut strateji arayüzü
│   │       ├── sma_crossover.py # SMA Kesişim
│   │       ├── rsi.py           # RSI
│   │       └── macd.py          # MACD
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
│   │   ├── hooks/               # useBacktest, useStocks
│   │   ├── api/client.ts        # API istekleri
│   │   └── types/index.ts       # TypeScript tipleri
│   ├── Dockerfile
│   └── nginx.conf
├── docker-compose.yml
├── CLAUDE.md
├── CONTRIBUTING.md
├── CHANGELOG.md
└── LICENSE (MIT)
```

## API

Backend Swagger dokümantasyonu: `http://localhost:8000/docs`

| Endpoint | Metot | Açıklama |
|----------|-------|----------|
| `/api/stocks` | GET | BIST-30 hisse listesi |
| `/api/strategies` | GET | Mevcut stratejiler ve parametreleri |
| `/api/backtest` | POST | Backtest çalıştır |

## Backtest Mantığı

- **Başlangıç sermayesi**: Varsayılan 100.000 ₺
- **Pozisyon**: Long-only (sadece alış)
- **AL sinyali**: Tüm nakit ile kapanış fiyatından hisse al
- **SAT sinyali**: Tüm hisseleri kapanış fiyatından sat
- **Equity curve**: Her gün portföy değeri = nakit + (hisse adedi × kapanış)
- **Veri**: yfinance üzerinden Yahoo Finance (4 saatlik cache)

## Lisans

Bu proje [MIT Lisansı](LICENSE) ile lisanslanmıştır.
