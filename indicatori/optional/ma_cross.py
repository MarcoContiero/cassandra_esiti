import pandas as pd

def analizza_ma_cross(df, timeframe):
    """
    Analizza l'incrocio tra SMA 9 e SMA 21 per fornire un segnale trend-following.
    Restituisce un punteggio su 2.
    """
    if not hasattr(df, 'columns') or 'close' not in df.columns:
        return {
            'indicatore': 'MA Cross',
            'scenario': 'errore',
            'punteggio': 0,
            'direzione': 'neutro',
            'timeframe': timeframe
        }

    df = df.copy()
    df["sma9"] = df["close"].rolling(9).mean()
    df["sma21"] = df["close"].rolling(21).mean()
    df_valide = df.dropna(subset=["sma9", "sma21"])

    if len(df_valide) < 10:
        return {
            "indicatore": "MA Cross",
            "timeframe": timeframe,
            "scenario": "dati insufficienti",
            "punteggio": 0,
            "direzione": "neutro",
            "valore": "medie non calcolabili"
        }

    # Ora puoi proseguire con l'analisi degli incroci su df_valide

    prev_row = df.iloc[-2]
    last_row = df.iloc[-1]

    if prev_row["sma9"] < prev_row["sma21"] and last_row["sma9"] > last_row["sma21"]:
        scenario = "incrocio rialzista"
        direzione = "long"
        punteggio = 4
    elif prev_row["sma9"] > prev_row["sma21"] and last_row["sma9"] < last_row["sma21"]:
        scenario = "incrocio ribassista"
        direzione = "short"
        punteggio = 4
    else:
        scenario = "nessun incrocio"
        direzione = "neutro"
        punteggio = 0

    return {
        "indicatore": "MA Cross",
        "timeframe": timeframe,
        "scenario": scenario,
        "punteggio": punteggio,
        "direzione": direzione,
        "valore": f"SMA9: {round(last_row['sma9'], 2)} / SMA21: {round(last_row['sma21'], 2)}"
    }
