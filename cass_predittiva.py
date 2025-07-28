import json
from datetime import datetime
import os
from analisi.analizza_coin_completa import analizza_coin_completa
from upload_to_gcs import upload_to_gcs

BUCKET = "cassandra_backup_moire"

# === CONFIG ===
LISTA_COIN_FILE = "lista_coin.txt"
TIMEFRAMES = ["15m", "1h", "4h"]
CARTELLA_PREVISIONI = "previsioni"


def leggi_lista_coin(percorso=LISTA_COIN_FILE):
    if not os.path.exists(percorso):
        print(f"⚠️ File lista coin non trovato: {percorso}")
        return []
    with open(percorso, "r") as f:
        return [r.strip().upper() for r in f if r.strip()]


def genera_previsione_reale(coin, tf):
    try:
        blocchi = analizza_coin_completa(coin, tf)
        scenario = blocchi.get("risultato_finale", {}).get("valore", "n.d.")
    except Exception as e:
        print(f"❌ Errore analisi {coin} {tf}: {e}")
        scenario = "errore"

    return {
        "timestamp": datetime.now().isoformat(),
        "coin": coin,
        "timeframe": tf,
        "direzione": scenario,
        "note": "Scenario reale stimato da Cassandra (Moire - Lachesi)"
    }


def run_predittiva():
    lista_coin = leggi_lista_coin()
    if not lista_coin:
        print("🚫 Nessuna coin da analizzare.")
        return

    for coin in lista_coin:
        for tf in TIMEFRAMES:
            previsione = genera_previsione_reale(coin, tf)
            timestamp = datetime.now().strftime("%Y-%m-%dT%H-%M-%S")
            nome_file = f"{coin}_{tf}_{timestamp}.json"
            path_gcs = f"{CARTELLA_PREVISIONI}/{nome_file}"
            try:
                upload_to_gcs(BUCKET, path_gcs, json.dumps(previsione, indent=2))
                print(f"✅ Salvata previsione ➤ {coin} {tf} → {previsione['direzione']}")
            except Exception as e:
                print(f"❌ Errore salvataggio GCS: {e}")


if __name__ == "__main__":
    run_predittiva()
