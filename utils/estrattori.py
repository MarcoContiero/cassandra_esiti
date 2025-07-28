import json
import os

# Carica la mappa dei punteggi massimi
with open("punteggi_massimi_indicatori.json", "r") as f:
    punteggi_massimi = json.load(f)

def estrai_indicatori_forti(blocco):
    """
    Estrae gli indicatori forti (con punteggio elevato o massimo teorico).
    """
    indicatori_forti = []
    for gruppo in ["core", "optional"]:
        for indicatore in blocco.get(gruppo, []):
            nome = indicatore.get("nome") or indicatore.get("indicatore", "Sconosciuto")
            punteggio = indicatore.get("punteggio", 0)

            chiave = nome.strip().lower()
            max_teorico = punteggi_massimi.get(chiave, 10)

            if punteggio >= 8 or punteggio == max_teorico:
                indicatori_forti.append((nome, punteggio))
    return indicatori_forti

def get_timeframes_from_grezzo(path: str) -> list:
    import json
    try:
        with open(path, "r") as f:
            dati = json.load(f)
        return dati.get("timeframes", [])
    except Exception as e:
        print(f"⚠️ Errore nel caricamento dei timeframe da {path}: {e}")
        return []