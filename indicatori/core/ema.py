import pandas as pd
import ta.trend

def analizza_ema(df: pd.DataFrame, timeframe: str) -> list:
    risultati = []
    try:
        ema9 = ta.trend.ema_indicator(df['close'], window=9)
        ema21 = ta.trend.ema_indicator(df['close'], window=21)
        ema50 = ta.trend.ema_indicator(df['close'], window=50)
        ema200 = ta.trend.ema_indicator(df['close'], window=200)
        prezzo = df['close'].iloc[-1]

        # CORRETTO: uso di .iloc[-1] sui Series per evitare ambiguità
        sopra_tutte = all(prezzo > ema.iloc[-1] for ema in [ema9, ema21, ema50, ema200])
        sotto_tutte = all(prezzo < ema.iloc[-1] for ema in [ema9, ema21, ema50, ema200])

        if sopra_tutte:
            scenario = "prezzo sopra tutte le EMA"
            direzione = "long"
            punteggio = 5
        elif sotto_tutte:
            scenario = "prezzo sotto tutte le EMA"
            direzione = "short"
            punteggio = 5
        else:
            scenario = "prezzo tra le EMA"
            direzione = "neutro"
            punteggio = 2

        risultati.append({
            "indicatore": "EMA multi",
            "timeframe": timeframe,
            "valore": prezzo,
            "scenario": scenario,
            "punteggio": punteggio,
            "direzione": direzione,
            "gruppo": "CORE"
        })
    except Exception as e:
        risultati.append({
            "indicatore": "EMA",
            "timeframe": timeframe,
            "valore": None,
            "scenario": f"errore EMA: {e}",
            "punteggio": 0,
            "direzione": "neutro",
            "gruppo": "CORE"
        })
    return risultati
