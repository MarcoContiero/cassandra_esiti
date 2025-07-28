import pandas as pd
import json
from collections import defaultdict
from utils.salvataggio import salva_csv 
from shared.caricamento import carica_dati
from utils.get_funzioni_indicatori import get_funzioni_indicatori
import os
from shared.config import PATH_DATI_CSV
from dati.downloader import scarica_ohlcv_binance
from shared.interpreta_scenari import interpreta_scenario
from indicatori.extra.ta_lib_indicators import analizza_ta_lib

with open("gruppi_indicatori.json", "r") as f:
    gruppi_indicatori = json.load(f)

MIN_RIGHE_TF = 300

def scarica_dati_grezzi(coin, timeframes):
    risultati_completi = {}

    for tf in timeframes:
        df = scarica_ohlcv_binance(coin, tf, limit=1000)

        if len(df) < MIN_RIGHE_TF:
            continue

        # 🔥 Usa direttamente il DataFrame scaricato, senza salvare/caricare
        funzioni = get_funzioni_indicatori()
        risultati = []

        for nome, funzione in funzioni.items():
            try:
                risultato = funzione(df.copy(), tf)
                if isinstance(risultato, list):
                    risultati.extend(risultato)
                else:
                    risultati.append(risultato)
            except Exception as e:
                print(f"❌ Errore su {nome}: {e}")

        risultati_completi[tf] = risultati

    return risultati_completi

def analizza_coin_light(nome_coin: str, dati_grezzi: dict, flag_debug=False) -> dict:
    risultati_per_tf = {}
    funzioni = get_funzioni_indicatori()

    for tf, df in dati_grezzi.items():
        if isinstance(df, pd.DataFrame):
            print(f"📋 Colonne disponibili nel df: {df.columns.tolist()}")
        else:
            print(f"⚠️ Errore: per il timeframe {tf} ho ricevuto un oggetto di tipo {type(df)} ➤ {df}")
            continue

        print(f"📏 Lunghezza del df: {len(df)}")

        risultati = []
        indicatori_validi = []
        indicatori_scartati = []

        for i, (nome, fn) in enumerate(funzioni.items(), 1):
            print(f"[DEBUG #{i}] ➤ {nome}")

            if not callable(fn):
                print(f"⚠️ {nome} non è una funzione: tipo {type(fn)}, saltato.")
                indicatori_scartati.append((nome, "non callable"))
                continue

            try:
                res = fn(df.copy(), tf)
                if not isinstance(res, dict):
                    print(f"⚠️ {nome} restituisce {type(res).__name__}, atteso dict. Ignorato.")
                    indicatori_scartati.append((nome, f"type: {type(res).__name__}"))
                    continue

                if res.get("scenario") == "errore" and not flag_debug:
                    print(f"⚠️ {nome} restituisce scenario=errore ➤ scartato.")
                    indicatori_scartati.append((nome, "scenario=errore"))
                    continue

                res["indicatore"] = nome
                res["timeframe"] = tf
                res["gruppo"] = gruppi_indicatori.get(nome, "n/d")
                res["punteggio"] = res.get("punteggio", 0)
                
                try:
                    res["scenario"] = interpreta_scenario(res)
                except Exception as e:
                    print(f"⚠️ Errore nel calcolo scenario per {nome}: {e}")
                    res["scenario"] = "n.d."

                risultati.append(res)
                indicatori_validi.append(nome)
                print(f"✅ {nome} → OK")

            except Exception as e:
                print(f"❌ Errore in {nome}: {e}")
                indicatori_scartati.append((nome, f"errore: {str(e)}"))

        print("\n🧮 Indicatori validi:", indicatori_validi)
        print("🧹 Indicatori scartati:", indicatori_scartati)
        print(f"✅ Totali OK: {len(indicatori_validi)} / ❌ Scartati: {len(indicatori_scartati)}")
                # ➕ Aggiunta indicatori TA-Lib
        try:
            risultati_ta = analizza_ta_lib(df.copy(), tf)
            risultati.extend(risultati_ta)
            print(f"📌 TA-LIB ➤ {len(risultati_ta)} indicatori aggiunti.")
        except Exception as e:
            print(f"❌ Errore TA-LIB ➤ {e}")
        risultati_per_tf[tf] = risultati
        print(f"📦 Totale risultati trovati per {tf}: {len(risultati)}")

    print(f"\n🧾 DEBUG_SCARICA ➤ risultati_per_tf finale:\n{risultati_per_tf}")
    return risultati_per_tf
