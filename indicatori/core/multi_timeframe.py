from indicatori.core.rsi import analizza_rsi
from indicatori.core.macd import analizza_macd
from indicatori.core.ema import analizza_ema
from indicatori.core.bollinger import analizza_bollinger
from indicatori.core.parabolic_sar import analizza_parabolic_sar
from indicatori.core.volume import analizza_volume

from indicatori.optional.pattern_tecnici import analizza_pattern_tecnici
from indicatori.optional.fvg import analizza_fvg
from indicatori.optional.gann_levels import analizza_gann
from indicatori.optional.fibonacci import analizza_fibonacci
from indicatori.optional.analisi_ciclica import analizza_ciclo
from indicatori.optional.massimi_minimi import analizza_massimi_minimi

from indicatori.extra.adx import analizza_adx
from indicatori.extra.ichimoku import analizza_ichimoku
from indicatori.extra.fasi_lunari import analizza_fasi_lunari
from indicatori.extra.elliott import analizza_elliott
from indicatori.optional.ma_cross import analizza_ma_cross

def analizza_singolo_timeframe(tf, df):
    print(f"🔍 DEBUG {tf.upper()} - Inizio analisi indicatori")

    print("📋 Tipo df:", type(df))
    print("📊 Prime righe df:", df[:5])

    risultati = [
        analizza_rsi(df, tf),
        analizza_macd(df, tf),
        analizza_ema(df, tf),
        analizza_bollinger(df, tf),
        analizza_parabolic_sar(df, tf),
        analizza_volume(df, tf),
        analizza_pattern_tecnici(df, tf),
        analizza_fvg(df, tf),
        analizza_gann(df, tf),
        analizza_fibonacci(df, tf),
        analizza_ciclo(df, tf),
        analizza_massimi_minimi(df, tf),
        analizza_adx(df, tf),
        analizza_ichimoku(df, tf)
    ]

    # DEBUG: log tipo e valore dei risultati
    print(f"📦 DEBUG risultati grezzi per {tf}:")
    for i, r in enumerate(risultati):
        print(f"  → [{i}] tipo: {type(r)}, valore: {r}")

    direzioni = {"long": 0, "short": 0}
    punteggio_totale = 0
    indicatori_valutati = 0

    for risultato in risultati:
        if not isinstance(risultato, dict):
            print(f"⚠️ [DEBUG - {tf}] Risultato non valido (non dict): {risultato}")
            continue
        try:
            direzione = risultato["direzione"]
            scenario = risultato["scenario"]
            punteggio = risultato["punteggio"]
        except Exception as e:
            print(f"⚠️ [DEBUG - {tf}] Errore lettura chiavi: {e} → risultato: {risultato}")
            continue

        if direzione in direzioni:
            direzioni[direzione] += punteggio
            punteggio_totale += punteggio
            indicatori_valutati += 1

    if indicatori_valutati == 0:
        return {
            "scenario": "errore",
            "punteggio": 0,
            "timeframe": tf
        }

    if direzioni["long"] > direzioni["short"]:
        scenario = "long"
    elif direzioni["short"] > direzioni["long"]:
        scenario = "short"
    else:
        scenario = "neutro"

    print(f"✅ [DEBUG - {tf}] ➤ Scenario: {scenario}, Punteggio: {punteggio_totale}, Direzione: {'long' if direzioni['long'] > direzioni['short'] else 'short' if direzioni['short'] > direzioni['long'] else 'neutro'}")

    return {
        "scenario": scenario,
        "punteggio": punteggio_totale,
        "direzione": scenario,
        "timeframe": tf
    }


# 🔹 Sintesi multi-timeframe
def analizza_multi_timeframe(dati_per_tf):
    try:
        risultati = {}
        totale_score = 0
        direzioni = {"long": 0, "short": 0}

        for tf, dati in dati_per_tf.items():
            direzione = dati.get("scenario", "neutro")
            punteggio = dati.get("punteggio", 0)

            risultati[tf] = {"direzione": direzione, "score": punteggio}
            if direzione in ["long", "short"]:
                direzioni[direzione] += punteggio
                totale_score += punteggio

        # Determina la direzione dominante
        if direzioni["long"] > direzioni["short"]:
            direzione_finale = "long"
        elif direzioni["short"] > direzioni["long"]:
            direzione_finale = "short"
        else:
            direzione_finale = "neutro"

        delta = abs(direzioni["long"] - direzioni["short"])
        forza_vincente = max(direzioni.values())
        forza_opposta = min(direzioni.values())
        dominante = max(risultati, key=lambda k: risultati[k]["score"]) if risultati else "n.d."

        return {
            "scenario": direzione_finale,
            "punteggio_totale": totale_score,
            "delta_forza": delta,
            "forza_vincente": forza_vincente,
            "forza_opposta": forza_opposta,
            "timeframe_dominante": dominante
        }

    except Exception as e:
        print(f"❌ Errore nella sintesi multi-timeframe: {e}")
        return {
            "scenario": "errore",
            "punteggio_totale": 0,
            "delta_forza": 0,
            "forza_vincente": 0,
            "forza_opposta": 0,
            "timeframe_dominante": "n.d."
        }

def valuta_coerenza_multi_timeframe(scenari_per_tf):
    try:
        conteggi = {"long": 0, "short": 0}
        for tf, info in scenari_per_tf.items():
            direzione = info.get("scenario", "neutro")
            if direzione in conteggi:
                conteggi[direzione] += 1

        if conteggi["long"] >= 3 and conteggi["short"] == 0:
            scenario = "long"
            punteggio = 6
        elif conteggi["short"] >= 3 and conteggi["long"] == 0:
            scenario = "short"
            punteggio = 6
        else:
            scenario = "neutro"
            punteggio = 0

        return {
            "indicatore": "Multi-Timeframe",
            "timeframe": "multi",  # puoi anche mettere "multi" o lasciarlo fuori
            "valore": f"long={conteggi['long']} / short={conteggi['short']}",
            "scenario": scenario,
            "punteggio": punteggio,
            "direzione": scenario
        }

    except Exception as e:
        print(f"❌ Errore in valuta_coerenza_multi_timeframe: {e}")
        return {
            "indicatore": "Multi-Timeframe",
            "timeframe": "multi",
            "valore": "errore",
            "scenario": "errore",
            "punteggio": 0,
            "direzione": "neutro"
        }

def costruisci_blocco_multi_tf(scenari_per_tf):
    dettagli = {}
    punteggi = {}

    for tf, dati in scenari_per_tf.items():
        scenario = dati.get("scenario", "n/d")
        punteggio = dati.get("punteggio", 0)

        # Salvo lo scenario e punteggio
        dettagli[tf] = {
            "scenario": scenario,
            "punteggio": punteggio,
            "timeframe": tf
        }

        punteggi[tf] = {
            "scenario": scenario,
            "punteggio": punteggio,
            "timeframe": tf
        }

        # Salvo anche i dettagli dei singoli indicatori, se presenti
        for chiave in dati:
            if chiave not in ["scenario", "punteggio", "timeframe"]:
                if "indicatori" not in dettagli[tf]:
                    dettagli[tf]["indicatori"] = {}
                dettagli[tf]["indicatori"][chiave] = dati[chiave]

    return dettagli, punteggi
    

def calcola_multi_tf_score(direzioni_tf: dict) -> dict:
    """
    Calcola scenario e punteggio in base alle direzioni dei timeframe.
    """
    direzioni = [val for val in direzioni_tf.values() if val in ["long", "short"]]

    if not direzioni:
        return {"scenario": "neutro", "punteggio": 0}

    direzione_dominante = max(set(direzioni), key=direzioni.count)
    occorrenze = direzioni.count(direzione_dominante)

    if occorrenze >= 3:
        return {"scenario": direzione_dominante, "punteggio": occorrenze}
    else:
        return {"scenario": "neutro", "punteggio": occorrenze}