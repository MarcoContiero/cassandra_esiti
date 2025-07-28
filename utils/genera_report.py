import json

def genera_report_completo(coin, risultato):

    righe = []

    scenario = risultato.get("scenario_finale", {})
    dettagli = risultato.get("dettagli_per_timeframe", {})
    riass_tecnico = risultato.get("riassunto_tecnico", "").strip()
    riass_globale = risultato.get("riassunto_testuale", "").strip()
    punteggi = risultato.get("punteggi_per_timeframe", {})
    dati_ohlcv = risultato.get("dati_ohlcv_per_timeframe", {})

    # 1. INFO GENERALI
    righe.append("# === INFO GENERALI ===")
    righe.append(f"Coin: {coin}")
    righe.append(f"Scenario finale: {scenario.get('direzione', scenario.get('scenario', 'n.d.'))}")
    righe.append(f"Punteggio totale: {scenario.get('punteggio_totale', 0)}")
    righe.append(f"Forza vincente: {scenario.get('forza_vincente', 0)}")
    righe.append(f"Forza opposta: {scenario.get('forza_opposta', 0)}")
    righe.append(f"Delta forza: {scenario.get('delta_forza', 0)}")
    righe.append(f"Timeframe dominante: {scenario.get('timeframe_dominante', 'n.d.')}")
    righe.append("")

    # 2. DETTAGLI PER TIMEFRAME
    righe.append("# === DETTAGLI PER TIMEFRAME ===")
    for tf, info in dettagli.items():
        direzione = info.get("direzione", info.get("scenario", "n.d."))
        long_c = info.get("long", 0)
        short_c = info.get("short", 0)
        righe.append(f"[{tf}] → direzione: {direzione}, long: {long_c}, short: {short_c}")
    righe.append("")

    # 3. RIASSUNTO TECNICO
    righe.append("# === RIASSUNTO TECNICO ===")
    righe.append(riass_tecnico)
    righe.append("")

    # 4. RIASSUNTO GLOBALE
    righe.append("# === RIASSUNTO GLOBALE ===")
    righe.append(riass_globale)
    righe.append("")

    # 5. PUNTEGGI PER TIMEFRAME
    righe.append("# === PUNTEGGI PER TIMEFRAME ===")
    totale_punteggi = 0
    for tf, punteggio_tf in punteggi.items():
        core_val = punteggio_tf.get("core", 0)
        optional_val = punteggio_tf.get("optional", 0)
        # Se core/optional sono liste di indicatori somma punteggio
        if isinstance(core_val, list):
            core = sum(ind.get("punteggio", 0) for ind in core_val)
        else:
            core = core_val
        if isinstance(optional_val, list):
            optional = sum(ind.get("punteggio", 0) for ind in optional_val)
        else:
            optional = optional_val
        totale = core + optional
        totale_punteggi += totale
        righe.append(f"* {tf}: Core={core}, Optional={optional} #totale {totale}")
    righe.append(f"- Totale {totale_punteggi}")
    righe.append("")

    # 6. INDICATORI PER TIMEFRAME (core + optional)
    righe.append("# === INDICATORI PER TIMEFRAME ===")
    for tf, dati in punteggi.items():
        righe.append(f"📊 {tf.upper()}")
        # CORE
        righe.append(" - CORE:")
        core_list = dati.get("core", [])
        if isinstance(core_list, list) and core_list:
            for indicatore in core_list:
                nome = indicatore.get("nome", indicatore.get("indicatore", "Sconosciuto"))
                valore = indicatore.get("valore", "N/A")
                punteggio = indicatore.get("punteggio", "N/A")
                direzione = indicatore.get("direzione", indicatore.get("scenario", "N/A"))
                righe.append(f"    · {nome} → valore: {valore}, punteggio: {punteggio}, direzione: {direzione}")
        else:
            righe.append("    · Nessun dato")
        # OPTIONAL
        righe.append(" - OPTIONAL:")
        optional_list = dati.get("optional", [])
        if isinstance(optional_list, list) and optional_list:
            for indicatore in optional_list:
                nome = indicatore.get("nome", indicatore.get("indicatore", "Sconosciuto"))
                valore = indicatore.get("valore", "N/A")
                punteggio = indicatore.get("punteggio", "N/A")
                direzione = indicatore.get("direzione", indicatore.get("scenario", "N/A"))
                righe.append(f"    · {nome} → valore: {valore}, punteggio: {punteggio}, direzione: {direzione}")
        else:
            righe.append("    · Nessun dato")
        righe.append("")

    # 7. DATI GREZZI COMPLETI PER TIMEFRAME (tutti i dati OHLCV)
    righe.append("# === DATI GREZZI COMPLETI PER TIMEFRAME ===")
    for tf, df in dati_ohlcv.items():
        righe.append(f"\n## {tf.upper()} (tutti i dati)")
        righe.append(df.to_string())
        righe.append("")

    # 8. DATI GREZZI COMPLESSIVI JSON (dump completo)
    righe.append("# === DATI GREZZI JSON COMPLETI ===")
    righe.append(json.dumps(risultato, indent=2, default=str))
    righe.append("")

    return "\n".join(righe)
