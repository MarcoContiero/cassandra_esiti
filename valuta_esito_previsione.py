import os
import json
import pandas as pd
from datetime import datetime, timedelta

CARTELLA_PREVISIONI = "previsioni"
CARTELLA_DATI = "dati_csv"
CARTELLA_ESITI = "esiti"

def parse_timestamp(s: str) -> datetime:
    """Prova a parsare una data, con o senza ora"""
    for fmt in ("%Y-%m-%d %H:%M", "%Y-%m-%d"):
        try:
            return datetime.strptime(s, fmt)
        except ValueError:
            continue
    raise ValueError(f"Formato data non riconosciuto: {s}")

def valuta_esito_da_previsione(previsione: dict, df: pd.DataFrame) -> dict:
    entry_min, entry_max = previsione["entry_range"]
    target = previsione["target"]
    stop = previsione["stop"]
    max_candele = previsione["max_candele"]

    t0 = parse_timestamp(previsione["data_previsione"])
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df = df[df["timestamp"] > t0].sort_values("timestamp").reset_index(drop=True)

    df_finestra = df.iloc[:max_candele]

    esito = {
        "coin": previsione["coin"],
        "timeframe": previsione["timeframe"],
        "data_previsione": previsione["data_previsione"],
        "entry_hit": False,
        "target_hit": False,
        "stop_hit": False,
        "esito": "non attivato",
        "dettagli": {}
    }

    entry_time = None
    for i, row in df_finestra.iterrows():
        high = row["high"]
        low = row["low"]
        time = row["timestamp"]

        if not esito["entry_hit"]:
            if high >= entry_min and low <= entry_max:
                esito["entry_hit"] = True
                entry_time = time
                esito["dettagli"]["entry_time"] = str(time)

        if esito["entry_hit"]:
            if low <= stop:
                esito["stop_hit"] = True
                esito["dettagli"]["stop_time"] = str(time)
                esito["esito"] = "fallito"
                return esito
            if high >= target:
                esito["target_hit"] = True
                esito["dettagli"]["target_time"] = str(time)
                esito["esito"] = "riuscito"
                return esito

    if esito["entry_hit"]:
        esito["esito"] = "in attesa"
    else:
        esito["esito"] = "non attivato"
    return esito

def main():
    os.makedirs(CARTELLA_ESITI, exist_ok=True)
    file_previsioni = [f for f in os.listdir(CARTELLA_PREVISIONI) if f.endswith(".json")]

    for file in file_previsioni:
        try:
            with open(os.path.join(CARTELLA_PREVISIONI, file), "r") as f:
                previsione = json.load(f)

            coin = previsione["coin"]
            tf = previsione["timeframe"]
            filename_csv = f"{coin}_{tf}.csv"
            path_csv = os.path.join(CARTELLA_DATI, filename_csv)

            if not os.path.exists(path_csv):
                print(f"❌ Dati non trovati per {coin} {tf}")
                continue

            df = pd.read_csv(path_csv)

            # pulizia colonne numeriche
            for col in ["open", "high", "low", "close"]:
                df[col] = pd.to_numeric(df[col], errors="coerce")

            esito = valuta_esito_da_previsione(previsione, df)

            nome_output = file.replace(".json", ".json")
            path_esito = os.path.join(CARTELLA_ESITI, nome_output)
            with open(path_esito, "w") as f_out:
                json.dump(esito, f_out, indent=2)

            print(f"✅ Esito salvato per {coin} ({previsione['data_previsione']}): {esito['esito']}")

        except Exception as e:
            print(f"❌ Errore su {file}: {e}")

if __name__ == "__main__":
    main()
