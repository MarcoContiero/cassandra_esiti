def calcola_range_ingresso(lista_indicatori_tf: list) -> str:
    """
    Calcola un range d'ingresso suggerito per il timeframe, basato su:
    - FVG
    - EMA21 / EMA50
    - Supporti/Resistenze forti
    """
    # === 1. Cerca FVG ===
    for ind in lista_indicatori_tf:
        if ind.get("indicatore", "").upper() == "FVG":
            valore = str(ind.get("valore", "")).replace(" ", "")
            if "-" in valore and any(x in valore.lower() for x in ["long", "short"]):
                return valore.split(":")[-1] if ":" in valore else valore

    # === 2. EMA 21 e 50 ===
    ema21 = None
    ema50 = None

    for ind in lista_indicatori_tf:
        nome = ind.get("indicatore", "").upper()
        if nome == "EMA 21":
            ema21 = ind.get("valore")
        elif nome == "EMA 50":
            ema50 = ind.get("valore")

    try:
        if isinstance(ema21, (int, float)) and isinstance(ema50, (int, float)):
            minimo = round(min(ema21, ema50), 2)
            massimo = round(max(ema21, ema50), 2)
            return f"{minimo}–{massimo}"
    except:
        pass

    # === 3. Supporti e resistenze forti ===
    supporti = []
    resistenze = []

    for ind in lista_indicatori_tf:
        if ind.get("indicatore", "").lower() == "supporto" and ind.get("forza", 0) >= 5:
            supporti.append(ind.get("valore"))
        elif ind.get("indicatore", "").lower() == "resistenza" and ind.get("forza", 0) >= 5:
            resistenze.append(ind.get("valore"))

    # Prendi i livelli più vicini al prezzo se disponibili
    if supporti and resistenze:
        try:
            minimo = round(min(supporti), 2)
            massimo = round(max(resistenze), 2)
            return f"{minimo}–{massimo}"
        except:
            pass

    # === Default ===
    return "n.d."
