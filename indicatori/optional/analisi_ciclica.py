import pandas as pd
from utils.validazione import valida_dataframe

@valida_dataframe
def analizza_ciclo(df: pd.DataFrame, timeframe: str) -> dict:
    """
    Analizza la fase del ciclo sulla base dei minimi locali.
    """
    try:
        chiusure = df["close"]
        prezzo_attuale = chiusure.iloc[-1]

        # Trova i minimi locali con rolling
        minimo_recenti = chiusure.rolling(window=5, center=True).min()
        indice_minimi = minimo_recenti[minimo_recenti == chiusure].dropna().index

        if len(indice_minimi) == 0:
            return {
                "indicatore": "Ciclica",
                "timeframe": timeframe,
                "valore": prezzo_attuale,
                "scenario": "neutro",
                "punteggio": 0,
                "messaggio": "Nessun minimo locale rilevante",
                "direzione": "neutro"
            }

        # Estrai l’ultimo minimo locale trovato
        ultimo_minimo_idx = indice_minimi[-1]
        pos_ultimo_minimo = chiusure.index.get_loc(ultimo_minimo_idx)
        distanza = len(chiusure) - pos_ultimo_minimo - 1

        # Valuta la fase del ciclo
        if distanza <= 3:
            scenario = "long"
            punteggio = 0
            messaggio = "Inizio nuovo ciclo"
        elif distanza >= 15:
            scenario = "short"
            punteggio = 0
            messaggio = "Fase finale del ciclo"
        else:
            scenario = "neutro"
            punteggio = 0
            messaggio = "Fase intermedia del ciclo"

        direzione = "long" if scenario == "long" else "short" if scenario == "short" else "neutro"

        return {
            "indicatore": "Ciclica",
            "timeframe": timeframe,
            "valore": f"{round(prezzo_attuale, 2)} | distanza minimo: {distanza}",
            "scenario": scenario,
            "punteggio": punteggio,
            "messaggio": messaggio,
            "direzione": direzione
        }

    except Exception as e:
        print(f"❌ Errore critico in analizza_ciclo: {e}")
        return {
            "indicatore": "Ciclica",
            "timeframe": timeframe,
            "valore": None,
            "scenario": "errore",
            "punteggio": 0,
            "messaggio": f"Errore: {e}",
            "direzione": "neutro"
        }

