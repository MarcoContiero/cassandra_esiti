# === costruisci_riassunto_cassandra_esteso.py ===

from datetime import datetime

def costruisci_riassunto_cassandra_esteso(meta_dati_finali: dict) -> str:
    """
    Genera un riassunto descrittivo esteso incrociando i risultati Cassandra.
    """
    coin = meta_dati_finali.get("coin", "N/D")
    timeframes = meta_dati_finali.get("timeframes", [])
    dettagli = meta_dati_finali.get("dettagli_per_timeframe", {})
    scenario_finale = meta_dati_finali.get("scenario_finale", {})
    data_analisi = meta_dati_finali.get("data_analisi", datetime.now().strftime("%Y-%m-%d %H:%M"))

    sezioni = []

    # === 1. Intestazione ===
    sezioni.append(f"📈 Analisi estesa per {coin} - {data_analisi}")

    # === 2. Scenario generale ===
    dominante = scenario_finale.get("dominante", "N/D")
    scenario = scenario_finale.get("scenario", "N.D.").upper()
    forza_long = scenario_finale.get("forza_long", 0)
    forza_short = scenario_finale.get("forza_short", 0)
    delta = scenario_finale.get("delta", 0)

    if forza_long > forza_short:
        tendenza = "rialzista"
    elif forza_short > forza_long:
        tendenza = "ribassista"
    else:
        tendenza = "neutra"

    sezioni.append(f"▶️ Scenario dominante: {scenario} (TF: {dominante}) con delta di forza pari a {delta}.")
    sezioni.append(f"💪 Forze totali ➤ Long: {forza_long} | Short: {forza_short} ⇒ Tendenza generale: **{tendenza}**.\n")

    # === 3. Analisi per timeframe ===
    blocchi_tf = []
    scenari_presenti = []
    compressioni = []
    strutture = []

    for tf in timeframes:
        tf_data = dettagli.get(tf, {})
        punteggio = tf_data.get("punteggio", 0)
        direzione = tf_data.get("scenario", "N.D.")
        forze = tf_data.get("forze", {"long": 0, "short": 0, "neutro": 0})
        commento = tf_data.get("commento", "").strip()

        scenari_presenti.append(f"{tf}: {direzione.upper()} ({punteggio})")

        # Estrai struttura se presente nel commento
        if "struttura su" in commento.lower():
            for riga in commento.splitlines():
                if "struttura su" in riga.lower():
                    strutture.append(f"{tf} ➤ {riga.strip()}")

        # Comprimiamo bande?
        if "compressione" in commento.lower():
            compressioni.append(f"{tf}")

        blocchi_tf.append(f"🕒 {tf.upper()} ➤ {direzione.upper()} | Punteggio: {punteggio} | Long: {forze.get('long')} – Short: {forze.get('short')} – Neutro: {forze.get('neutro')}")

    sezioni.append("📊 **Scenario per timeframe:**")
    sezioni.extend(blocchi_tf)

    # === 4. Incroci operativi ===
    sezioni.append("\n🔍 **Strutture Tecniche rilevate:**")
    if strutture:
        sezioni.extend([f"- {s}" for s in strutture])
    else:
        sezioni.append("- Nessuna struttura chiaramente definita.")

    sezioni.append("\n📉 **Compressioni attive (Bollinger):**")
    if compressioni:
        sezioni.append(f"- Compressione rilevata su: {', '.join(compressioni)}")
    else:
        sezioni.append("- Nessuna compressione attiva.")

    # === 5. Scenario atteso / Probabilità ===
    sezioni.append("\n📈 **Scenario operativo atteso:**")
    if tendenza == "rialzista":
        sezioni.append("- È probabile una continuazione al rialzo nei prossimi giorni, soprattutto se regge il supporto dinamico sul TF dominante.")
    elif tendenza == "ribassista":
        sezioni.append("- Il mercato appare debole: possibile proseguimento ribassista, salvo rimbalzi da zone tecniche.")
    else:
        sezioni.append("- Il quadro tecnico è incerto: osservare breakout o nuove strutture nei prossimi giorni.")

    sezioni.append(f"\n📌 Scenario sintetico per TF ➤ {', '.join(scenari_presenti)}")

    return "\n".join(sezioni)
