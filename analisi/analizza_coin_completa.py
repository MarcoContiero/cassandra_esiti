import os
import json
from datetime import datetime
from analisi.analizza_coin_light import scarica_dati_grezzi
from elaborazione.genera_blocchi_analisi_finale import genera_blocchi_analisi_finale
from shared.config import PATH_ANALISI_GREZZE

def analizza_coin_completa(coin: str, timeframes: list = None) -> dict:
    if timeframes is None:
        timeframes = ["15m", "1h", "4h", "1d", "1w"]

    # Scarica dati grezzi
    grezzi = scarica_dati_grezzi(coin, timeframes)

    # Timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Salva file grezzi
    risultati_grezzi = {
        "dati": grezzi,
        "_timestamp_download": timestamp
    }
    os.makedirs(PATH_ANALISI_GREZZE, exist_ok=True)
    path_json = os.path.join(PATH_ANALISI_GREZZE, f"{coin.lower()}_grezzi.json")
    with open(path_json, "w") as f:
        json.dump(risultati_grezzi, f, indent=2, default=str)

    # Costruzione lista_con_gruppi e gruppi_indicatori
    with open("gruppi_indicatori.json", "r") as g:
        raw_gruppi = json.load(g)
        gruppi_indicatori = {k.strip().lower().replace(" ", "_"): v for k, v in raw_gruppi.items()}

    lista_con_gruppi = []
    for tf, lista in grezzi.items():
        conversione_tf = {"1": "1h", "4": "4h", "15": "15m", "240": "4h"}
        if tf in conversione_tf:
            tf = conversione_tf[tf]

    intervalli_validi = ["15m", "1h", "4h", "1d"]
    if tf not in intervalli_validi:
        print(f"⚠️ Interval non valido: {tf} → salto {coin}")
        continue
    intervalli_validi = ["15m", "1h", "4h", "1d"]
    if tf not in intervalli_validi:
        print(f"⚠️ Interval non valido: {tf} → salto {coin}")
        continue
        for riga in lista:
            nome = riga.get("indicatore", "").strip().lower().replace(" ", "_")
            riga["gruppo"] = gruppi_indicatori.get(nome, "core")
            riga["timeframe"] = tf
            lista_con_gruppi.append(riga)

    # Genera blocchi (ora con gruppi_indicatori passati)
    blocchi = genera_blocchi_analisi_finale(
        coin=coin,
        lista_indicatori=lista_con_gruppi,
        gruppi_indicatori=gruppi_indicatori,
        salva_file=True,
        data_analisi=timestamp,
        data_dati=timestamp
    )

    # Ritorna anche i dati per classifica
    return {
        **blocchi,
        "blocco_riepilogo_tf": blocchi.get("blocco_riepilogo_tf", {}),
        "scenario_finale": blocchi.get("risultato_finale", "n/d")
    }
