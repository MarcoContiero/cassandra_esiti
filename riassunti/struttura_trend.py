def analizza_struttura_trend(hh, hl, lh, ll, tf: str) -> dict:
    """
    Analizza la struttura del trend tramite livelli:
    - HH (Higher High)
    - HL (Higher Low)
    - LH (Lower High)
    - LL (Lower Low)
    e determina la configurazione attuale (trend, range, transizione)
    """

    def normalizza_valore(val):
        if isinstance(val, list):
            return val[0] if val else None
        return val

    def formatta_valore(val):
        try:
            return f"{val:.2f}"
        except:
            return "n/d"

    # Normalizza input
    hh = normalizza_valore(hh)
    hl = normalizza_valore(hl)
    lh = normalizza_valore(lh)
    ll = normalizza_valore(ll)

    struttura = "neutro"
    alert = False
    commento = ""

    if hh and hl and hh > hl:
        struttura = "rialzista"
        commento = f"⚙️ Struttura su {tf} impostata a rialzo: massimi e minimi crescenti (HH: {hh}, HL: {hl})."
        alert = True
    elif lh and ll and lh < ll:
        struttura = "ribassista"
        commento = f"⚙️ Struttura su {tf} impostata a ribasso: massimi e minimi decrescenti (LH: {lh}, LL: {ll})."
        alert = True
    elif hh and lh and hh < lh:
        struttura = "in transizione"
        commento = f"⚠️ Struttura su {tf} in potenziale inversione ribassista: HH < LH."
        alert = True
    elif ll and hl and ll > hl:
        struttura = "in transizione"
        commento = f"⚠️ Struttura su {tf} in potenziale inversione rialzista: LL > HL."
        alert = True
    else:
        struttura = "range"
        commento = f"ℹ️ Struttura su {tf} non chiaramente direzionale. Possibile consolidamento."

    commento_livelli = (
        f"📊 Livelli ➤ HH: {formatta_valore(hh)}, "
        f"HL: {formatta_valore(hl)}, "
        f"LH: {formatta_valore(lh)}, "
        f"LL: {formatta_valore(ll)}"
    )

    return {
        "nome": "Struttura di trend",
        "commento": f"{commento}\n{commento_livelli}",
        "alert": alert,
        "struttura": struttura,
        "timeframe": tf
    }
