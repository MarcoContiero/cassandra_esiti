# file: home.py
import streamlit as st
import pandas as pd
import requests
import json

st.set_page_config(page_title="Le Tre Moire", page_icon="🧶", layout="centered")

st.title("🧶 Le Tre Moire - Cassandra Autonoma")
st.caption("La versione riflessiva e profetica di Cassandra")

st.markdown("### 📘 Ultimo registro degli esiti")
try:
    # URL pubblico GCS oppure endpoint API che restituisce JSON
    url_log = "https://storage.googleapis.com/cassandra_backup_moire/log/registro_successi.json"
    response = requests.get(url_log)
    data = response.json()
    df = pd.DataFrame(data)
    df = df.sort_values("timestamp", ascending=False)
    st.dataframe(df.head(50), use_container_width=True)
except Exception as e:
    st.warning(f"⚠️ Impossibile caricare il registro: {e}")

st.markdown("---")
st.markdown("🌀 _Cloto tesse il passato, Lachesi misura il presente, Atropo giudica il futuro..._")
