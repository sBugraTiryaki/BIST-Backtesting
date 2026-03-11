from fastapi import APIRouter, HTTPException

from app.models.requests import BacktestRequest
from app.models.responses import (
    BacktestResponse,
    StrategiesResponse,
    StrategyInfo,
    StrategyParam,
)
from app.services.backtester import run_backtest
from app.services.data_fetcher import fetch_price_data
from app.strategies.bollinger_bands import BollingerBands
from app.strategies.ema_crossover import EMACrossover
from app.strategies.ichimoku import IchimokuCloud
from app.strategies.macd import MACDStrategy
from app.strategies.parabolic_sar import ParabolicSAR
from app.strategies.rsi import RSIStrategy
from app.strategies.sma_crossover import SMACrossover
from app.strategies.stochastic import StochasticOscillator
from app.strategies.supertrend import Supertrend
from app.strategies.williams_r import WilliamsR

router = APIRouter(prefix="/api", tags=["backtest"])

STRATEGIES = {
    "sma_crossover": SMACrossover(),
    "rsi": RSIStrategy(),
    "macd": MACDStrategy(),
    "bollinger_bands": BollingerBands(),
    "stochastic": StochasticOscillator(),
    "supertrend": Supertrend(),
    "ema_crossover": EMACrossover(),
    "parabolic_sar": ParabolicSAR(),
    "ichimoku": IchimokuCloud(),
    "williams_r": WilliamsR(),
}

STRATEGY_DEFINITIONS = [
    StrategyInfo(
        id="sma_crossover",
        name="SMA Kesişim",
        description=(
            "Kısa vadeli hareketli ortalama uzun vadeliyi yukarı kestiğinde alış, aşağı kestiğinde satış sinyali verir. "
            "Trend başlangıçlarını yakalamada etkilidir ancak yatay piyasalarda çok sayıda yanlış sinyal üretebilir."
        ),
        parameters=[
            StrategyParam(
                key="kisa_periyot", label="Kısa Periyot", min=5, max=50, default=20, step=1,
                description="Kısa vadeli trendi takip eder. Düşük değerler daha hassas ama daha gürültülü sinyaller üretir.",
            ),
            StrategyParam(
                key="uzun_periyot", label="Uzun Periyot", min=10, max=200, default=50, step=1,
                description="Uzun vadeli trendi belirler. Yüksek değerler ana trendi daha iyi yakalar ama gecikmeli sinyal verir.",
            ),
        ],
    ),
    StrategyInfo(
        id="rsi",
        name="RSI",
        description=(
            "RSI (Güç Endeksi), fiyat hareketlerinin hızını ve büyüklüğünü 0-100 arasında ölçer. "
            "Aşırı satım bölgesinden yukarı çıkışta alış, aşırı alım bölgesinden aşağı düşüşte satış sinyali verir. "
            "Yatay piyasalarda başarılı, güçlü trendlerde erken çıkışa neden olabilir."
        ),
        parameters=[
            StrategyParam(
                key="periyot", label="RSI Periyot", min=5, max=30, default=14, step=1,
                description="Hesaplama penceresi. 14 standart değerdir; düşük değerler daha sık sinyal verir.",
            ),
            StrategyParam(
                key="asiri_alim", label="Aşırı Alım", min=60, max=90, default=70, step=5,
                description="Bu seviyenin üzerindeki RSI aşırı alım sayılır. Düşürmek daha erken satış sinyali verir.",
            ),
            StrategyParam(
                key="asiri_satim", label="Aşırı Satım", min=10, max=40, default=30, step=5,
                description="Bu seviyenin altındaki RSI aşırı satım sayılır. Yükseltmek daha erken alış sinyali verir.",
            ),
        ],
    ),
    StrategyInfo(
        id="macd",
        name="MACD",
        description=(
            "MACD, iki üstel hareketli ortalama arasındaki farkı ölçer. MACD çizgisi sinyal çizgisini yukarı kestiğinde alış, "
            "aşağı kestiğinde satış sinyali üretir. Hem trend yönünü hem de momentumu gösterir. "
            "Trendli piyasalarda güçlü sinyaller verir; yatay piyasalarda çok sık al-sat üretebilir."
        ),
        parameters=[
            StrategyParam(
                key="hizli", label="Hızlı EMA", min=5, max=20, default=12, step=1,
                description="Kısa dönemli EMA. Daraltmak daha erken sinyaller verir ama yanlış sinyal riskini artırır.",
            ),
            StrategyParam(
                key="yavas", label="Yavaş EMA", min=15, max=40, default=26, step=1,
                description="Uzun dönemli EMA. MACD çizgisinin referans noktasını belirler.",
            ),
            StrategyParam(
                key="sinyal", label="Sinyal Periyot", min=5, max=15, default=9, step=1,
                description="Sinyal çizgisinin EMA periyodu. Düşük değerler daha hızlı ama daha gürültülü sinyaller üretir.",
            ),
        ],
    ),
    StrategyInfo(
        id="bollinger_bands",
        name="Bollinger Bantları",
        description=(
            "Fiyatın istatistiksel olarak 'normal' aralığını gösterir. Fiyat alt banda değdiğinde ucuz bölgeye gelmiş sayılır "
            "ve alış sinyali üretilir; üst banda ulaştığında pahalı bölgeye gelmiş sayılır ve satış sinyali üretilir. "
            "Yatay piyasalarda en iyi sonucu verir; güçlü trendlerde yanıltıcı sinyal üretebilir."
        ),
        parameters=[
            StrategyParam(
                key="periyot", label="Periyot", min=10, max=50, default=20, step=1,
                description="Orta bandın (SMA) hesaplama periyodu. 20 standart değerdir.",
            ),
            StrategyParam(
                key="std_carpani", label="Standart Sapma Çarpanı", type="float",
                min=1.0, max=3.0, default=2.0, step=0.5,
                description="Bantların genişliğini belirler. 2.0 standart; yüksek değerler daha az ama daha güvenilir sinyal üretir.",
            ),
        ],
    ),
    StrategyInfo(
        id="stochastic",
        name="Stochastic Osilatör",
        description=(
            "Kapanış fiyatının belirli bir dönem içindeki en düşük ve en yüksek fiyata göre konumunu 0-100 arasında ölçer. "
            "%K aşırı satım bölgesinde %D'yi yukarı keserse alış, aşırı alım bölgesinde aşağı keserse satış sinyali üretir. "
            "Özellikle yatay piyasalarda dönüş noktalarını yakalamak için kullanılır."
        ),
        parameters=[
            StrategyParam(
                key="k_periyot", label="%K Periyot", min=5, max=21, default=14, step=1,
                description="Ana gösterge periyodu. Düşük değerler daha duyarlı ama gürültülü sinyaller üretir.",
            ),
            StrategyParam(
                key="d_periyot", label="%D Periyot", min=1, max=10, default=3, step=1,
                description="%K'nın hareketli ortalaması. Sinyal çizgisi olarak kullanılır.",
            ),
            StrategyParam(
                key="asiri_alim", label="Aşırı Alım", min=70, max=90, default=80, step=5,
                description="Bu seviyenin üzerinde aşırı alım bölgesi. Standart değer 80'dir.",
            ),
            StrategyParam(
                key="asiri_satim", label="Aşırı Satım", min=10, max=30, default=20, step=5,
                description="Bu seviyenin altında aşırı satım bölgesi. Standart değer 20'dir.",
            ),
        ],
    ),
    StrategyInfo(
        id="supertrend",
        name="Supertrend",
        description=(
            "ATR (Ortalama Gerçek Aralık) bazlı bir trend takip göstergesidir. Türkiye'de Matriks platformunda çok popülerdir. "
            "Fiyat Supertrend çizgisini yukarı kırdığında alış, aşağı kırdığında satış sinyali verir. "
            "Trend piyasalarında çok etkilidir; çarpan parametresini artırmak daha az ama daha güvenilir sinyal üretir."
        ),
        parameters=[
            StrategyParam(
                key="atr_periyot", label="ATR Periyot", min=5, max=30, default=10, step=1,
                description="Volatilite hesaplama penceresi. Yüksek değerler daha yumuşak bir Supertrend çizgisi üretir.",
            ),
            StrategyParam(
                key="carpan", label="Çarpan", type="float", min=1.0, max=5.0, default=3.0, step=0.5,
                description="ATR çarpanı. Yüksek değerler trendi daha geç yakalar ama yanlış sinyalleri azaltır.",
            ),
        ],
    ),
    StrategyInfo(
        id="ema_crossover",
        name="EMA Kesişim",
        description=(
            "EMA (Üstel Hareketli Ortalama) son fiyatlara daha fazla ağırlık verir ve SMA'ya göre fiyat değişimlerine "
            "daha hızlı tepki verir. Kısa EMA uzun EMA'yı yukarı kestiğinde alış, aşağı kestiğinde satış sinyali üretir. "
            "Trend başlangıçlarına SMA'dan daha erken girmek isteyen traderlar için uygundur."
        ),
        parameters=[
            StrategyParam(
                key="kisa_periyot", label="Kısa EMA", min=5, max=50, default=12, step=1,
                description="Kısa dönemli EMA. 12 günlük değer yaygın kullanılır.",
            ),
            StrategyParam(
                key="uzun_periyot", label="Uzun EMA", min=10, max=200, default=26, step=1,
                description="Uzun dönemli EMA. Kısa EMA ile arasındaki fark büyüdükçe sinyal gecikir ama güvenilirlik artar.",
            ),
        ],
    ),
    StrategyInfo(
        id="parabolic_sar",
        name="Parabolic SAR",
        description=(
            "Parabolic SAR (Dur ve Dönüş), trend yönünü ve potansiyel dönüş noktalarını belirler. "
            "Fiyatın üzerinde veya altında noktalar olarak görüntülenir. Fiyat SAR noktalarını kırdığında trend değişir "
            "ve alım/satım sinyali üretilir. Hızlanma faktörü, trendin ivme kazandıkça SAR'ın fiyata ne kadar hızlı yaklaşacağını belirler."
        ),
        parameters=[
            StrategyParam(
                key="af_baslangic", label="Hızlanma Başlangıç", type="float",
                min=0.01, max=0.05, default=0.02, step=0.01,
                description="Başlangıç hızlanma faktörü. Düşük değerler trendin başında daha yavaş tepki verir.",
            ),
            StrategyParam(
                key="af_artis", label="Hızlanma Artışı", type="float",
                min=0.01, max=0.05, default=0.02, step=0.01,
                description="Her yeni zirve/dipte hızlanma faktörüne eklenen değer.",
            ),
            StrategyParam(
                key="af_maks", label="Hızlanma Maksimum", type="float",
                min=0.1, max=0.3, default=0.2, step=0.05,
                description="Hızlanma faktörünün ulaşabileceği üst limit. Düşürmek daha geniş bir SAR mesafesi sağlar.",
            ),
        ],
    ),
    StrategyInfo(
        id="ichimoku",
        name="Ichimoku Bulutu",
        description=(
            "Japonya'dan gelen kapsamlı bir gösterge: tek bir bakışta trend yönü, destek/direnç seviyeleri ve momentum bilgisi verir. "
            "Tenkan-sen Kijun-sen'i yukarı kestiğinde ve fiyat bulutun üstündeyse alış, aşağı kestiğinde ve fiyat bulutun altındaysa "
            "satış sinyali üretir. Senkou A ve B çizgileri arasındaki 'bulut' gelecekteki destek/direnç bölgelerini gösterir."
        ),
        parameters=[
            StrategyParam(
                key="tenkan", label="Tenkan-sen", min=5, max=15, default=9, step=1,
                description="Dönüş çizgisi periyodu. Kısa vadeli momentum ve destek/direnç gösterir.",
            ),
            StrategyParam(
                key="kijun", label="Kijun-sen", min=15, max=40, default=26, step=1,
                description="Standart çizgi periyodu. Orta vadeli trend yönünü belirler.",
            ),
            StrategyParam(
                key="senkou_b", label="Senkou Span B", min=30, max=80, default=52, step=1,
                description="Bulutun ikinci sınır çizgisi. Uzun vadeli destek/direnci gösterir.",
            ),
        ],
    ),
    StrategyInfo(
        id="williams_r",
        name="Williams %R",
        description=(
            "Fiyatın belirli bir dönem içindeki en yüksek ve en düşük arasındaki konumunu 0 ile -100 arasında ölçer. "
            "-80'in altına düştüğünde aşırı satım bölgesine girer ve yükselme potansiyeli vardır (alış); "
            "-20'nin üzerine çıktığında aşırı alım bölgesine girer ve düşme riski artar (satış)."
        ),
        parameters=[
            StrategyParam(
                key="periyot", label="Periyot", min=5, max=30, default=14, step=1,
                description="Hesaplama penceresi. 14 standart değerdir; düşük değerler daha duyarlı sinyal verir.",
            ),
            StrategyParam(
                key="asiri_alim", label="Aşırı Alım", min=-30, max=-5, default=-20, step=5,
                description="Bu seviyenin üzerinde aşırı alım sayılır. Standart değer -20'dir.",
            ),
            StrategyParam(
                key="asiri_satim", label="Aşırı Satım", min=-95, max=-70, default=-80, step=5,
                description="Bu seviyenin altında aşırı satım sayılır. Standart değer -80'dir.",
            ),
        ],
    ),
]


@router.get("/strategies", response_model=StrategiesResponse)
async def get_strategies():
    return StrategiesResponse(strategies=STRATEGY_DEFINITIONS)


@router.post("/backtest", response_model=BacktestResponse)
async def run_backtest_endpoint(request: BacktestRequest):
    if request.strategy not in STRATEGIES:
        raise HTTPException(
            status_code=400,
            detail=f"Bilinmeyen strateji: {request.strategy}. Geçerli stratejiler: {list(STRATEGIES.keys())}",
        )

    try:
        df = fetch_price_data(request.symbol, request.start_date, request.end_date)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

    strategy = STRATEGIES[request.strategy]
    result = run_backtest(df, strategy, request.parameters, request.initial_capital)

    return BacktestResponse(**result)
