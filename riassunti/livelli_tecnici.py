
def analizza_livelli_tecnici(prezzo: float, livelli: dict, tf: str) -> dict:
    """
    Analizza la posizione del prezzo rispetto a livelli tecnici chiave.
    Restituisce un commento strategico, livello attivo, tipo di setup e alert.

    livelli = {
        "supporti": [float, ...],
        "resistenze": [float, ...]
    }
    """

    supporti = sorted(livelli.get("supporti", []), reverse=True)  # dal più vicino in alto
    resistenze = sorted(livelli.get("resistenze", []))  # dal più vicino in basso

    commento = ""
    livello_attivo = "n/d"
    tipo_setup = "n/d"
    alert = False
    distanza = None

    # Trova supporto sotto e resistenza sopra
    supporto_attivo = next((s for s in supporti if s < prezzo), None)
    resistenza_attiva = next((r for r in resistenze if r > prezzo), None)

    if supporto_attivo and resistenza_attiva:
        distanza_supporto = abs(prezzo - supporto_attivo)
        distanza_resistenza = abs(resistenza_attiva - prezzo)

        distanza = min(distanza_supporto, distanza_resistenza)

        if distanza_resistenza < 0.01 * prezzo:
            livello_attivo = "resistenza"
            tipo_setup = "vicino a breakout rialzista"
            commento = f"Il prezzo su {tf} è molto vicino alla resistenza a {resistenza_attiva}. Una rottura potrebbe aprire spazio verso l'alto."
            alert = True
        elif distanza_supporto < 0.01 * prezzo:
            livello_attivo = "supporto"
            tipo_setup = "vicino a breakdown ribassista"
            commento = f"Il prezzo su {tf} è molto vicino al supporto a {supporto_attivo}. Una rottura potrebbe generare pressione ribassista."
            alert = True
        else:
            livello_attivo = "range"
            tipo_setup = "in congestione"
            commento = f"Il prezzo su {tf} è compreso tra il supporto a {supporto_attivo} e la resistenza a {resistenza_attiva}. Attendere una rottura per conferme."
            alert = False

    elif resistenza_attiva:
        distanza = abs(resistenza_attiva - prezzo)
        livello_attivo = "resistenza"
        tipo_setup = "lontano dalla resistenza"
        commento = f"Prossima resistenza su {tf} a {resistenza_attiva}, ma il prezzo è ancora distante."
        alert = False

    elif supporto_attivo:
        distanza = abs(prezzo - supporto_attivo)
        livello_attivo = "supporto"
        tipo_setup = "lontano dal supporto"
        commento = f"Prossimo supporto su {tf} a {supporto_attivo}, ma il prezzo è ancora distante."
        alert = False

    else:
        livello_attivo = "nessuno"
        tipo_setup = "nessun livello rilevante"
        commento = f"Il prezzo su {tf} non è vicino a supporti o resistenze noti."
        alert = False

    return {
        "commento": commento,
        "livello_attivo": livello_attivo,
        "tipo_setup": tipo_setup,
        "distanza_prossimo_livello": distanza,
        "alert": alert,
        "timeframe": tf
    }
