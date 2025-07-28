def blocco_commento_finale(scenario):
    valore = scenario.get("valore", "n.d.").lower()
    delta = scenario.get("delta", 0)
    tf_dom = scenario.get("timeframe_dominante", "n.d.").upper()
    forza_long = scenario.get("forza_long", 0)
    forza_short = scenario.get("forza_short", 0)

    frase = []

    if valore == "long":
        messaggio = f"📈 Il trend attuale è LONG con dominanza su {tf_dom}. Δ forza = {delta} (long: {forza_long} / short: {forza_short})."
        if delta >= 100:
            strategia = f"Scenario forte: possibile ingresso long su conferma operativa o breakout delle resistenze."
        elif delta >= 50:
            strategia = f"Scenario positivo ma non ancora esplosivo: osservare il comportamento del prezzo su livelli chiave."
        else:
            strategia = f"Scenario long debole: servono ulteriori conferme sul timeframe dominante."
    elif valore == "short":
        messaggio = f"📉 Il trend attuale è SHORT con dominanza su {tf_dom}. Δ forza = {delta} (long: {forza_long} / short: {forza_short})."
        if delta >= 100:
            strategia = f"Scenario forte: possibile ingresso short su conferma o rottura dei supporti."
        elif delta >= 50:
            strategia = f"Scenario short discreto: valutare con cautela su ulteriori segnali tecnici."
        else:
            strategia = f"Scenario short debole: rischio laterale, attendere nuovi sviluppi."
    else:
        messaggio = f"🔍 Scenario neutro con dominanza su {tf_dom}. Δ forza = {delta} (long: {forza_long} / short: {forza_short})."
        strategia = f"Attendere sviluppi: nessuna direzionalità chiara sul timeframe dominante."

    frase.append(messaggio)
    frase.append("")
    frase.append(f"💡 Strategia suggerita: {strategia}")

    return "\n".join(frase)
