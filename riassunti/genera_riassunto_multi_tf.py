from collections import Counter

def genera_riassunto_multi_tf(indicatori_per_tf: dict, meta_info: dict) -> str:
    """
    Genera un riassunto tecnico strategico multi-timeframe in stile Cassandra potenziato (Mini-Me).
    """

    tf_rilevanti = ["15m", "1h", "4h", "1d", "1w"]
    tf_attivi = [tf for tf in tf_rilevanti if tf in indicatori_per_tf]

    direzioni, scenari, forza_long, forza_short = [], [], 0, 0

    for tf in tf_attivi:
        for ind in indicatori_per_tf[tf]:
            if ind.get("punteggio", 0) > 0:
                direzione = ind.get("direzione", "neutro")
                scenario = ind.get("scenario", "").lower()
                direzioni.append(direzione)
                if scenario not in ["", "n.d.", "neutro", "intermedia"]:
                    scenari.append(scenario)
                if direzione == "long":
                    forza_long += ind.get("punteggio", 0)
                elif direzione == "short":
                    forza_short += ind.get("punteggio", 0)

    delta = round(abs(forza_long - forza_short), 1)
    dominante = "long" if forza_long > forza_short else "short" if forza_short > forza_long else "neutro"
    conflitto = direzioni.count("long") > 1 and direzioni.count("short") > 1

    # Frasi direzionali
    if dominante == "long" and not conflitto:
        frase_direzionale = "📈 Spinta rialzista ben distribuita tra i timeframe: il trend appare sostenuto e coerente."
    elif dominante == "short" and not conflitto:
        frase_direzionale = "📉 Pressione ribassista diffusa sui timeframe principali: scenario tecnico fragile ma coerente."
    elif conflitto:
        frase_direzionale = "⚠️ Divergenze tra i timeframe: struttura direzionale in conflitto, attenzione a falsi segnali."
    else:
        frase_direzionale = "🌀 Nessuna direzionalità dominante: il mercato sembra in fase laterale o indecisa."

    # Frasi scenario dominante
    scenario_dominante, freq = None, 0
    if scenari:
        counts = Counter(scenari)
        scenario_dominante, freq = counts.most_common(1)[0]

    if freq >= 2:
        frase_scenario = f"🔍 Lo scenario tecnico più ricorrente è **{scenario_dominante}**, rilevato in {freq} timeframe."
    else:
        frase_scenario = "🔎 Nessuno scenario ricorrente significativo, il contesto tecnico resta frammentato."

    # Frasi sulle forze
    frase_forze = f"💪 Forza long: {round(forza_long,1)} | Forza short: {round(forza_short,1)} | Delta: {delta}"

    # Sintesi finale operativa
    if dominante == "long" and not conflitto:
        frase_operativa = "✅ Strategia operativa: favorire ingressi long, con conferme su TF superiori."
    elif dominante == "short" and not conflitto:
        frase_operativa = "⚠️ Strategia operativa: short tattici consentiti, ma attenzione a rimbalzi su supporti."
    elif conflitto:
        frase_operativa = "⛔ Strategia operativa sospesa: conflitti tra timeframe, meglio attendere una conferma direzionale."
    else:
        frase_operativa = "🤔 Strategia operativa: neutrale. Valutare breakout o segnali di rottura imminente."

    # Output completo
    return "\n".join([
        "🧠 **Analisi Multi-Timeframe Cassandra**",
        frase_direzionale,
        frase_scenario,
        frase_forze,
        frase_operativa
    ])
