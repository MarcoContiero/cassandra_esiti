def costruisci_riassunto_tecnico(dettagli_per_timeframe, direzione):
    if not dettagli_per_timeframe:
        return "⚠️ Nessun dettaglio disponibile."

    righe = [f"Scenario prevalente: {direzione}", "Indicatori significativi:"]
    for tf, dettagli in dettagli_per_timeframe.items():
        righe.append(f"• {tf.upper()}:")
        for nome, d in dettagli.get("indicatori", {}).items():
            direzione_ind = d.get("direzione", "n.d.")
            punteggio = d.get("punteggio", "n.d.")
            righe.append(f"   · {nome} → {direzione_ind} ({punteggio})")
    return "\n".join(righe)

def costruisci_riassunto_testuale(finale, indicatori_forti=None):
    """
    Crea un riassunto testuale dello scenario finale con dati chiave e indicatori forti opzionali.
    """
    if indicatori_forti is None:
        indicatori_forti = []

    direzione = finale.get("direzione") or finale.get("scenario", "n.d.").upper()
    punteggio = finale.get("punteggio_totale", 0)
    tf_dom = finale.get("timeframe_dominante", "n.d.")
    forza = finale.get("forza_vincente", 0)
    opposta = finale.get("forza_opposta", 0)
    delta = finale.get("delta_forza", 0)

    emoji = {
        "LONG": "📈",
        "SHORT": "📉",
        "NEUTRO": "⏸️",
        "N.D.": "⏸️"
    }.get(direzione, "⏸️")

    righe = [
        f"{emoji} Scenario finale: {direzione}",
        f"* 💪 Totale forza {direzione.lower()}: {forza}",
        f"* ⚔️ Forza opposta: {opposta}",
        f"* ➖ Delta forza: {delta}",
        f"* 📊 Punteggio totale: {punteggio}",
        f"* ⌛ Timeframe dominante: {tf_dom}"
    ]

    if indicatori_forti:
        righe.append("")
        righe.append("🌟 Indicatori forti:")
        for tf, nome in indicatori_forti:
            righe.append(f"· {tf} → {nome}")

    return "\n".join(righe)


def costruisci_riassunto_globale(finale):
    direzione = finale.get("direzione", "n.d.")
    punteggio = finale.get("punteggio_totale", 0)
    tf_dom = finale.get("timeframe_dominante", "n.d.")
    forza = finale.get("forza_vincente", 0)
    opposta = finale.get("forza_opposta", 0)
    delta = finale.get("delta_forza", 0)

    return (
        f"📈 Scenario finale: {direzione.upper()}  \n"
        f"💪 Totale forza {direzione.lower()}: {forza}  \n"
        f"⚔️ Forza opposta: {opposta}  \n"
        f"➖ Delta forza: {delta}  \n"
        f"📊 Punteggio totale: {punteggio}  \n"
        f"⌛ Timeframe dominante: {tf_dom}"
    )
