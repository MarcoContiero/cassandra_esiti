from shared.riassunti import costruisci_riassunto_testuale

def genera_riassunti(finale, dettagli_per_tf):
    try:
        # Attualmente dettagli_per_tf contiene solo scenario/punteggio, quindi indicatori forti non sono calcolabili
        indicatori_forti = []  # estrai_indicatori_forti(dettagli_per_tf) richiederebbe una struttura diversa
    except Exception as e:
        print(f"❌ Errore indicatori forti: {e}")
        indicatori_forti = []

    try:
        # Riassunto tecnico con lista delle direzioni per timeframe
        riassunto_tecnico = costruisci_riassunto_tecnico_base(dettagli_per_tf)
    except Exception as e:
        print(f"⚠️ Errore riassunto tecnico: {e}")
        riassunto_tecnico = "N/A"

    try:
        riassunto_testuale = costruisci_riassunto_testuale(finale, indicatori_forti)
    except Exception as e:
        print(f"⚠️ Errore riassunto testuale: {e}")
        riassunto_testuale = "N/A"
    return indicatori_forti, riassunto_tecnico, riassunto_testuale


def costruisci_riassunto_tecnico_base(dettagli_per_tf):
    if not dettagli_per_tf:
        return "⚠️ Nessun dettaglio disponibile."

    righe = []
    for tf, dati in dettagli_per_tf.items():
        direzione = dati.get("scenario", "n/d")
        punteggio = dati.get("punteggio", "n/d")
        righe.append(f"• {tf} → {direzione.upper()} ({punteggio})")

    return "\n".join(righe)
