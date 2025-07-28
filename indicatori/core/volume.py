import pandas as pd

def analizza_volume(df: pd.DataFrame, timeframe: str) -> list:
    risultati = []
    try:
        vol = df['volume']
        vol_now = vol.iloc[-1]
        vol_prev = vol.iloc[-2]
        delta_prezzo = df['close'].iloc[-1] - df['close'].iloc[-2]

        # CORRETTO: definizione sicura di media_volume PRIMA dell'utilizzo
        media_volume = vol.mean()

        if vol_now > vol_prev and delta_prezzo > 0:
            scenario = "volume in aumento con prezzo in salita"
            direzione = "long"
            punteggio = 4
        elif vol_now > vol_prev and delta_prezzo < 0:
            scenario = "volume in aumento con prezzo in discesa"
            direzione = "short"
            punteggio = 4
        elif vol_now < media_volume:
            scenario = "volume sotto media"
            direzione = "neutro"
            punteggio = 2
        else:
            scenario = "volume normale"
            direzione = "neutro"
            punteggio = 1

        risultati.append({
            "indicatore": "Volume",
            "timeframe": timeframe,
            "valore": round(vol_now, 2),
            "scenario": scenario,
            "punteggio": punteggio,
            "direzione": direzione,
            "gruppo": "CORE"
        })
    except Exception as e:
        risultati.append({
            "indicatore": "Volume",
            "timeframe": timeframe,
            "valore": None,
            "scenario": f"errore Volume: {e}",
            "punteggio": 0,
            "direzione": "neutro",
            "gruppo": "CORE"
        })
    return risultati
