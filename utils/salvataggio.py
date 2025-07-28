import json
import os
import pandas as pd
from shared.config import PATH_DATI_CSV

def salva_csv(df: pd.DataFrame, coin: str, timeframe: str):
    os.makedirs(PATH_DATI_CSV, exist_ok=True)
    path = os.path.join(PATH_DATI_CSV, f"{coin}_{timeframe}.csv")

    colonne_utili = [
        "time", "open", "high", "low", "close", "volume",
        "bollinger_hband", "bollinger_lband", "bollinger_mavg",
        "ema_21", "ema_50", "ema_100", "ema_200",
        "adx", "macd", "macd_signal", "macd_hist",
        "rsi", "obv", "cci", "aroon_up", "aroon_down", "aroon_osc",
        "roc", "trix", "fvg_valore", "psar"
    ]

    colonne_presenti = [c for c in colonne_utili if c in df.columns]
    df[colonne_presenti].to_csv(path, index=False)
    print(f"✅ Salvato: {path}")


def salva_file_testo(contenuto: str, nome_file: str, cartella: str = "output"):
    """
    Salva una stringa in un file di testo.
    """
    os.makedirs(cartella, exist_ok=True)
    path_completo = os.path.join(cartella, nome_file)
    with open(path_completo, "w", encoding="utf-8") as f:
        f.write(contenuto)
    print(f"✅ File salvato: {path_completo}")
    return path_completo

def estrai_scenario_e_punteggio(blocco):
    """
    Estrae la direzione dominante e il punteggio totale da un blocco (core + optional).
    """
    direzioni = []
    punteggio_totale = 0

    for gruppo in ["core", "optional"]:
        for indicatore in blocco.get(gruppo, []):
            direzioni.append(indicatore.get("scenario", "neutro"))
            punteggio_totale += indicatore.get("punteggio", 0)

    conta = {d: direzioni.count(d) for d in set(direzioni)}
    direzione_dominante = max(conta, key=conta.get) if conta else "n/a"

    return direzione_dominante, punteggio_totale
