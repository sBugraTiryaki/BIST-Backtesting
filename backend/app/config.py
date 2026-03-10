from pathlib import Path

CACHE_DIR = Path(__file__).resolve().parent.parent / "cache"
CACHE_TTL_SECONDS = 4 * 60 * 60  # 4 saat

BIST30: list[dict[str, str]] = [
    {"symbol": "AKBNK", "name": "Akbank", "yahoo_symbol": "AKBNK.IS"},
    {"symbol": "ARCLK", "name": "Arçelik", "yahoo_symbol": "ARCLK.IS"},
    {"symbol": "ASELS", "name": "Aselsan", "yahoo_symbol": "ASELS.IS"},
    {"symbol": "BIMAS", "name": "BİM Mağazalar", "yahoo_symbol": "BIMAS.IS"},
    {"symbol": "EKGYO", "name": "Emlak Konut GYO", "yahoo_symbol": "EKGYO.IS"},
    {"symbol": "ENKAI", "name": "Enka İnşaat", "yahoo_symbol": "ENKAI.IS"},
    {"symbol": "EREGL", "name": "Ereğli Demir Çelik", "yahoo_symbol": "EREGL.IS"},
    {"symbol": "FROTO", "name": "Ford Otosan", "yahoo_symbol": "FROTO.IS"},
    {"symbol": "GARAN", "name": "Garanti BBVA", "yahoo_symbol": "GARAN.IS"},
    {"symbol": "GUBRF", "name": "Gübre Fabrikaları", "yahoo_symbol": "GUBRF.IS"},
    {"symbol": "HEKTS", "name": "Hektaş Ticaret", "yahoo_symbol": "HEKTS.IS"},
    {"symbol": "ISCTR", "name": "İş Bankası C", "yahoo_symbol": "ISCTR.IS"},
    {"symbol": "KCHOL", "name": "Koç Holding", "yahoo_symbol": "KCHOL.IS"},
    {"symbol": "KOZAA", "name": "Koza Altın", "yahoo_symbol": "KOZAA.IS"},
    {"symbol": "KOZAL", "name": "Koza Anadolu Metal", "yahoo_symbol": "KOZAL.IS"},
    {"symbol": "KRDMD", "name": "Kardemir D", "yahoo_symbol": "KRDMD.IS"},
    {"symbol": "MGROS", "name": "Migros Ticaret", "yahoo_symbol": "MGROS.IS"},
    {"symbol": "OYAKC", "name": "Oyak Çimento", "yahoo_symbol": "OYAKC.IS"},
    {"symbol": "PETKM", "name": "Petkim", "yahoo_symbol": "PETKM.IS"},
    {"symbol": "PGSUS", "name": "Pegasus", "yahoo_symbol": "PGSUS.IS"},
    {"symbol": "SAHOL", "name": "Sabancı Holding", "yahoo_symbol": "SAHOL.IS"},
    {"symbol": "SASA", "name": "SASA Polyester", "yahoo_symbol": "SASA.IS"},
    {"symbol": "SISE", "name": "Şişecam", "yahoo_symbol": "SISE.IS"},
    {"symbol": "TAVHL", "name": "TAV Havalimanları", "yahoo_symbol": "TAVHL.IS"},
    {"symbol": "TCELL", "name": "Turkcell", "yahoo_symbol": "TCELL.IS"},
    {"symbol": "THYAO", "name": "Türk Hava Yolları", "yahoo_symbol": "THYAO.IS"},
    {"symbol": "TKFEN", "name": "Tekfen Holding", "yahoo_symbol": "TKFEN.IS"},
    {"symbol": "TOASO", "name": "Tofaş Oto Fab.", "yahoo_symbol": "TOASO.IS"},
    {"symbol": "TUPRS", "name": "Tüpraş", "yahoo_symbol": "TUPRS.IS"},
    {"symbol": "YKBNK", "name": "Yapı Kredi", "yahoo_symbol": "YKBNK.IS"},
]

DEFAULT_INITIAL_CAPITAL = 100_000.0
