def genera_blocchi_analisi_finale(
    coin: str,
    lista_indicatori: list,
    gruppi_indicatori: dict,  # <--- nuovo parametro obbligatorio
    salva_file: bool = True,
    data_analisi: str = "",
    data_dati: str = "",
    solo_multi_tf: bool = False
) -> dict:

    from collections import defaultdict
    import os
    import pandas as pd
    from shared.config import PATH_ANALISI_GREZZE, PATH_ANALISI_FINALI
    from analisi.blocchi_commenti import blocco_commento_finale
    from analisi.blocchi_generali import (
        blocco_info_generali, blocco_dettagli_per_tf, blocco_dati_binance,
        blocco_riassunto_globale, blocco_indicatori_forti, calcola_riepilogo_totale
    )
    from analisi.blocchi_extra import (
        blocco_scenari_per_tf, blocco_commento_scenari,
        blocco_dati_grezzi, blocco_riassunto_tecnico
    )
    from analisi.blocchi_supporti_resistenze import blocco_supporti_resistenze
    from analisi.genera_commento_finale import genera_commento_finale_avanzato
    from indicatori.core.calcola_scenario_finale import calcola_scenario_finale
    from riassunti.genera_riassunto_multi_tf import genera_riassunto_multi_tf
    from riassunti.genera_riassunto_blocchi import genera_riassunto_blocchi
    from utils.utils_analisi import aggrega_per_tf

    blocchi = {}

    # === STEP 1: aggregazione e scenario ===
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

    # === Riassunto multi-tf strategico (sempre calcolato) ===
    indicatori_per_tf = aggrega_per_tf(lista_indicatori)
    riassunto_multi_tf = genera_riassunto_multi_tf(indicatori_per_tf, meta_dati_finali)

    # === SOLO BOT: ritorna solo i due blocchi
    if solo_multi_tf:
        return {
            "blocco_info": blocco_info_generali(risultato["scenario_finale"], data_analisi, data_dati, coin),
            "b_riassunto_multi_tf": riassunto_multi_tf.strip()
        }

    # === STREAMLIT COMPLETO ===
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
            b_riepilogo_tf += f"[{tf}] ➤ scenario: {voce['direzione']} | punteggio: {voce['punteggio']} | delta: {voce['delta']} | forze: {voce['forze']}\n"

    df = pd.DataFrame([{
        "Coin": coin,
        "Timeframe": tf,
        "Punteggio": voce["punteggio"],
        "Direzione": voce["direzione"],
        "Scenario": voce["direzione"],
        "Delta": voce["delta"],
        "Scenario finale": risultato.get("scenario_finale", "n/d")
    } for tf, voce in riepilogo_tf.items()])
    os.makedirs(PATH_ANALISI_FINALI, exist_ok=True)
    df.to_csv(os.path.join(PATH_ANALISI_FINALI, f"classifica_{coin}.csv"), sep=";", index=False)

    indicatori_tf = [x for tf in per_tf for x in risultato.get(tf, []) if x.get("indicatore") in ["MACD", "RSI", "EMA 21", "STOCH"]]
    riepilogo_globale = calcola_riepilogo_totale(lista_indicatori)
    b_commento = "# === COMMENTO CASSANDRA ===\n" + genera_commento_finale_avanzato(
    indicatori_per_tf, meta_info=meta_dati_finali or {}
    )
    b_scenari = blocco_scenari_per_tf(lista_indicatori)
    b_commento_scenari = blocco_commento_scenari(lista_indicatori)
    b_binance = blocco_dati_binance(coin)
    b_sr = blocco_supporti_resistenze(lista_indicatori, coin)
    b_grezzi = blocco_dati_grezzi(lista_indicatori)

    # === Riassunto per ogni TF (solo per cassandra finale) ===
    lista_tf_ordinata = [tf for tf in ["1m", "3m", "5m", "15m", "30m", "1h", "2h", "4h", "6h", "8h", "12h", "1d", "3d", "1w", "1M"] if tf in meta_dati_finali["timeframes"]]
    riassunti_per_tf = {tf: genera_riassunto_blocchi(lista_indicatori, meta_dati_finali, coin, tf=tf) for tf in lista_tf_ordinata}
    riassunto_finale = "\n\n----------------------------------------\n\n".join([r["commento_riassuntivo"] for r in riassunti_per_tf.values()])

    return {
        "blocco_info": b_info,
        "riassunto_multi_tf": riassunto_multi_tf, #tenere
        "blocco_tf": b_tf,
        "blocco_tech": b_tech,
        "blocco_globale": b_globale,
        "blocco_riepilogo_tf": b_riepilogo_tf, #questo serve
        
        "riassunto_per_tf": riassunti_per_tf,
        "blocco_commento": b_commento, 
        "blocco_scenari": b_scenari, #utile solo se viene fatta divisione fra direzione
        "blocco_commento_scenari": b_commento_scenari, #utile solo in caso di analisi statistica
        "blocco_forti": b_forti,
        "blocco_binance": b_binance, #servono solo se passati ad ai
        "blocco_supporti_resistenze": b_sr,
        "blocco_grezzi": b_grezzi, #servono solo se passati ad ai
        "risultato_finale": risultato,
        "riassunto_finale": riassunto_finale        
    }
