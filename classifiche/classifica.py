import os
import json
import pandas as pd
from datetime import datetime
import streamlit as st
from analisi.analizza_coin_completa import analizza_coin_completa

def genera_classifica_finale(lista_coin: list[str], timeframes: list[str]) -> pd.DataFrame:
    risultati = []

    for coin in lista_coin:
        try:
            st.write(f"🔍 Analisi per `{coin}`...")
            analisi = analizza_coin_completa(coin, timeframes)

            # Protezione: analisi deve essere un dizionario valido
            if not isinstance(analisi, dict):
                st.warning(f"⚠️ Analisi non valida per {coin}. Skippata.")
                st.write(f"🧪 DEBUG ➤ tipo: {type(analisi)} — contenuto: {str(analisi)[:150]}")
                continue

            riga = {"Coin": coin}
            punteggio_totale = 0
            blocco_riepilogo = analisi.get("blocco_riepilogo_tf", {})

            for tf in timeframes:
                scenario = "n/d"
                punteggio = 0
                direzione = "n/d"
                delta = "n/d"

                riepilogo = blocco_riepilogo.get(tf, "")
                if "➤" in riepilogo:
                    scenario = riepilogo.split("➤")[1].split("|")[0].strip()
                if "|" in riepilogo:
                    parti = [x.strip() for x in riepilogo.split("|")]
                    for p in parti:
                        if p.lower().startswith("punteggio:"):
                            try:
                                punteggio = int(p.split(":")[1].strip())
                            except:
                                pass
                        elif p.lower().startswith("direzione:"):
                            direzione = p.split(":")[1].strip()
                        elif p.lower().startswith("range:"):
                            delta = p.split(":")[1].strip()

                riga[f"Punteggio_{tf}"] = punteggio
                riga[f"Direzione_{tf}"] = direzione
                riga[f"Scenario_{tf}"] = scenario
                riga[f"Delta_{tf}"] = delta
                punteggio_totale += punteggio

            riga["Totale"] = punteggio_totale
            risultati.append(riga)

        except Exception as e:
            st.error(f"❌ Errore durante l'analisi di {coin}: {e}")

    # === Costruzione finale e salvataggio ===
    df = pd.DataFrame(risultati)

    if not df.empty and "Totale" in df.columns:
        df = df.sort_values(by="Totale", ascending=False).reset_index(drop=True)

        os.makedirs("analisi_finali", exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        nome_file = f"analisi_finali/classifica_{timestamp}.csv"
        df.to_csv(nome_file, sep=";", index=False)

        st.success(f"✅ Classifica salvata: `{nome_file}`")
    else:
        st.warning("⚠️ Classifica vuota: nessun dato utile generato.")

    return df
