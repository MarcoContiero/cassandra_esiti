from collections import Counter

def calcola_score_timeframe(risultati_per_tf: dict) -> dict:
    score_per_tf = {}
    for tf, lista_indicatori in risultati_per_tf.items():
        if not isinstance(lista_indicatori, list):
            print(f"⚠️ ERRORE: {tf} non è una lista! ➤ {type(lista_indicatori)}")
            continue
        punteggio_totale = 0
        direzioni = []
        for indicatore in lista_indicatori:
            punteggio = indicatore.get("punteggio", 0)
            direzione = indicatore.get("direzione", "neutro")
            if isinstance(punteggio, (int, float)):
                punteggio_totale += punteggio
            if isinstance(direzione, str):
                direzioni.append(direzione.lower())
        direzione_dominante = Counter(direzioni).most_common(1)[0][0] if direzioni else "neutro"
        score_per_tf[tf] = {
            "punteggio": punteggio_totale,
            "direzione": direzione_dominante,
            "dettagli": lista_indicatori
        }
    return score_per_tf

def calcola_score_globale(score_per_tf: dict, pesi_tf: dict = None) -> dict:
    if pesi_tf is None:
        pesi_tf = {"15m": 1, "1h": 1, "4h": 2, "1d": 3, "1w": 2}
    totale_punteggio = 0
    somma_pesi = 0
    direzioni_pesate = []
    for tf, dati in score_per_tf.items():
        peso = pesi_tf.get(tf, 1)
        totale_punteggio += dati["punteggio"] * peso
        somma_pesi += peso
        direzioni_pesate.extend([dati["direzione"]] * peso)
    media = round(totale_punteggio / somma_pesi, 2) if somma_pesi > 0 else 0
    direzione_finale = Counter(direzioni_pesate).most_common(1)[0][0] if direzioni_pesate else "neutro"
    return {"score": media, "direzione": direzione_finale}

