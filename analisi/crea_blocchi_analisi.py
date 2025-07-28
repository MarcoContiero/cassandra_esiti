from collections import defaultdict
import os
import pandas as pd
from shared.config import PATH_ANALISI_GREZZE, PATH_ANALISI_FINALI
from analisi.blocchi_generali import (
    blocco_info_generali, blocco_dettagli_per_tf, blocco_dati_binance, blocco_indicatori_forti, calcola_riepilogo_totale, blocco_riassunto_globale
)
from analisi.blocchi_extra import (
    blocco_scenari_per_tf, blocco_commento_scenari, blocco_dati_grezzi, blocco_riassunto_tecnico
)
from analisi.genera_commento_finale import genera_commento_finale_avanzato
from indicatori.core.calcola_scenario_finale import calcola_scenario_finale
from blocchi_commenti import blocco_commento_finale
from blocchi_supporti_resistenze import blocco_supporti_resistenze
from utils.utils_analisi import aggrega_per_tf
import json

with open("gruppi_indicatori.json", "r") as g:
    raw_mappa = json.load(g)
    gruppi_indicatori = {k.strip().lower().replace(" ", "_"): v for k, v in raw_mappa.items()}


def crea_blocchi_analisi(coin: str, lista_indicatori: list, data_analisi: str = "", data_dati: str = "") -> dict:

    per_tf = aggrega_per_tf(lista_indicatori)
    risultato = calcola_scenario_finale(per_tf)

    # === METADATI ===
    timeframes_presenti = sorted({x.get("timeframe") for x in lista_indicatori if "timeframe" in x})
    tf_riferimento = timeframes_presenti[0] if timeframes_presenti else "n/d"
    path_file_grezzo = os.path.join(PATH_ANALISI_GREZZE, f"{coin.lower()}_grezzi.json")

    risultato["meta_dati"] = {
        "coin": coin,
        "timeframe": tf_riferimento,
        "path_file_grezzo": path_file_grezzo,
        "timeframes": sorted(per_tf.keys())
    }

    meta_dati_finali = risultato["meta_dati"]

    # Blocchi principali
    b_info = blocco_info_generali(risultato["scenario_finale"], data_analisi, data_dati, coin)
    b_tf = blocco_dettagli_per_tf(risultato["punteggi_per_timeframe"])
    b_tech = blocco_riassunto_tecnico(lista_indicatori, gruppi_indicatori)
    b_globale = blocco_riassunto_globale(risultato["scenario_finale"])
    b_forti = blocco_indicatori_forti(lista_indicatori)

    riepilogo_tf = {}
    for tf in ["15m", "1h", "4h", "1d", "1w"]:
        lista = per_tf.get(tf, [])
        if not lista:
            continue
        punteggi = {"long": 0.0, "short": 0.0, "neutro": 0.0}
        for item in lista:
            direzione = item.get("direzione", "neutro")
            punteggio = item.get("punteggio", 0.0)
            if direzione in punteggi:
                punteggi[direzione] += punteggio
        ordinati = sorted(punteggi.items(), key=lambda x: x[1], reverse=True)
        direzione_dominante = ordinati[0][0]
        delta_val = ordinati[0][1] - ordinati[1][1] if len(ordinati) > 1 else 0.0
        punteggio_totale = sum(punteggi.values())
        riepilogo_tf[tf] = {
            "direzione": direzione_dominante,
            "delta": round(delta_val, 1),
            "punteggio": round(punteggio_totale, 1),
            "forze": punteggi
        }

    b_riepilogo_tf = "# === RIEPILOGO PER TIMEFRAME ===\n"
    for tf in meta_dati_finali["timeframes"]:
        voce = riepilogo_tf.get(tf)
        if voce:
            b_riepilogo_tf += f"[{tf}] ➔ scenario: {voce['direzione']} | punteggio: {voce['punteggio']} | delta: {voce['delta']} | forze: {voce['forze']}\n"

    indicatori_tf = [x for tf in per_tf for x in risultato.get(tf, []) if x.get("indicatore") in ["MACD", "RSI", "EMA 21", "STOCH"]]
    riepilogo_globale = calcola_riepilogo_totale(lista_indicatori)
    b_commento = "# === COMMENTO STRATEGICO ===\n" + genera_commento_finale_avanzato(riepilogo_globale, indicatori_tf) + \
                 "\n\n# === COMMENTO GENERICO ===\n" + blocco_commento_finale(risultato["scenario_finale"])

    # Blocchi extra
    b_scenari = blocco_scenari_per_tf(lista_indicatori)
    b_commento_scenari = blocco_commento_scenari(lista_indicatori)
    b_binance = blocco_dati_binance(coin)
    b_sr = blocco_supporti_resistenze(lista_indicatori, coin)
    b_grezzi = blocco_dati_grezzi(lista_indicatori)

    return {
        "b_info": b_info,
        "b_tf": b_tf,
        "b_tech": b_tech,
        "b_globale": b_globale,
        "b_riepilogo_tf": b_riepilogo_tf,
        "b_commento": b_commento,
        "b_scenari": b_scenari,
        "b_commento_scenari": b_commento_scenari,
        "b_forti": b_forti,
        "b_binance": b_binance,
        "b_sr": b_sr,
        "b_grezzi": b_grezzi,
        "risultato": risultato,
        "per_tf": per_tf
    }
