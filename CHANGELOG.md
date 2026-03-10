# Değişiklik Günlüğü

Bu proje [Semantic Versioning](https://semver.org/) kullanır.

## [0.1.0] - 2026-03-10

### Eklendi
- FastAPI backend: BIST-100 hisse listesi, fiyat verisi ve backtest API
- 3 teknik analiz stratejisi: SMA Kesişim, RSI, MACD
- Portföy simülasyon motoru (long-only, tam pozisyon)
- 9 performans metriği: toplam getiri, Sharpe oranı, maks. düşüş, kazanma oranı vb.
- yfinance ile Yahoo Finance entegrasyonu (4 saatlik dosya cache)
- React + TypeScript frontend (Vite, Tailwind CSS v4, shadcn/ui)
- TradingView Lightweight Charts v5 ile mum grafiği ve indikatör overlay
- Senkronize fiyat ve portföy grafikleri
- AL/SAT sinyal işaretleri (ok + etiket)
- Ayarlanabilir strateji parametreleri (slider)
- Tarih aralığı seçici (hazır butonlar: 6A, 1Y, 2Y, 5Y)
- Aranabilir hisse seçici (combobox)
- İşlem geçmişi tablosu
- Dark tema arayüz
- Türkçe arayüz ve metrikler
- Docker Compose yapılandırması (backend + frontend)
- Backend unit testleri (strateji sinyalleri, backtester)
- Favicon ve Open Graph meta etiketleri
