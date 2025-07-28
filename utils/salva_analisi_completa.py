import json

def salva_analisi_completa(coin, risultato):
    print("✅ Versione aggiornata di salva_analisi_completa chiamata")

    scenario = risultato.get("scenario_finale", {})
    dettagli = risultato.get("dettagli_per_timeframe", {})
    riass_tecnico = risultato.get("riassunto_tecnico", "")
    riass_globale = risultato.get("riassunto_testuale", "")
    punteggi = risultato.get("punteggi_per_timeframe", {})

    righe = []
    righe.append("# === SCENARIO FINALE ===")
    righe.append(f"Direzione: {scenario.get('scenario', 'n.d.')}")
    righe.append(f"Punteggio totale: {scenario.get('punteggio_totale', 'n/a')}")
    righe.append(f"Forza vincente: {scenario.get('forza_vincente', 'n/a')}")
    righe.append(f"Forza opposta: {scenario.get('forza_opposta', 'n/a')}")
    righe.append(f"Delta forza: {scenario.get('delta_forza', 'n/a')}")
    righe.append(f"Timeframe dominante: {scenario.get('timeframe_dominante', 'n/a')}")
    righe.append("")

    righe.append("# === PUNTEGGI PER TIMEFRAME ===")
    righe.append(riass_tecnico)
    righe.append("")

    righe.append("# === ANALISI GLOBALE ===")
    righe.append(riass_globale)
    righe.append("")

    righe.append("# === DATI GREZZI PER TIMEFRAME ===")
    for tf, gruppi in dettagli.items():
        righe.append(f"\n📊 Timeframe: {tf}")

        for gruppo_nome in ["core", "optional"]:
            elenco = gruppi.get(gruppo_nome, [])
            simbolo = "🔹" if gruppo_nome == "core" else "🔸"
            righe.append(f"  {simbolo} {gruppo_nome.upper()}:")
            if not elenco:
                righe.append("    (nessun dato)")
            else:
                for indicatore in elenco:
                    nome = indicatore.get("nome", "-")
                    valore = indicatore.get("valore", "-")
                    punteggio = indicatore.get("punteggio", "-")
                    direzione = indicatore.get("direzione", "-")
                    righe.append(f"    · {nome} → valore: {valore}, punteggio: {punteggio}, direzione: {direzione}")

    return "\n".join(righe)

def salva_riassunto_singolo(coin, risultato):
    scenario = risultato.get("scenario_finale", {})
    riass_tecnico = risultato.get("riassunto_tecnico", "")
    riass_globale = risultato.get("riassunto_testuale", "")

    righe = []
    righe.append("# === SCENARIO FINALE ===")
    righe.append(f"Direzione: {scenario.get('scenario', 'n.d.')}")
    righe.append(f"Punteggio totale: {scenario.get('punteggio_totale', 'n/a')}")
    righe.append(f"Forza vincente: {scenario.get('forza_vincente', 'n/a')}")
    righe.append(f"Forza opposta: {scenario.get('forza_opposta', 'n/a')}")
    righe.append(f"Delta forza: {scenario.get('delta_forza', 'n/a')}")
    righe.append(f"Timeframe dominante: {scenario.get('timeframe_dominante', 'n/a')}")
    righe.append("")

    righe.append("# === PUNTEGGI PER TIMEFRAME ===")
    righe.append(riass_tecnico)
    righe.append("")

    righe.append("# === ANALISI GLOBALE ===")
    righe.append(riass_globale)

    return "\n".join(righe)
