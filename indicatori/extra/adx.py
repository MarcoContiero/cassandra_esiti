import ta.trend
from utils.validazione import valida_dataframe  # ✅ IMPORT NECESSARIO

@valida_dataframe
def analizza_adx(df, timeframe):
    if len(df) < 14:
        return {
            "indicatore": "ADX",
            "timeframe": timeframe,
            "valore": "errore",
            "punteggio": 0,
            "direzione": "neutro",
            "scenario": "errore"
        }

    adx_indicator = ta.trend.ADXIndicator(
        high=df['high'],
        low=df['low'],
        close=df['close'],
        window=14
    )
    adx = adx_indicator.adx().iloc[-1]

    if adx > 25:
        scenario = "trend forte"
        direzione = "long"
        punteggio = 4
    elif adx < 15:
        scenario = "assenza di trend"
        direzione = "neutro"
        punteggio = 0
    else:
        scenario = "trend debole"
        direzione = "neutro"
        punteggio = 2

    return {
        "indicatore": "ADX",
        "timeframe": timeframe,
        "valore": round(adx, 2),
        "punteggio": punteggio,
        "scenario": scenario,
        "direzione": direzione
    }