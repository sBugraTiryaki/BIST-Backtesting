# Katkıda Bulunma Rehberi

BIST-Backtesting projesine katkıda bulunmak istediğiniz için teşekkürler! Bu rehber, katkıda bulunma sürecini açıklar.

## Başlamadan Önce

1. Projeyi fork'layın
2. Kendi branch'inizi oluşturun: `git checkout -b ozellik/yeni-strateji`
3. Değişikliklerinizi commit'leyin
4. Pull request açın

## Geliştirme Ortamı

### Backend
```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

### Testler
```bash
cd backend
pytest tests/ -v
```

## Kod Kuralları

### Genel
- Değişken ve fonksiyon isimleri **İngilizce** (Python/TypeScript standardı)
- UI metinleri **Türkçe**
- Commit mesajları **Türkçe**

### Backend (Python)
- Python 3.12+ özellikleri kullanılabilir
- Type hint zorunlu
- Pydantic v2 modelleri
- Dosya isimleri: `snake_case`

### Frontend (TypeScript)
- TypeScript strict mode
- Fonksiyonel componentler (class component yok)
- shadcn/ui componentleri tercih edilir
- Dosya isimleri: `PascalCase` (componentler), `camelCase` (hook/util)

## Yeni Strateji Ekleme

1. `backend/app/strategies/` altında yeni dosya oluşturun
2. `BaseStrategy` sınıfını miras alın (`base.py`)
3. `generate_signals()` ve `get_indicator_data()` metodlarını implement edin
4. `backend/app/routers/backtest.py` dosyasında `STRATEGIES` ve `STRATEGY_DEFINITIONS`'a ekleyin
5. Test yazın: `backend/tests/test_strategies.py`

```python
# Örnek: backend/app/strategies/yeni_strateji.py
from app.strategies.base import BaseStrategy

class YeniStrateji(BaseStrategy):
    def generate_signals(self, df, params):
        # signal kolonu: 1 = AL, -1 = SAT, 0 = bekle
        ...
        return df

    def get_indicator_data(self, df, params):
        # Grafik üzerinde gösterilecek indikatörler
        return [{"name": "İndikatör", "values": [...]}]
```

## Pull Request Süreci

1. Değişikliklerinizin testlerden geçtiğinden emin olun
2. Açıklayıcı bir PR başlığı ve açıklaması yazın
3. Ekran görüntüsü ekleyin (UI değişiklikleri için)
4. Review bekleyin

## Sorun Bildirme

GitHub Issues üzerinden sorun bildirebilirsiniz. Lütfen şunları ekleyin:
- Sorunun açık tanımı
- Yeniden üretme adımları
- Beklenen ve gerçekleşen davranış
- Ekran görüntüsü (varsa)

## Lisans

Katkıda bulunarak, kodunuzun [MIT Lisansı](LICENSE) altında yayınlanmasını kabul etmiş olursunuz.
