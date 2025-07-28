
import streamlit as st
import os
import json
from shared.config import PATH_ANALISI_GREZZE
from elaborazione.genera_blocchi_analisi_finale import genera_blocchi_analisi_finale
from analisi.scrivi_blocchi_analisi import scrivi_blocchi_analisi

def interfaccia_analisi_coin():
    st.header("🔎 Analisi Tecnica - Cassandra")

    nome_coin = st.text_input("Inserisci la coin (es. ETHUSDT):", "BTCUSDT").upper()
    timeframes = st.multiselect(
        "Seleziona i timeframe da analizzare (solo per scaricare i dati):",
        ["1m", "3m", "5m", "15m", "30m", "1h", "2h", "4h", "6h", "8h", "12h", "1d", "3d", "1w", "1M"],
        default=["15m", "1h", "4h", "1d", "1w"]
    )

    # Bottone per scaricare dati
    if st.button("📥 Scarica dati grezzi", key="scarica_dati"):
        from analisi.analizza_coin_light import scarica_dati_grezzi
        # Scarica dati grezzi
        grezzi_raw = scarica_dati_grezzi(nome_coin, timeframes)

        # Aggiungi timestamp
        from datetime import datetime
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        risultati_grezzi = {
            "dati": grezzi_raw,
            "_timestamp_download": timestamp,
            "timeframes": timeframes  # ✅ Aggiunta lista dei TF selezionati
        }

        # Salva file
        os.makedirs(PATH_ANALISI_GREZZE, exist_ok=True)
        path = os.path.join(PATH_ANALISI_GREZZE, f"{nome_coin.lower()}_grezzi.json")
        with open(path, "w") as f:
            json.dump(risultati_grezzi, f, indent=2, default=str)
        st.success(f"Dati grezzi salvati in: {path}")

    # Bottone per avviare analisi tecnica
    if st.button("🧠 Avvia analisi tecnica", key="avvia_analisi"):
        path = os.path.join(PATH_ANALISI_GREZZE, f"{nome_coin.lower()}_grezzi.json")
        if not os.path.exists(path):
            st.error("⚠️ Devi prima scaricare i dati grezzi.")
            return

        with open(path, "r") as f:
            risultati = json.load(f)

        with open("gruppi_indicatori.json", "r") as g:
            raw_mappa = json.load(g)
            mappa_gruppi = {k.strip().lower(): v for k, v in raw_mappa.items()}

        # Ricostruzione lista con gruppo + timeframe
        lista_con_gruppi = []
        timestamp_dati = risultati.get("_timestamp_download", "n.d.")
        dati_indicatori = risultati.get("dati", {})

        for tf, lista in dati_indicatori.items():
            for riga in lista:
                nome = riga.get("indicatore", "").strip().lower().replace(" ", "_")
                riga["gruppo"] = mappa_gruppi.get(nome, "core")
                riga["timeframe"] = tf
                lista_con_gruppi.append(riga)

        if not lista_con_gruppi:
            st.error("❌ Errore: lista_con_gruppi è vuota!")
            return

        st.json(lista_con_gruppi[0])

        # Genera blocchi e salva il file TXT
        from datetime import datetime
        data_analisi = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        data_dati = risultati.get("_timestamp_download", "n.d.")

        blocchi = genera_blocchi_analisi_finale(nome_coin, lista_con_gruppi, mappa_gruppi,
                                                salva_file=True, data_analisi=data_analisi, data_dati=data_dati)

        scrivi_blocchi_analisi(
            coin=nome_coin,
            blocchi=blocchi,
            path=f"analisi_{nome_coin}_completa.txt"
        )

        # Mostra blocchi in ordine
        st.subheader("📌 Info Generali")
        st.code(blocchi.get("blocco_info", "❌ Blocco mancante"))

        st.subheader("⏱️ Dettagli per Timeframe")
        st.code(blocchi.get("blocco_tf", "❌ Blocco mancante"))

        st.subheader("🧠 Riassunto Tecnico")
        st.code(blocchi.get("blocco_tech", "❌ Blocco mancante"))

        st.subheader("🌍 Riassunto Globale")
        st.code(blocchi.get("blocco_globale", "❌ Blocco mancante"))

        st.subheader("🗣️ Commento automatico")
        st.markdown(blocchi.get("blocco_commento", "❌ Blocco mancante"))

        st.subheader("🏦 Dati Binance")
        st.code(blocchi.get("blocco_binance", "❌ Blocco mancante"))

        st.subheader("💪 Indicatori Forti")
        st.code(blocchi.get("blocco_forti", "❌ Blocco mancante"))

        st.subheader("📊 Dati Grezzi per Timeframe")
        st.code(blocchi.get("blocco_grezzi", "❌ Blocco mancante"))

        st.subheader("🧱 Supporti e Resistenze")
        st.code(blocchi.get("blocco_supporti_resistenze", "❌ Blocco mancante"))

        # Pulsante download file .txt
        path_file = f"analisi_{nome_coin}_completa.txt"
        if os.path.exists(path_file):
            with open(path_file, "r") as f:
                contenuto = f.read()
            st.download_button(
                label="📄 Scarica Analisi Completa (TXT)",
                data=contenuto,
                file_name=os.path.basename(path_file),
                mime="text/plain",
                key="download_txt"
            )
