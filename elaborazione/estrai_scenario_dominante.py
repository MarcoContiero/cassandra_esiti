from collections import Counter

def estrai_scenario_dominante(lista_indicatori_tf: list) -> str:
    """
    Analizza gli indicatori di un singolo timeframe e restituisce una sintesi
    tecnica significativa (es. 'Trend forte', 'Breakout rialzista', ecc.)
    """
    # Raccogli solo scenari significativi (punteggio > 0)
    scenari_validi = [
        ind.get("scenario", "").lower()
        for ind in lista_indicatori_tf
        if ind.get("punteggio", 0) > 0
    ]

    # Conta le occorrenze dei vari scenari
    conta = Counter(scenari_validi)

    # Converti a lowercase per uniformità
    scenari_set = set(scenari_validi)

    # === REGOLA 1: Trend forte ===
    if conta["trend forte"] >= 2:
        return "Trend forte in atto"

    # === REGOLA 2: Breakout rialzista ===
    if (
        any("macd incrocio positivo" in s for s in scenari_set)
        and any("prezzo sopra media" in s for s in scenari_set)
        and any("trend forte" in s for s in scenari_set)
    ):
        return "Breakout rialzista in corso"

    # === REGOLA 3: Compressione ===
    if (
        "compressione" in scenari_set
        or any("dentro bande" in s for s in scenari_set)
    ) and conta["trend forte"] == 0:
        return "Compressione in corso"

    # === REGOLA 4: Trend ribassista ===
    if (
        any("macd incrocio negativo" in s for s in scenari_set)
        and any("volume in calo" in s for s in scenari_set)
        and any("prezzo sotto media" in s for s in scenari_set)
    ):
        return "Trend ribassista in atto"

    # === REGOLA 5: Fase laterale ===
    direzioni = [ind.get("direzione") for ind in lista_indicatori_tf if ind.get("punteggio", 0) > 0]
    count_direzioni = Counter(direzioni)

    if (
        count_direzioni.get("long", 0) >= 2
        and count_direzioni.get("short", 0) >= 2
    ):
        return "Fase laterale indecisa"

    # === REGOLA 6: Rientro tecnico (da supporto) ===
    if (
        any("fvg long" in s for s in scenari_set)
        and any("ipercomprato" in s or "rsi basso" in s for s in scenari_set)
    ):
        return "Rientro da supporto tecnico"

    # === REGOLA 7: Ritracciamento da resistenza ===
    if (
        any("fvg short" in s for s in scenari_set)
        and any("ipercomprato" in s for s in scenari_set)
    ):
        return "Ritracciamento da resistenza"

    # === REGOLA 8: Trend rialzista generico ===
    if count_direzioni.get("long", 0) > max(count_direzioni.get("short", 0), count_direzioni.get("neutro", 0)):
        return "Tendenza rialzista moderata"

    # === REGOLA 9: Trend ribassista generico ===
    if count_direzioni.get("short", 0) > max(count_direzioni.get("long", 0), count_direzioni.get("neutro", 0)):
        return "Tendenza ribassista moderata"

    # === DEFAULT ===
    return "Scenario poco chiaro"
