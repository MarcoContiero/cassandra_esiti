
def valuta_momentum(indicatori: list, tf: str) -> dict:
    """
    Analizza la forza del momentum aggregando gli indicatori rilevanti.
    Determina se c'è accelerazione, perdita di forza o divergenze in atto.

    Ogni indicatore deve avere:
    - "indicatore": nome
    - "scenario": descrizione (es. "in crescita", "divergenza", "ipercomprato", etc.)
    - "punteggio": forza direzionale numerica
    - "direzione": "long" / "short" / "neutro"
    """

    total = {"long": 0, "short": 0, "neutro": 0}
    scenari = []
    divergenze = []
    direzioni_forti = []

    for ind in indicatori:
        dir = ind.get("direzione", "neutro")
        punteggio = ind.get("punteggio", 0)
        scenario = ind.get("scenario", "").lower()
        nome = ind.get("indicatore", "")

        total[dir] += punteggio
        scenari.append(f"{nome}: {scenario}")

        if "divergenza" in scenario:
            divergenze.append(nome)

        if punteggio >= 3:
            direzioni_forti.append((nome, dir, punteggio))

    direzione_prevalente = max(total, key=total.get)
    delta = abs(total["long"] - total["short"])

    # Classificazione momentum
    if delta >= 5 and total[direzione_prevalente] >= 6:
        forza = "forte"
    elif delta >= 3:
        forza = "moderata"
    else:
        forza = "debole"

    # Costruzione commento
    commento = f"Sul timeframe {tf}, il momentum è {forza} e prevale la direzione {direzione_prevalente}."

    if direzioni_forti:
        forti = ", ".join([f"{n} ({d})" for n, d, _ in direzioni_forti])
        commento += f" Indicatori con segnali forti: {forti}."

    if divergenze:
        div_txt = ", ".join(divergenze)
        commento += f" ⚠️ Divergenze rilevate su: {div_txt}."

    alert = forza != "debole" or bool(divergenze)

    return {
        "commento": commento,
        "momentum": forza,
        "direzione": direzione_prevalente,
        "divergenze": divergenze,
        "alert": alert,
        "timeframe": tf
    }
