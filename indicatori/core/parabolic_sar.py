import pandas as pd
import ta.trend


def analizza_parabolic_sar(df, timeframe):
    """
    Analizza la posizione del Parabolic SAR rispetto al prezzo.
    """
    if not hasattr(df, 'columns') or 'close' not in df.columns:
        return {
            'indicatore': 'Parabolic SAR',
            'scenario': 'errore',
            'punteggio': 0,
            'direzione': 'neutro'
        }

    sar = ta.trend.PSARIndicator(high=df["high"], low=df["low"], close=df["close"]).psar()
    prezzo = df["close"].iloc[-1]
    sar_val = sar.iloc[-1]
    sar_prev = sar.iloc[-2]

    if sar_prev > prezzo and sar_val < prezzo:
        scenario = "inversione rialzista"
        direzione = "long"
        punteggio = 6
    elif sar_prev < prezzo and sar_val > prezzo:
        scenario = "inversione ribassista"
        direzione = "short"
        punteggio = 6
    elif sar_val < prezzo:
        scenario = "trend rialzista"
        direzione = "long"
        punteggio = 4
    elif sar_val > prezzo:
        scenario = "trend ribassista"
        direzione = "short"
        punteggio = 4
    else:
        scenario = "neutro"
        direzione = "neutro"
        punteggio = 0

    return {
        "indicatore": "Parabolic SAR",
        "timeframe": timeframe,
        "valore": round(sar_val, 2) if sar_val else "SAR non disponibile",
        "scenario": scenario,
        "punteggio": punteggio,
        "direzione": direzione
    }
