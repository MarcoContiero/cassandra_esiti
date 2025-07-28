import streamlit as st
import pandas as pd
import os
from glob import glob
from classifiche.classifica import genera_classifica_finale

def interfaccia_classifica():
    st.header("📊 Classifica Tecnica - Cassandra")

    # === Carica lista di default da file ===
    def carica_lista_default():
        path_lista = os.path.join(os.path.dirname(__file__), "..", "lista_coin.txt")
        try:
            with open(path_lista, "r") as f:
                return [r.strip().upper() for r in f if r.strip()]
        except FileNotFoundError:
            st.warning("⚠️ File 'lista_coin.txt' non trovato. Uso lista di default.")
            return ["BTCUSDT", "ETHUSDT", "XRPUSDT"]

    lista_default = carica_lista_default()

    # === Pulsanti gestione lista ===
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔄 Reset lista coin (da file)", key="reset_coin"):
            st.session_state["lista_coin"] = lista_default.copy()
            st.success("✅ Lista ripristinata da 'lista_coin.txt'")
    with col2:
        if st.button("🧹 Svuota lista coin", key="clear_coin"):
            st.session_state["lista_coin"] = []
            st.success("✅ Lista completamente azzerata")

    # === Inizializza lista coin se assente ===
    if "lista_coin" not in st.session_state:
        st.session_state["lista_coin"] = lista_default.copy()

    # === Aggiunta manuale ===
    nuova_coin = st.text_input("➕ Aggiungi coin manualmente (es. BTCUSDT o BTCUSDT, ETHUSDT)")
    if nuova_coin:
        nuove = [c.strip().upper() for c in nuova_coin.split(",") if c.strip()]
        for coin in nuove:
            if coin not in st.session_state["lista_coin"]:
                st.session_state["lista_coin"].append(coin)

    lista_coin = st.session_state["lista_coin"]
    st.markdown(f"✅ Coin selezionate: `{', '.join(lista_coin)}`")

    # === Selezione timeframe ===
    timeframes = st.multiselect(
        "⏱️ Timeframe da analizzare",
        options=["1m", "3m", "5m", "15m", "30m", "1h", "2h", "4h", "6h", "8h", "12h", "1d", "3d", "1w", "1M"],
        default=["1h", "4h", "1d"]
    )

    # === Avvio generazione ===
    if "genera" not in st.session_state:
        st.session_state["genera"] = False

    if st.button("📈 Genera Classifica", disabled=len(lista_coin) == 0):
        st.session_state["genera"] = True

    if st.session_state["genera"]:
        with st.spinner("⏳ Analisi in corso..."):
            df_result = genera_classifica_finale(lista_coin, timeframes)

        if df_result is not None and not df_result.empty:
            nome_file = "classifica_tabella.csv"
            csv_bytes = df_result.to_csv(index=False, sep=";").encode("utf-8")

            st.success("✅ Analisi completata. Classifica generata.")
            st.download_button(
                label="📥 Download completato automaticamente",
                data=csv_bytes,
                file_name=nome_file,
                mime="text/csv",
                key="auto_download"
            )
            st.stop()
        else:
            st.warning("⚠️ Nessun risultato da esportare.")
        st.session_state["genera"] = False

    # === Visualizzazione risultati ===
    st.markdown("---")
    st.subheader("📄 Classifica finale unificata")

    path_dir = "analisi_finali"
    pattern = os.path.join(path_dir, "classifica_*.csv")
    files = glob(pattern)

    if not files:
        st.warning("⚠️ Nessun file classifica trovato. Esegui prima almeno un'analisi.")
        return

    df_list = []
    for file in files:
        try:
            df = pd.read_csv(file, sep=";")
            df_list.append(df)
        except Exception as e:
            st.error(f"Errore leggendo {file}: {e}")

    if not df_list:
        st.warning("⚠️ Nessun dato valido trovato nei file CSV.")
        return

    df_all = pd.concat(df_list, ignore_index=True)

    # === Pulsante per scaricare l'ultimo file CSV grezzo ===
    files_ordinati = sorted(files, key=os.path.getmtime, reverse=True)
    ultimo_file = files_ordinati[0] if files_ordinati else None
    if ultimo_file:
        with open(ultimo_file, "rb") as f:
            st.download_button(
                label="📥 Scarica ultima classifica (grezza)",
                data=f,
                file_name=os.path.basename(ultimo_file),
                mime="text/csv"
            )

    # === Pivot per visualizzazione finale ===
    campi = ["Punteggio", "Direzione", "Scenario", "Delta"]
    pivot = df_all.pivot_table(
        index="Coin",
        columns="Timeframe",
        values=campi,
        aggfunc="first"
    )

    pivot.columns = [f"{col[1]}_{col[0]}" for col in pivot.columns]
    pivot.reset_index(inplace=True)
    pivot = pivot.drop(columns=[c for c in pivot.columns if "Scenario finale" in c], errors="ignore")

    punteggi = [col for col in pivot.columns if col.endswith("_Punteggio")]
    if punteggi:
        pivot["Totale"] = pivot[punteggi].sum(axis=1)
        pivot = pivot.sort_values(by="Totale", ascending=False)

    # === Evidenzia la top coin
    def evidenzia_top(df):
        max_score = df["Totale"].max()
        return df.style.apply(
            lambda row: ["background-color: lightgreen" if row["Totale"] == max_score else "" for _ in row],
            axis=1
        )

    st.dataframe(evidenzia_top(pivot), use_container_width=True)

    # === Scarica CSV tabella mostrata
    csv_pivot = pivot.to_csv(index=False, sep=";").encode("utf-8")
    st.download_button(
        label="📥 Scarica tabella mostrata",
        data=csv_pivot,
        file_name="classifica_tabella.csv",
        mime="text/csv"
    )
