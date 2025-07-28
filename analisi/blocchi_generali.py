from collections import defaultdict
from shared.config import PATH_DATI_CSV
import os
import pandas as pd
from utils.valuta_operativita import valuta_operativita_totale, genera_blocco_strutturale_e_operativo
import json

with open("gruppi_indicatori.json") as f:
    gruppi = json.load(f)


def calcola_riepilogo_totale(lista_indicatori):
    forze = defaultdict(float)

    for x in lista_indicatori:
        direzione = x.get("direzione", "neutro")
        punteggio = x.get("punteggio", 0)
        forze[direzione] += punteggio

    ord = sorted(forze.items(), key=lambda x: x[1], reverse=True)
    direzione = ord[0][0] if ord else "neutro"
    delta = round(ord[0][1] - ord[1][1], 1) if len(ord) > 1 else 0

    return {
        "direzione": direzione,
        "dominante": "1h",  # da aggiornare se serve
        "delta": delta,
        "long": forze.get("long", 0.0),
        "short": forze.get("short", 0.0),
        "neutro": forze.get("neutro", 0.0),
    }


def blocco_info_generali(scenario, data_analisi: str, data_dati: str, coin: str):
    return "\n".join([
        "# === INFO GENERALI ===",
        f"Coin: {coin}",
        f"Data analisi: {data_analisi}",
        f"Dati scaricati il: {data_dati}",
        f"Scenario: {scenario.get('valore', '?')}",
        f"Delta: {scenario.get('delta', '?')}",
        f"Forza long: {scenario.get('forza_long', '?')}",
        f"Forza short: {scenario.get('forza_short', '?')}",
        f"Dominante: {scenario.get('timeframe_dominante', '?')}",
        f"Punteggio totale: {scenario.get('punteggio_totale', '?')}",
    ])


def blocco_dettagli_per_tf(punteggi):
    righe = ["# === DETTAGLI PER TIMEFRAME ==="]
    ordine = ["15m", "1h", "4h", "1d", "1w"]
    for tf in sorted(punteggi, key=lambda x: ordine.index(x) if x in ordine else 99):
        r = punteggi[tf]
        righe.append(f"{tf.upper()}: LONG {r.get('long', 0)} | SHORT {r.get('short', 0)} | NEUTRO {r.get('neutro', 0)} | TOT {r.get('totale', 0)}")
    return "\n".join(righe)

def blocco_riassunto_globale(scenario):
    return "\n".join([
        "# === RIASSUNTO GLOBALE ===",
        f"Scenario: {scenario.get('valore', 'n.d.')}",
        f"Delta forza: {scenario.get('delta', 0)}",
        f"Timeframe dominante: {scenario.get('timeframe_dominante', 'n.d.')}",
        f"Forza long: {scenario.get('forza_long', 0)}",
        f"Forza short: {scenario.get('forza_short', 0)}",
        f"Punteggio totale: {scenario.get('punteggio_totale', 0)}"
    ])


def blocco_dati_binance(coin):
    testo = ["# === DATI BINANCE ==="]
    for tf in ["15m", "1h", "4h", "1d", "1w"]:
        path = os.path.join(PATH_DATI_CSV, f"{coin}_{tf}.csv")
        if os.path.exists(path):
            df = pd.read_csv(path).head(5)
            testo.append(f"\n📊 {tf.upper()}")
            testo.append(df.to_string(index=False))
    return "\n".join(testo)

def blocco_indicatori_forti(lista):
    from collections import defaultdict

    testo = ["# === INDICATORI FORTI ==="]
    by_tf = defaultdict(list)

    punteggi_massimi = {
        "multi_timeframe.py": 6,
        "ema.py": 3,
        "bollinger.py": 3,
        "pattern_tecnici.py": 6,
        "macd.py": 3,
        "volume.py": 6,
        "parabolic_sar.py": 6,
        "ichimoku.py": 6,
        "adx.py": 4,
        "rsi.py": 4,
        "analisi_ciclica.py": 0,
        "ma_cross.py": 4,
        "massimi_minimi.py": 0,
        "fvg.py": 2,
        "fibonacci.py": 0,
        "fasi_lunari.py": 0,
        "gann_levels.py": 2,
        "ema 21": 3,
        "ema 50": 3,
        "macd": 2,
        "rsi": 2,
        "stoch": 4,
        "adx": 3,
        "bbands": 2,
        "obv": 3,
        "mfi": 3,
        "cci": 2,
        "aroon": 0,
        "aroonosc": 0,
        "roc": 4,
        "ultosc": 3,
        "willr": 4,
        "trix": 4,
        "di+ vs di-": 2,
        "cdldoji": 1,
        "natr": 0
    }

    for r in lista:
        nome = r.get("indicatore", "").strip().lower()
        punteggio = r.get("punteggio", 0)
        massimo = punteggi_massimi.get(nome, None)
        if massimo is not None and punteggio == massimo:
            tf = r.get("timeframe", "n/d")
            by_tf[tf].append(r)

    for tf in sorted(by_tf):
        testo.append(f"\n[{tf}]")
        for r in by_tf[tf]:
            scenario = r.get("scenario", "n.d.")
            direzione = r.get("direzione", "n.d.")
            if r.get("punteggio", 0) > 0:
                testo.append(f"➤ {r['indicatore']} | punteggio: {r['punteggio']} | direzione: {direzione} | scenario: {scenario}")

    return "\n".join(testo)

