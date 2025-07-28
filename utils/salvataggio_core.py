import json
import pandas as pd
import os

def esporta_risultati_core(nome_coin: str, risultati: dict, cartella: str = "dati_core"):
    """Salva i risultati validi (core) in JSON e CSV"""
    os.makedirs(cartella, exist_ok=True)

    # Salvataggio JSON
    path_json = os.path.join(cartella, f"{nome_coin}_core.json")
    with open(path_json, "w") as f:
        json.dump(risultati, f, indent=2, default=str)

    # Esplodi in CSV
    records = []
    for tf, lista in risultati.items():
        for r in lista:
            record = r.copy()
            record["timeframe"] = tf
            records.append(record)

    if records:
        df = pd.DataFrame(records)
        path_csv = os.path.join(cartella, f"{nome_coin}_core.csv")
        df.to_csv(path_csv, index=False)


def carica_risultati_core(nome_coin: str, cartella: str = "dati_core") -> dict:
    """Carica i risultati salvati della parte core (formato JSON)"""
    path = os.path.join(cartella, f"{nome_coin}_core.json")
    with open(path, "r") as f:
        return json.load(f)
