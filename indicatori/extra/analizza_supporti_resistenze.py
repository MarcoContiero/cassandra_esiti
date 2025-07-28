import numpy as np
import pandas as pd
from scipy.signal import argrelextrema

def analizza_supporti_resistenze(df: pd.DataFrame, timeframe: str, nome_coin: str = None) -> list:
    risultati = []

    # Usa i prezzi di chiusura per semplificare
    chiusure = df["close"]
    prezzi = chiusure.values

    # Massimi e minimi locali (finestra 5 periodi)
    max_idx = argrelextrema(prezzi, np.greater, order=5)[0]
    min_idx = argrelextrema(prezzi, np.less, order=5)[0]

    livelli = []

    # Aggiungi massimi
    for i in max_idx:
        livelli.append({"prezzo": round(prezzi[i], 2), "tipo": "resistenza"})

    # Aggiungi minimi
    for i in min_idx:
        livelli.append({"prezzo": round(prezzi[i], 2), "tipo": "supporto"})

    # Raggruppa livelli vicini (±1%)
    raggruppati = {}
    soglia = 0.01  # 1%

    for lvl in livelli:
        prezzo = lvl["prezzo"]
        tipo = lvl["tipo"]
        trovato = False

        for key in raggruppati:
            if abs(prezzo - key) / key < soglia and tipo == raggruppati[key]["tipo"]:
                raggruppati[key]["count"] += 1
                trovato = True
                break

        if not trovato:
            raggruppati[prezzo] = {"prezzo": prezzo, "tipo": tipo, "count": 1}

    # Trasforma in lista e ordina per prezzo
    tutti = list(raggruppati.values())
    tutti.sort(key=lambda x: x["prezzo"])

    # Trova il prezzo attuale
    prezzo_attuale = prezzi[-1]

    # Separa supporti e resistenze
    supporti = [x for x in tutti if x["tipo"] == "supporto" and x["prezzo"] < prezzo_attuale]
    resistenze = [x for x in tutti if x["tipo"] == "resistenza" and x["prezzo"] > prezzo_attuale]

    # Ordina sempre per prezzo crescente
    supporti.sort(key=lambda x: x["prezzo"])
    resistenze.sort(key=lambda x: x["prezzo"])

    # Prendi i 3 più forti
    top_supporti = sorted(supporti, key=lambda x: -x["count"])[:3]
    top_resistenze = sorted(resistenze, key=lambda x: -x["count"])[:3]

    # Ripristina ordine per prezzo
    top_supporti.sort(key=lambda x: x["prezzo"])
    top_resistenze.sort(key=lambda x: x["prezzo"])

    # Supporti e resistenze intermedi
    intermedi_supporti = [x for x in supporti if x not in top_supporti]
    intermedi_resistenze = [x for x in resistenze if x not in top_resistenze]

    # ➤ Output finale
    for s in top_supporti:
        risultati.append({
            "indicatore": "Supporto",
            "timeframe": timeframe,
            "valore": s["prezzo"],
            "scenario": "principale",
            "punteggio": 0,
            "direzione": "neutro",
            "forza": s["count"]
        })

    for r in top_resistenze:
        risultati.append({
            "indicatore": "Resistenza",
            "timeframe": timeframe,
            "valore": r["prezzo"],
            "scenario": "principale",
            "punteggio": 0,
            "direzione": "neutro",
            "forza": r["count"]
        })

    for s in intermedi_supporti:
        risultati.append({
            "indicatore": "Supporto",
            "timeframe": timeframe,
            "valore": s["prezzo"],
            "scenario": "intermedio",
            "punteggio": 0,
            "direzione": "neutro",
            "forza": s["count"]
        })

    for r in intermedi_resistenze:
        risultati.append({
            "indicatore": "Resistenza",
            "timeframe": timeframe,
            "valore": r["prezzo"],
            "scenario": "intermedio",
            "punteggio": 0,
            "direzione": "neutro",
            "forza": r["count"]
        })

    return risultati
