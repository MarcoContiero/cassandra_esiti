import os
import json
import random
from collections import defaultdict, Counter
from utils.valuta_operativita import valuta_operativita_totale, genera_blocco_strutturale_e_operativo

def genera_frase_scenario(direzione="long", punteggio=None, path_json="frasi_base.json"):
    if not os.path.exists(path_json):
        return "⚠️ Impossibile generare frase: dizionario mancante."
    with open(path_json, "r", encoding="utf-8") as f:
        frasi = json.load(f)
    inizio = random.choice(frasi["inizio"])
    trend = random.choice(frasi["trend_rialzista" if direzione == "long" else "trend_ribassista"])
    conferma = random.choice(frasi["conferme"])
    strategia = random.choice(frasi["strategie"])
    frase = f"{inizio}, {trend}, {conferma.lower()}."
    if punteggio:
        frase += f" Il punteggio tecnico è {punteggio}."
    frase += " " + strategia
    return frase

def genera_frase_dinamica(direzione="long", contesto="in_conferma", path_json="frasi_dinamiche.json") -> str:
    if not os.path.exists(path_json):
        return "⚠️ Errore: dizionario frasi_dinamiche non trovato."
    try:
        with open(path_json, "r", encoding="utf-8") as f:
            dizionario = json.load(f)
        blocco = dizionario.get(direzione.lower(), {}).get(contesto.lower(), [])
        if not blocco:
            return f"⚠️ Nessuna frase disponibile per direzione '{direzione}' e contesto '{contesto}'."
        return random.choice(blocco)
    except Exception as e:
        return f"⚠️ Errore nella generazione frase dinamica: {e}"

def genera_commento_finale_avanzato(indicatori_per_tf: dict, meta_info: dict) -> str:
    TF_FUNZIONE = {
        "1m": "timing", "3m": "timing", "5m": "timing",
        "15m": "timing", "30m": "timing", "1h": "timing",
        "2h": "trend", "4h": "trend", "6h": "trend", "8h": "trend", "12h": "trend",
        "1d": "trend", "3d": "ciclo", "1w": "ciclo", "1M": "ciclo"
    }

    funzioni = defaultdict(list)
    forza_globale = defaultdict(float)
    scenari = []

    for tf, indicatori in indicatori_per_tf.items():
        ruolo = TF_FUNZIONE.get(tf, "altro")
        for ind in indicatori:
            if ind.get("punteggio", 0) > 0:
                funzioni[ruolo].append(ind)
                forza_globale[ind.get("direzione", "neutro")] += ind.get("punteggio", 0)
                scenario = ind.get("scenario", "").lower()
                if scenario not in ["", "n.d.", "neutro", "intermedia"]:
                    scenari.append(scenario)

    def analizza_blocco(nome, lista):
        if not lista:
            return f"🕳️ Nessun segnale rilevante per la fase **{nome}**."
        direzioni = Counter([i.get("direzione", "neutro") for i in lista])
        scenari_funzione = [i.get("scenario", "").lower() for i in lista if i.get("scenario", "").lower() not in ["", "n.d.", "neutro", "intermedia"]]
        forza_l = sum(i.get("punteggio", 0) for i in lista if i.get("direzione") == "long")
        forza_s = sum(i.get("punteggio", 0) for i in lista if i.get("direzione") == "short")
        delta = round(abs(forza_l - forza_s), 1)
        dominante = (
            "📈 forza long" if forza_l > forza_s else
            "📉 forza short" if forza_s > forza_l else
            "🌀 direzione neutra"
        )
        top_scenario = Counter(scenari_funzione).most_common(1)
        scenario_text = f"🔍 Scenario prevalente: {top_scenario[0][0]}" if top_scenario else "🔎 Nessuno scenario dominante."
        return f"🔹 **{nome.upper()}** ➤ {dominante} | Δ: {delta}\n{scenario_text}"

    blocco_timing = analizza_blocco("timing", funzioni["timing"])
    blocco_trend = analizza_blocco("trend", funzioni["trend"])
    blocco_ciclo = analizza_blocco("ciclo", funzioni["ciclo"])

    direzione_globale = max(forza_globale, key=forza_globale.get)
    delta_globale = round(abs(forza_globale["long"] - forza_globale["short"]), 1)
    direzioni_forti = [k for k, v in forza_globale.items() if v > 0]

    top_scenario = Counter(scenari).most_common(1)
    scenario_tecnico = top_scenario[0][0] if top_scenario else "n.d."

    # Scegli tipo frase in base allo scenario
    contesto = "in_conferma"
    if "breakout" in scenario_tecnico:
        contesto = "breakout"
    elif "pullback" in scenario_tecnico or "ritraccio" in scenario_tecnico:
        contesto = "pullback"
    elif "compressione" in scenario_tecnico or "range" in scenario_tecnico:
        contesto = "compressione"
    elif "conflitto" in scenario_tecnico or "indecisione" in scenario_tecnico:
        contesto = "conflitto"
    elif "attesa" in scenario_tecnico:
        contesto = "attesa"

    if direzione_globale in ["long", "short", "neutro"]:
        frase_sintesi = genera_frase_dinamica(direzione=direzione_globale, contesto=contesto)
    else:
        frase_sintesi = genera_frase_scenario(direzione=direzione_globale)

    scenario_line = f"🧩 Scenario tecnico prevalente: **{scenario_tecnico}**" if scenario_tecnico != "n.d." else "🧩 Nessuno scenario tecnico ricorrente."
    esito_op = valuta_operativita_totale([i for tf in indicatori_per_tf for i in indicatori_per_tf[tf]])
    blocco_operativo = genera_blocco_strutturale_e_operativo(forza_globale, meta_info.get("timeframe", "n.d."), esito_op)

    return "\n\n".join([
        "🧠 **Cassandra 2125 | Analisi Stratificata Multi-TF**",
        scenario_line,
        frase_sintesi,
        "",
        blocco_timing,
        blocco_trend,
        blocco_ciclo,
        "",
        blocco_operativo
    ])
