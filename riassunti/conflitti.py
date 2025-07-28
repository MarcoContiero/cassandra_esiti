from collections import defaultdict

def valuta_conflitti(lista_indicatori: list, tf: str) -> dict:
    """
    Analizza i conflitti tra indicatori su un determinato timeframe.
    Rileva:
    - presenza di conflitto
    - livello di conflitto (basso, medio, alto)
    - direzione prevalente
    - indicatore dominante (con punteggio maggiore)
    - commento strategico
    """

    conteggio = defaultdict(int)
    punteggi = defaultdict(int)
    direzioni_valide = ["long", "short", "neutro"]

    for ind in lista_indicatori:
        direzione = ind.get("direzione", "neutro")
        punteggio = ind.get("punteggio", 0)
        nome = ind.get("indicatore", "sconosciuto")

        if direzione in direzioni_valide:
            conteggio[direzione] += 1
            punteggi[direzione] += punteggio

    # 🔒 Protezione contro dizionario vuoto
    if not punteggi:
        return {
            "nome": "Conflitti direzionali",
            "conflitto": False,
            "livello_conflitto": "n/d",
            "direzione_prevalente": "n/d",
            "indicatore_dominante": "n/d",
            "commento": f"Struttura priva di conflitti tra gli indicatori su {tf}.",
            "timeframe": tf
        }

    # ✅ Direzione prevalente per punti
    direzione_prevalente = max(punteggi, key=punteggi.get)

    # ✅ Indicatore dominante per punteggio singolo
    indicatore_dominante = None
    max_score = -1
    for ind in lista_indicatori:
        if ind.get("punteggio", 0) > max_score:
            max_score = ind["punteggio"]
            indicatore_dominante = ind["indicatore"]

    # ⚠️ Verifica conflitto tra long/short
    direzioni_non_neutre = [d for d in direzioni_valide if d != "neutro"]
    conteggi_effettivi = [conteggio[d] for d in direzioni_non_neutre]

    conflitto = abs(conteggi_effettivi[0] - conteggi_effettivi[1]) <= 2 and sum(conteggi_effettivi) > 2

    # 🔄 Livello conflitto
    if not conflitto:
        livello_conflitto = "basso"
    else:
        diff = abs(punteggi["long"] - punteggi["short"])
        if diff <= 2:
            livello_conflitto = "alto"
        elif diff <= 5:
            livello_conflitto = "medio"
        else:
            livello_conflitto = "basso"

    # 🧠 Commento finale
    if conflitto:
        commento = (
            f"Scenario {tf} contrastato: {conteggio['long']} indicatori long, "
            f"{conteggio['short']} short. "
            f"La direzione prevalente è {direzione_prevalente}, spinta soprattutto da {indicatore_dominante}. "
            f"Livello di conflitto: {livello_conflitto}."
        )
    else:
        commento = (
            f"Nessun conflitto rilevante su {tf}. "
            f"La maggioranza degli indicatori suggerisce direzione {direzione_prevalente}, "
            f"guidata da {indicatore_dominante}."
        )

    return {
        "nome": "Conflitti direzionali",
        "conflitto": conflitto,
        "livello_conflitto": livello_conflitto,
        "direzione_prevalente": direzione_prevalente,
        "indicatore_dominante": indicatore_dominante,
        "commento": commento,
        "timeframe": tf
    }
