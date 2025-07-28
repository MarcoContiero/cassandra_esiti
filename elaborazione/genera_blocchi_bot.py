import traceback
import json
import os
from elaborazione.genera_blocchi_analisi_finale import genera_blocchi_analisi_finale

def genera_analisi_bot(coin: str, dati: list, data_analisi: str, data_dati: str) -> str:
    blocchi = None

    try:
        # ✅ Carica gruppi indicatori
        with open("gruppi_indicatori.json", "r") as g:
            raw_mappa = json.load(g)
            gruppi_indicatori = {k.strip().lower(): v for k, v in raw_mappa.items()}

        blocchi = genera_blocchi_analisi_finale(
            coin=coin,
            lista_indicatori=dati,
            gruppi_indicatori=gruppi_indicatori,
            salva_file=False,
            data_analisi=data_analisi,
            data_dati=data_dati,
            solo_multi_tf=False
        )

    except Exception as e:
        print("❌ Errore nella generazione dei blocchi:", e)
        traceback.print_exc()
        return None

    if not isinstance(blocchi, dict):
        print("❌ Errore: formato blocchi inatteso.")
        return None

    testo = (
        "# === INFO GENERALI ===\n"
        + blocchi.get("blocco_info", "").strip()
        + "\n\n"
        "# === COMMENTO CASSANDRA ===\n"
        + blocchi.get("blocco_commento", "").strip()
        + "\n\n"
        "# === SUPPORTI E RESISTENZE ===\n"
        + blocchi.get("blocco_supporti_resistenze", "").strip()
    )

    return testo.strip()
