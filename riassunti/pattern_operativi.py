
def analizza_pattern_operativi(patterns: list, tf: str) -> dict:
    """
    Analizza i pattern tecnici rilevati sul timeframe dato.
    Ogni pattern contiene:
    - "nome": nome del pattern (es. "engulfing", "hammer")
    - "direzione": "long" / "short" / "neutro"
    - "validita": True / False
    - "note": opzionale (es. "conferma con volume")

    Restituisce un commento strategico e un alert se pattern forti sono presenti.
    """

    validi_long = [
        p for p in patterns
        if isinstance(p, dict) and p.get("validita") and p.get("direzione") == "long"
    ]

    validi_short = [
        p for p in patterns
        if isinstance(p, dict) and p.get("validita") and p.get("direzione") == "short"
    ]

    neutri = [
        p for p in patterns
        if isinstance(p, dict) and p.get("validita") and p.get("direzione") == "neutro"
]
    total_validi = len(validi_long) + len(validi_short) + len(neutri)

    if total_validi == 0:
        return {
            "commento": f"Nessun pattern tecnico rilevante su {tf}.",
            "pattern_rilevati": [],
            "direzione": "neutro",
            "alert": False,
            "timeframe": tf
        }

    # Determina direzione prevalente
    if len(validi_long) > len(validi_short):
        direzione = "long"
    elif len(validi_short) > len(validi_long):
        direzione = "short"
    else:
        direzione = "neutro"

    pattern_attivi = validi_long + validi_short + neutri
    nomi_pattern = [p["nome"] for p in pattern_attivi]

    frasi_pattern = []
    for p in pattern_attivi:
        frase = p["nome"]
        if "note" in p and p["note"]:
            frase += f" ({p['note']})"
        frasi_pattern.append(frase)

    commento = f"Pattern attivi su {tf}: " + ", ".join(frasi_pattern) + "."
    if direzione != "neutro":
        commento += f" Prevale una lettura {direzione}."

    alert = direzione != "neutro"

    return {
        "commento": commento,
        "pattern_rilevati": nomi_pattern,
        "direzione": direzione,
        "alert": alert,
        "timeframe": tf
    }
