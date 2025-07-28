from collections import defaultdict, Counter
import os
import pandas as pd
from shared.config import PATH_DATI_CSV
from utils.valuta_operativita import valuta_operativita_totale, genera_blocco_strutturale_e_operativo
from utils.utils_analisi import aggrega_per_tf

def integra_blocco_finale(dati, scenario, dominante, forza_long, forza_short, delta):
    esito_operativo = valuta_operativita_totale(dati)
    forza_neutro = dati.get("neutro", 0)
    direzioni = {"long": forza_long, "short": forza_short, "neutro": forza_neutro}
    return genera_blocco_strutturale_e_operativo(direzioni, dominante, esito_operativo)

def blocco_dettagli_per_tf(punteggi):
    righe = ["# === DETTAGLI PER TIMEFRAME ==="]
    for tf in sorted(punteggi, key=lambda x: ["15m", "1h", "4h", "1d", "1w"].index(x) if x in ["15m", "1h", "4h", "1d", "1w"] else 99):
        r = punteggi[tf]
        righe.append(f"{tf.upper()}: LONG {r.get('long', 0)} | SHORT {r.get('short', 0)} | NEUTRO {r.get('neutro', 0)} | TOT {r.get('totale', 0)}")
    return "\n".join(righe)


def blocco_riassunto_tecnico(lista, gruppi_indicatori):
    righe = ["# === RIASSUNTO TECNICO ==="]
    aggregati = aggrega_per_tf(lista)
    for tf in sorted(aggregati):
        core = sum(r.get("punteggio", 0) for r in aggregati[tf] if gruppi_indicatori.get(r["indicatore"].strip().lower().replace(" ", "_"), "core") == "core")
        opt = sum(r.get("punteggio", 0) for r in aggregati[tf] if gruppi_indicatori.get(r["indicatore"].strip().lower().replace(" ", "_"), "core") == "optional")
        righe.append(f"{tf}: CORE {core} | OPTIONAL {opt}")
    return "\n".join(righe)

def blocco_dati_grezzi(lista):
    testo = ["# === DATI GREZZI PER TIMEFRAME ==="]
    by_tf = aggrega_per_tf(lista)
    for tf in sorted(by_tf):
        testo.append(f"\n[{tf}]")
        for r in by_tf[tf]:
            nome = r.get("indicatore", "?")
            gruppo = r.get("gruppo", "?").upper()
            punteggio = r.get("punteggio", "?")
            direzione = r.get("direzione", "?")
            valore = r.get("valore", "?")
            testo.append(f"➤ {nome} | gruppo: {gruppo} | punteggio: {punteggio} | direzione: {direzione} | valore: {valore}")
    return "\n".join(testo)

def blocco_commento_scenari(lista):
    from collections import defaultdict, Counter

    testo = ["# === COMMENTO SCENARI ==="]

    scenari_per_tf = defaultdict(set)
    tutti_scenari = []

    SCENARI_NEUTRI = {
        "", "n.d.", "neutro", "intermedia", "trend debole", "long", "short",
        "nessun incrocio", "nessun pattern", "prezzo sopra kumo", 
        "prezzo sopra tutte le ema", "assenza di trend", "volume sotto media", 
        "dati insufficienti"
    }

    for r in lista:
        tf = r.get("timeframe", "n/d")
        scenario = r.get("scenario", "").lower()
        if scenario in SCENARI_NEUTRI:
            continue
        scenari_per_tf[scenario].add(tf)
        tutti_scenari.append(scenario)

    if not tutti_scenari:
        testo.append("Nessuno scenario tecnico rilevante da commentare.")
        return "\n".join(testo)

    conteggio = Counter(tutti_scenari)
    scenari_ordinati = conteggio.most_common()

    for scenario, _ in scenari_ordinati:
        ordine_tf = ["15m", "1h", "4h", "1d", "1w"]
        tf_list = sorted(scenari_per_tf[scenario], key=lambda x: ordine_tf.index(x) if x in ordine_tf else 99)
        tf_str = ", ".join(tf_list)

        if scenario == "compressione":
            frase = f"🔒 Compressione attiva su {tf_str} → possibile movimento esplosivo in arrivo."
        elif scenario == "breakout":
            frase = f"🚀 Breakout rilevati su {tf_str} → attenzione a conferme rialziste."
        elif scenario == "falso_breakout":
            frase = f"⚠️ Falsi breakout osservati su {tf_str} → rischio trappole per breakout traders."
        elif scenario == "pullback":
            frase = f"🔁 Pullback in corso su {tf_str} → possibili rientri tattici."
        elif scenario == "scarico_post_pump":
            frase = f"💥 Scarico post-pump su {tf_str} → prese di profitto in atto."
        elif scenario == "rientro_strategico":
            frase = f"🎯 Rientro strategico su {tf_str} → ripresa ordinata dopo correzione."
        elif scenario == "pre_breakout":
            frase = f"⚡ Pre-breakout su {tf_str} → segnali anticipatori di breakout."
        elif scenario == "confluenza_bullish":
            frase = f"📈 Confluenza rialzista su {tf_str} → più segnali convergono al rialzo."
        elif scenario == "confluenza_bearish":
            frase = f"📉 Confluenza ribassista su {tf_str} → attenzione a segnali di discesa."
        elif scenario == "incrocio_in_compressione":
            frase = f"🔀 Incrocio tecnico in compressione su {tf_str} → setup in formazione."
        elif scenario == "compressione_esplosiva":
            frase = f"💣 Compressione esplosiva su {tf_str} → breakout imminente altamente probabile."
        else:
            frase = f"📊 Scenario '{scenario}' rilevato su {tf_str}."

        testo.append(frase)

    return "\n".join(testo)

def blocco_scenari_per_tf(lista):
    from collections import defaultdict

    testo = ["# === SCENARI PER TIMEFRAME ==="]
    per_tf = defaultdict(list)

    for r in lista:
        tf = r.get("timeframe", "n/d")
        scenario = r.get("scenario", "").lower()
        if scenario in {
            "", "n.d.", "neutro", "intermedia", "trend debole", "long", "short",
            "nessun incrocio", "nessun pattern", "prezzo sopra kumo", 
            "prezzo sopra tutte le ema", "assenza di trend", "volume sotto media", 
            "dati insufficienti"
        }:
            continue
        nome = r.get("indicatore", "n.d.")
        if nome.lower() in {"supporto", "resistenza"}:
            continue
        per_tf[tf].append(f"{scenario} ({nome})")

    if not per_tf:
        testo.append("Nessuno scenario tecnico rilevato.")
    else:
        ordine_tf = ["15m", "1h", "4h", "1d", "1w"]
        for tf in sorted(per_tf, key=lambda x: ordine_tf.index(x) if x in ordine_tf else 99):
            scenari = ", ".join(per_tf[tf])
            testo.append(f"**_{tf}_**: {scenari}")

    return "\n".join(testo)
