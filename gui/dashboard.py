
import streamlit as st
from gui.gui_analisi_coin import interfaccia_analisi_coin
from gui.gui_classifica import interfaccia_classifica

def main():
    st.title("📊 Cassandra - Analisi Tecnica Multi-Coin")

    scelta = st.selectbox("Seleziona modalità:", [
        "Seleziona...",
        "🔍 Analisi Tecnica Singola",
        "📊 Classifica Tecnica Multi-Coin"
    ])

    if scelta == "🔍 Analisi Tecnica Singola":
        interfaccia_analisi_coin()
    elif scelta == "📊 Classifica Tecnica Multi-Coin":
        interfaccia_classifica()
