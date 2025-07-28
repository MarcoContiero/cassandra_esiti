import os
import json
from datetime import datetime
import pandas as pd
from google.cloud import storage
from google.oauth2 import service_account
from analisi.analizza_coin_completa import analizza_coin_completa
from upload_to_gcs import upload_to_gcs

BUCKET = "cassandra_backup_moire"
CREDENTIALS_FILE = "credentials.json"
LOG_PATH_CSV = "log/registro_successi.csv"
LOG_PATH_JSON = "log/registro_successi.json"


def confronta_scenario(previsto, osservato):
    return previsto.lower() == osservato.lower()


def scarica_lista_file(bucket_name, prefix):
    credentials = service_account.Credentials.from_service_account_file("credentials.json")
    client = storage.Client(credentials=credentials)
    blobs = client.list_blobs(bucket_name, prefix=prefix)
    return [b.name for b in blobs if b.name.endswith(".json")]


def scarica_json(bucket_name, blob_name):
    credentials = service_account.Credentials.from_service_account_file("credentials.json")
    client = storage.Client(credentials=credentials)
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(blob_name)
    content = blob.download_as_text()
    return json.loads(content)


def run_riflessiva():
    print("🧠 Riflessiva in esecuzione...")
    files = scarica_lista_file(BUCKET, "previsioni/")
    logs = []

    for f in files:
        try:
            previsione = scarica_json(BUCKET, f)
            coin = previsione.get("coin")
            tf = previsione.get("timeframe")
            previsto = previsione.get("direzione")

            blocchi = analizza_coin_completa(coin, tf)
            osservato = blocchi.get("risultato_finale", {}).get("valore", "n.d.")
            corretto = confronta_scenario(previsto, osservato)

            logs.append({
                "timestamp": datetime.now().isoformat(),
                "coin": coin,
                "timeframe": tf,
                "previsto": previsto,
                "reale": osservato,
                "esito": "✅" if corretto else "❌"
            })
        except Exception as e:
            print(f"⚠️ Errore nel confronto file {f}: {e}")
            continue

    if logs:
        df_log = pd.DataFrame(logs)
        try:
            old_log = scarica_json(BUCKET, LOG_PATH_JSON)
            df_old = pd.DataFrame(old_log)
            df_log = pd.concat([df_old, df_log], ignore_index=True)
        except Exception:
            pass

        upload_to_gcs(BUCKET, LOG_PATH_CSV, df_log.to_csv(index=False), content_type="text/csv")
        upload_to_gcs(BUCKET, LOG_PATH_JSON, df_log.to_json(orient="records", indent=2))
        print(f"📘 Riflessiva ➤ {len(logs)} confronti registrati.")
    else:
        print("🟡 Riflessiva ➤ Nessun confronto disponibile.")


if __name__ == "__main__":
    run_riflessiva()
