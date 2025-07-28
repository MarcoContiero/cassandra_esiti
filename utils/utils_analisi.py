from collections import defaultdict

def crea_indicatore(nome, timeframe, scenario, punteggio, direzione, valore=None, messaggio=None, pattern=None):  # ✅ Estesa
    return {
        'nome': nome,
        'timeframe': timeframe,
        'scenario': scenario,
        'punteggio': punteggio,
        'direzione': direzione,
        'valore': valore,
        'messaggio': messaggio,
        'pattern': pattern,
    }

def normalizza_risultato(dati_grezzi: dict) -> dict:
    scenario_finale = {}
    dettagli_per_timeframe = {}
    punteggi_per_timeframe = {}
    indicatori_forti = []

    for tf, gruppo in dati_grezzi.items():
        indicatori = gruppo.get("indicatori", [])
        if not indicatori:
            continue

        punteggio_totale = 0
        for ind in indicatori:
            punteggio_totale += ind.get("punteggio", 0)

            # Raccoglie indicatori forti (punteggio >= 80% di 10)
            if ind.get("punteggio", 0) >= 8:
                indicatori_forti.append((tf, ind))

        # Semplificazione scenario finale per singolo TF
        direzioni = [i.get("direzione") for i in indicatori if i.get("direzione") != "neutro"]
        if direzioni:
            # Conta la direzione prevalente
            from collections import Counter
            direzione_finale = Counter(direzioni).most_common(1)[0][0]
        else:
            direzione_finale = "n/d"

        punteggi_per_timeframe[tf] = punteggio_totale
        dettagli_per_timeframe[tf] = {
            "scenario": direzione_finale,
            "punteggio": punteggio_totale,
            "timeframe": tf,
            "indicatori": indicatori,
        }

    # Calcolo dello scenario finale
    direzioni_finali = [v["scenario"] for v in dettagli_per_timeframe.values() if v["scenario"] != "n/d"]
    if direzioni_finali:
        from collections import Counter
        direzione_global = Counter(direzioni_finali).most_common(1)[0][0]
    else:
        direzione_global = "neutro"

    scenario_finale = {
        "scenario": direzione_global,
        "punteggio_totale": sum(punteggi_per_timeframe.values())
    }

    return {
        "scenario_finale": scenario_finale,
        "riassunto_tecnico": "",  # opzionale: da costruire altrove
        "riassunto_testuale": "",  # opzionale: da costruire altrove
        "indicatori_forti": indicatori_forti,
        "dettagli_per_timeframe": dettagli_per_timeframe,
        "punteggi_per_timeframe": punteggi_per_timeframe,
    }

def aggrega_per_tf(lista):
    tf_dict = defaultdict(list)
    for r in lista:
        tf_dict[r.get("timeframe", "n/d")].append(r)
    return tf_dict