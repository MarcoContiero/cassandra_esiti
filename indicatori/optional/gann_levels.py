
import pandas as pd
import numpy as np

def analizza_gann(df, timeframe):
    if not hasattr(df, 'columns') or 'close' not in df.columns:
        return {
            'indicatore': 'GANN',
            'scenario': 'errore',
            'punteggio': 0,
            'direzione': 'neutro'
        }

    base_price = df['close'].iloc[0]
    num_candele = len(df)

    scale_ratio = (df['close'].max() - df['close'].min()) / num_candele
    scale_ratio = scale_ratio if scale_ratio != 0 else 1

    angoli = {
        '1:1': 1,
        '2:1': 2,
        '1:2': 0.5,
        '4:1': 4,
        '1:4': 0.25
    }

    punteggio = 0
    scenario = "neutro"
    messaggi = []

    for nome, rapporto in angoli.items():
        linea = [base_price + (i * scale_ratio * rapporto) for i in range(len(df))]
        df[f'gann_{nome}'] = linea

        prezzo_attuale = df['close'].iloc[-1]
        linea_attuale = linea[-1]
        diff_percentuale = (prezzo_attuale - linea_attuale) / linea_attuale * 100

        if abs(diff_percentuale) <= 0.5:
            punteggio = max(punteggio, 1)
            scenario = "neutro"
            messaggi.append(f"Prezzo vicino all'angolo {nome}")
        elif diff_percentuale > 1:
            punteggio = max(punteggio, 2)
            scenario = "long"
            messaggi.append(f"Breakout sopra angolo {nome}")
        elif diff_percentuale < -1:
            punteggio = max(punteggio, 2)
            scenario = "short"
            messaggi.append(f"Breakdown sotto angolo {nome}")

    direzione = "long" if "long" in scenario else "short" if "short" in scenario else "neutro"

    return {
        "indicatore": "Gann",
        "timeframe": timeframe,
        "scenario": scenario,
        "punteggio": punteggio,
        "messaggio": "; ".join(messaggi),
        "direzione": direzione,
        "valore": f"Prezzo: {round(prezzo_attuale, 2)} | Scala: {round(scale_ratio, 4)}"
    }
