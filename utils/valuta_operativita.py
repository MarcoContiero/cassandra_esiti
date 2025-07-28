# === FILE: utils/valuta_operativita.py ===

def valuta_timing_operativo(dati_indicatore_tf: dict, timeframe: str) -> str:
    macd_dir = dati_indicatore_tf.get("MACD", {}).get("direzione", "neutro")
    rsi_val = dati_indicatore_tf.get("RSI", {}).get("valore", 50)
    ema21_dir = dati_indicatore_tf.get("EMA 21", {}).get("direzione", "neutro")
    stoch_val = dati_indicatore_tf.get("STOCH", {}).get("valore", 50)

    if macd_dir == "short" and rsi_val < 50 and ema21_dir == "short":
        return "no_entry"
    if macd_dir == "short" or rsi_val < 45:
        return "attendere_conferma"
    if macd_dir == "long" and rsi_val > 55 and ema21_dir == "long" and stoch_val < 80:
        return "entry_favorevole"
    return "attendere_conferma"


def valuta_operativita_totale(dati) -> str:
    """
    Valuta l'esito operativo complessivo.
    Accetta sia lista piatta che dizionario per timeframe.
    """
    tfs = ["15m", "1h", "4h"]
    esiti = []

    if isinstance(dati, list):
        for tf in tfs:
            subset = [x for x in dati if x.get("timeframe") == tf]
            indicatore_dict = {x["indicatore"]: x for x in subset if "indicatore" in x}
            esiti.append(valuta_timing_operativo(indicatore_dict, tf))

    elif isinstance(dati, dict):
        for tf in tfs:
            esiti.append(valuta_timing_operativo(dati.get(tf, []), tf))

    if "strong buy" in esiti:
        return "🟢 STRONG BUY → concordanza su tutti i timeframe."
    elif "buy" in esiti:
        return "🟢 BUY → segnali operativi in costruzione."
    elif "wait" in esiti:
        return "⚠️ Attendere conferma: struttura long, ma segnali deboli."
    else:
        return "❌ Nessuna operatività consigliata."

def genera_blocco_strutturale_e_operativo(direzioni: dict, dominante: str, esito_operativo: str) -> str:
    print("🧪 DEBUG: contenuto direzioni ricevute ➤", direzioni)

    top2 = sorted(direzioni.items(), key=lambda x: x[1], reverse=True)[:2]
    dir1, val1 = top2[0]
    dir2, val2 = top2[1]
    delta = val1 - val2

    riga1 = f"📈 SCENARIO STRUTTURALE: {dir1.upper()} (dominante su {dominante})"
    riga2 = f"🔢 Δ forza = {delta:.1f} ({dir1}: {val1:.1f} / {dir2}: {val2:.1f})"
    riga3 = f"\n{esito_operativo}"
    return f"{riga1}\n{riga2}\n{riga3}"


def genera_blocco_strategico_completo(direzione: str, delta: float, esito_operativo: str) -> str:
    forza = "forte" if delta >= 100 else "decisa" if delta >= 40 else "moderata" if delta >= 10 else "fragile"

    if direzione == "neutro" or forza == "fragile":
        return "⚠️ Scenario incerto o frammentato. Nessuna direzione affidabile al momento."

    if direzione == "long":
        if esito_operativo.startswith("✅"):
            return f"📈 Trend long {forza} e coerente su più timeframe. Possibile ingresso operativo."
        elif esito_operativo.startswith("⚠️"):
            return f"📈 Direzione long {forza} ma segnali operativi deboli. Attendere conferma prima di entrare."
        else:
            return f"⚠️ Struttura long {forza} ma i timeframe inferiori negano l'ingresso. Rischio controtrend."

    if direzione == "short":
        if esito_operativo.startswith("✅"):
            return f"📉 Trend short {forza} con conferme operative. Possibile setup ribassista."
        elif esito_operativo.startswith("⚠️"):
            return f"📉 Direzione short {forza} ma segnali misti. Attendere conferma di continuazione ribassista."
        else:
            return f"⛔️ Scenario short {forza} non supportato dal breve termine. Meglio evitare operazioni."

    return "⚠️ Situazione non definita. Verifica coerenza tra scenario e segnali operativi."

def calcola_forze_totali(dati_indicatori) -> dict:
    somma = {"long": 0.0, "short": 0.0, "neutro": 0.0}

    if isinstance(dati_indicatori, dict):
        for tf, lista in dati_indicatori.items():
            #print(f"\n🧪 DEBUG ➤ Timeframe: {tf} ➤ {len(lista)} indicatori")
            for item in lista:
                #print("🔹 Item ➤", item)
                if not isinstance(item, dict):
                    print("❌ NON è un dizionario:", item)
                    continue
                direzione = item.get("direzione")
                punteggio = item.get("punteggio", 0)
                print(f"➡️  Direzione: {direzione} | Punteggio: {punteggio}")
                if direzione in somma:
                    somma[direzione] += punteggio

    elif isinstance(dati_indicatori, list):
        #print(f"\n🧪 DEBUG ➤ Lista semplice con {len(dati_indicatori)} elementi")
        for item in dati_indicatori:
            #print("🔹 Item ➤", item)
            if not isinstance(item, dict):
                print("❌ NON è un dizionario:", item)
                continue
            direzione = item.get("direzione")
            punteggio = item.get("punteggio", 0)
            print(f"➡️  Direzione: {direzione} | Punteggio: {punteggio}")
            if direzione in somma:
                somma[direzione] += punteggio

    print("✅ TOTALE FORZE CALCOLATE:", somma)
    return somma

def genera_commento_finale_completo(riepilogo_tf: dict, indicatori_tf: list) -> str:
    direzione = riepilogo_tf.get("direzione")
    dominante = riepilogo_tf.get("dominante")
    forza_long = riepilogo_tf.get("long", 0)
    forza_short = riepilogo_tf.get("short", 0)
    forza_neutro = riepilogo_tf.get("neutro", 0)
    delta = riepilogo_tf.get("delta", 0)

    direzioni = {
        "long": forza_long,
        "short": forza_short,
        "neutro": forza_neutro
    }

    esito_op = valuta_operativita_totale(indicatori_tf)  # accetta anche lista piatta se già sistemato

    frase = genera_blocco_strategico_completo(direzione, delta, esito_op)
    blocco = genera_blocco_strutturale_e_operativo(direzioni, dominante, esito_op)

    return frase + "\n\n" + blocco


