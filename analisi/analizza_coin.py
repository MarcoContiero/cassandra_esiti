import streamlit as st
import os
import pandas as pd

from shared.riassunti import costruisci_riassunto_tecnico
from indicatori.core.calcola_scenario_finale import calcola_scenario_finale
from analisi.analizza_tutti_indicatori import analizza_tutti_indicatori
from indicatori.core.multi_timeframe import costruisci_blocco_multi_tf
from utils.salva_analisi_completa import salva_analisi_completa
from shared.caricamento import carica_dati
from dati.downloader import scarica_ohlcv_binance


def analizza_coin(nome_coin: str, timeframes: list, usa_streamlit=True):
    if usa_streamlit:
        st.markdown(f"## 📊 Analisi per {nome_coin}")
    
    dfs = {}
    risultati_grezzi = {}
    risultati_completi = {}
    scenari_per_tf = {}
    dati_ohlcv_per_timeframe = {}
    dati_grezzi = {}

    for tf in timeframes:
        print(f"⏱️ Timeframe: {tf}")
        df = carica_dati(nome_coin, tf)

        if df is not None and not df.empty:
            csv_path = f"dati_csv/{nome_coin.upper()}_{tf}.csv"
            os.makedirs("dati_csv", exist_ok=True)
            df.to_csv(csv_path, sep=";", decimal=",", index=False)
            print(f"✅ Salvato: {csv_path}")
            dfs[tf] = df
            dati_ohlcv_per_timeframe[tf] = df
        else:
            print(f"❌ Errore: Nessun dato restituito per {nome_coin} - {tf}")
            dati_grezzi[tf] = {}
            print(f"\n🔍 Input dati grezzi:\n{dati_grezzi}")
            print("\n⚠️ Nessun dato normalizzabile trovato.")
            return None


    # 🔽 Poi procedi con il resto del codice (analisi tecnica ecc.)
    for tf in timeframes:
        try:
            if usa_streamlit:
                st.markdown(f"### ⏱️ Timeframe: {tf}")
            risultato = analizza_tutti_indicatori(nome_coin, [tf])
            if risultato is None:
                if usa_streamlit:
                    st.warning(f"⚠️ Nessun dato per {tf}")
                    continue

            dfs[tf] = risultato["df"]
            risultati_grezzi[tf] = risultato["risultati_grezzi"]
            risultati_completi[tf] = {
                "core": risultato["risultati_completi"]
            }
            scenari_per_tf[tf] = risultato["multi_tf"]
        except Exception as e:
            if usa_streamlit:
                st.error(f"❌ Errore durante l'analisi del timeframe {tf}: {e}")
    if not scenari_per_tf:
        return None



    try:
        finale = calcola_scenario_finale(nome_coin, dfs, scenari_per_tf)
    except Exception as e:
        print(f"❌ Errore nel calcolo dello scenario finale: {e}")
        return None



    # === COSTRUISCI DETTAGLI PER TIMEFRAME ===

    if isinstance(scenari_per_tf, list):
        scenari_per_tf = {item['timeframe']: item for item in scenari_per_tf if 'timeframe' in item}


    try:
        dettagli_per_timeframe, punteggi_per_timeframe = costruisci_blocco_multi_tf(scenari_per_tf)
    except Exception as e:
        print(f"⚠️ Errore nel calcolo multi-timeframe: {e}")
        dettagli_per_timeframe, punteggi_per_timeframe = {}, {}

    try:
        for tf, riga in risultati_completi.items():
            riassunto_tecnico = costruisci_riassunto_tecnico(risultati_completi, finale.get("direzione", "n/d"))
    except Exception as e:
        if usa_streamlit:
            st.error(f"❌ Errore nella costruzione del riassunto tecnico: {e}")
            riassunto_tecnico = ""

    # Output finale formattato
    blocco = ""
    blocco += "# === INFO GENERALI ===\n"
    blocco += f"Coin: {nome_coin}\n"
    blocco += f"Scenario finale: {finale.get('scenario', 'n/d')}\n"
    blocco += f"Punteggio totale: {finale.get('punteggio', 0)}\n"
    blocco += f"Forza vincente: {finale.get('forza_vincente', 0)}\n"
    blocco += f"Forza opposta: {finale.get('forza_opposta', 0)}\n"
    blocco += f"Delta forza: {finale.get('delta_forza', 0)}\n"
    blocco += f"Timeframe dominante: {finale.get('dominante', 'n/d')}\n"

    blocco += "\n# === DETTAGLI PER TIMEFRAME ===\n"
    for tf in timeframes:
        multi = scenari_per_tf.get(tf, {})
        blocco += f"[{tf}] → direzione: {multi.get('direzione', 'n/d')}, "
        blocco += f"long: {multi.get('long', 0)}, short: {multi.get('short', 0)}\n"

    blocco += "\n# === RIASSUNTO TECNICO ===\n"
    blocco += riassunto_tecnico + "\n"

    blocco += "\n# === RIASSUNTO GLOBALE ===\n"
    blocco += f"Considerazioni: 🚀 Scenario finale: 📈 {finale.get('scenario', 'n/d').upper()}\n"
    blocco += f"* 💪 Totale forza {finale.get('scenario', '')}: {finale.get('forza_vincente', 0)}\n"
    blocco += f"* ⚔️ Forza opposta: {finale.get('forza_opposta', 0)}\n"
    blocco += f"* ➖ Delta forza: {finale.get('delta_forza', 0)}\n"
    blocco += f"* 📊 Punteggio totale: {finale.get('punteggio', 0)}\n"
    blocco += "Timeframes considerati:\n"
    for tf in timeframes:
        multi = scenari_per_tf.get(tf, {})
        blocco += f"• {tf} → {multi.get('direzione', 'n/d')} ({multi.get(multi.get('direzione', 'long'), 0)})\n"

    if finale.get("indicatori_forti"):
        blocco += f"💥 Indicatori forti: {', '.join(finale['indicatori_forti'])}\n"
    else:
        blocco += "⚠️ Nessun indicatore forte rilevato.\n"

    blocco += f"{finale.get('testo_finale', '')}\n"

    if usa_streamlit:
        st.code(blocco)


    # Ricostruzione aggregata per salvataggio
    risultato = {
        'core': [],
        'optional': [],
        'extra': [],
    }
    for tf in risultati_completi:
        for gruppo in ['core', 'optional', 'extra']:
            risultato[gruppo].extend(risultati_completi[tf].get(gruppo, []))
    risultato['multi_tf'] = finale

    salva_analisi_completa(nome_coin, risultato)

    return blocco
