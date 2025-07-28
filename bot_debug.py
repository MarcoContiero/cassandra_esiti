# bot_debug.py

import os
import json
from datetime import datetime
from analisi.analizza_coin_light import scarica_dati_grezzi
from elaborazione.genera_blocchi_analisi_finale import genera_blocchi_analisi_finale
from shared.config import PATH_ANALISI_GREZZE

def analizza_coin(coin):
    print(f"🔍 Analizzo {coin}")

    timeframes = ["15m", "1h", "4h", "1d", "1w"]
    grezzi_raw = scarica_dati_grezzi(coin, timeframes)

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    risultati_grezzi = {
        "dati": grezzi_raw,
        "_timestamp_download": timestamp,
        "timeframes": timeframes
    }

    os.makedirs(PATH_ANALISI_GREZZE, exist_ok=True)
    path_json = os.path.join(PATH_ANALISI_GREZZE, f"{coin.lower()}_grezzi.json")
    with open(path_json, "w") as f:
        json.dump(risultati_grezzi, f, indent=2, default=str)

    print(f"✅ Salvato JSON grezzo ➤ {path_json}")

    # === Ricarica e avvia analisi finale
    with open(path_json, "r") as f:
        risultati = json.load(f)

    # Carica mappa gruppi indicatori
    with open("gruppi_indicatori.json", "r") as g:
        raw_mappa = json.load(g)
        mappa_gruppi = {k.strip().lower(): v for k, v in raw_mappa.items()}

    lista_con_gruppi = []
    dati_indicatori = risultati.get("dati", {})
    for tf, lista in dati_indicatori.items():
        for riga in lista:
            nome = riga.get("indicatore", "").strip().lower().replace(" ", "_")
            riga["gruppo"] = mappa_gruppi.get(nome, "core")
            riga["timeframe"] = tf
            lista_con_gruppi.append(riga)

    if not lista_con_gruppi:
        print("❌ Errore: lista_con_gruppi è vuota!")
        return

    print(f"📊 Trovati {len(lista_con_gruppi)} indicatori")

    data_analisi = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    data_dati = risultati.get("_timestamp_download", "n.d.")

    blocchi = None  # ✅ Prevenzione errore variabile non associata

    try:
        blocchi = genera_blocchi_analisi_finale(
            coin,
            lista_con_gruppi,
            salva_file=True,
            data_analisi=data_analisi,
            data_dati=data_dati
        )

        if blocchi is None:
            testo_finale = "❌ Errore: la funzione ha restituito None"
        elif isinstance(blocchi, str):
            testo_finale = blocchi
        else:
            testo_finale = blocchi.get("blocco_commento", "❌ Nessun commento generato")

    except Exception as e:
        import traceback
        traceback.print_exc()
        testo_finale = f"❌ Errore nella generazione dei blocchi: {e}"

    print("\n===== COMMENTO FINALE =====\n")
    print(testo_finale)

# ✅ Test manuale solo se lanciato direttamente
if __name__ == "__main__":
    analizza_coin("ETHUSDT")
