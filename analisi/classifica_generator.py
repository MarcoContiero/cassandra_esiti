import os
import json
from collections import defaultdict
from analisi.analizza_coin_completa import analizza_coin_completa
from elaborazione.genera_blocchi_analisi_finale import genera_blocchi_analisi_finale

def esegui_classifica(lista_coin, timeframes=None, debug=False):
    risultati = []
    analisi_complete = {}

    for coin in lista_coin:
        print(f"🔍 Analisi in corso per {coin}...")
        dati_coin = analizza_coin_completa(coin, timeframes=timeframes)

        # ✅ Verifica se esiste almeno un dato valido
        if not dati_coin or not isinstance(dati_coin, list) or len(dati_coin) == 0:
            print(f"⚠️ Analisi vuota o non valida per {coin}, salto.")
            continue

        analisi_complete[coin] = dati_coin

        try:
            blocchi = genera_blocchi_analisi_finale(coin, dati_coin, salva_file=True)
            risultati.append({
                "coin": coin,
                "punteggio": blocchi["risultato_finale"]["scenario_finale"]["punteggio_totale"],
                "direzione": blocchi["risultato_finale"]["scenario_finale"]["valore"],
                "file": blocchi.get("file_analisi", "")
            })
        except Exception as e:
            print(f"❌ Errore durante la generazione dei blocchi per {coin}: {e}")
            continue

    if not risultati:
        print("⚠️ Nessun dato valido ricevuto per la classifica finale.")
        return []

    # Ordina per punteggio decrescente
    risultati.sort(key=lambda x: x["punteggio"], reverse=True)
    return risultati
