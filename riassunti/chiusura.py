
def genera_blocco_chiusura(chiusura: float, tf: str, livelli: dict) -> dict:
    """
    Analizza la chiusura rispetto a livelli tecnici chiave e restituisce un commento strategico,
    uno scenario e un flag 'alert' per indicare potenziale setup in formazione.

    livelli = {
        "massimo": float,
        "minimo": float,
        "resistenza": float,
        "supporto": float,
        "ema": float,
        "bollinger_sup": float,
        "bollinger_inf": float
    }
    """

    livelli = livelli or {}

    elementi_rotti = []
    scenario = "neutro"
    alert = False

    # Frasi da costruire
    frasi = []

    # Confronti
    if "massimo" in livelli and chiusura > livelli["massimo"]:
        elementi_rotti.append("massimo precedente")
        frasi.append("sopra il massimo precedente")
    if "minimo" in livelli and chiusura < livelli["minimo"]:
        elementi_rotti.append("minimo precedente")
        frasi.append("sotto il minimo precedente")
    if "resistenza" in livelli and chiusura > livelli["resistenza"]:
        elementi_rotti.append("resistenza")
        frasi.append("sopra la resistenza")
    if "supporto" in livelli and chiusura < livelli["supporto"]:
        elementi_rotti.append("supporto")
        frasi.append("sotto il supporto")
    if "ema" in livelli and chiusura > livelli["ema"]:
        elementi_rotti.append("EMA")
        frasi.append("sopra la media mobile")
    if "ema" in livelli and chiusura < livelli["ema"]:
        frasi.append("sotto la media mobile")
    if "bollinger_sup" in livelli and chiusura > livelli["bollinger_sup"]:
        elementi_rotti.append("banda superiore")
        frasi.append("fuori dalla banda superiore di Bollinger")
    if "bollinger_inf" in livelli and chiusura < livelli["bollinger_inf"]:
        elementi_rotti.append("banda inferiore")
        frasi.append("fuori dalla banda inferiore di Bollinger")

    # Determinazione scenario
    if any(x in elementi_rotti for x in ["massimo precedente", "resistenza", "EMA", "banda superiore"]):
        scenario = "rialzista"
        alert = True
    elif any(x in elementi_rotti for x in ["minimo precedente", "supporto", "banda inferiore"]):
        scenario = "ribassista"
        alert = True
    else:
        scenario = "neutro"
        alert = False

    # Costruzione commento
    if frasi:
        commento = f"La chiusura {tf} è avvenuta " + ", ".join(frasi) + "."
        if alert:
            commento += f" Possibile scenario {scenario} in formazione."
    else:
        commento = f"La chiusura {tf} non evidenzia segnali tecnici rilevanti."

    return {
        "commento": commento,
        "scenario": scenario,
        "alert": alert,
        "elementi_rotti": elementi_rotti,
        "timeframe": tf
    }

