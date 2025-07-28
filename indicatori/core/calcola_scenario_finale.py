from indicatori.core.multi_timeframe import analizza_multi_timeframe, costruisci_blocco_multi_tf, analizza_singolo_timeframe
from analisi.genera_riassunti import genera_riassunti
from collections import defaultdict, Counter

def calcola_scenario_finale(indicatori_per_tf: dict, dfs: dict = None) -> dict:
    """
    Calcola scenario finale a partire da indicatori aggregati per timeframe.
    Ogni indicatore deve avere almeno: gruppo, punteggio, direzione.
    """

    if not isinstance(indicatori_per_tf, dict):
        raise ValueError("❌ ERRORE: 'indicatori_per_tf' deve essere un dizionario {timeframe: [indicatori]}")

    punteggi_per_timeframe = {}
    dettagli_per_timeframe = {}
    totale_long = 0
    totale_short = 0
    totale_neutro = 0
    forza_long = 0
    forza_short = 0
    conteggio_timeframe = {}

    for tf, indicatori in indicatori_per_tf.items():
        totale = 0
        somma_long = 0
        somma_short = 0
        somma_neutro = 0

        dettaglio_tf = {
            "core": [],
            "optional": [],
            "extra": [],
        }

        for ind in indicatori:
            gruppo = ind.get("gruppo", "OPTIONAL").upper()
            direzione = ind.get("direzione", "neutro").lower()
            punteggio = ind.get("punteggio", 0)
            try:
                punteggio = float(punteggio)
            except Exception as e:
                print(f"⚠️ ERRORE: punteggio non numerico ({punteggio}) ➤ {e}")
                continue


            #print(f"[{tf}] ➤ {ind.get('indicatore','?')} | gruppo: {gruppo} | punteggio: {punteggio} | direzione: {direzione}")

            if not isinstance(punteggio, (int, float)):
                continue

            totale += punteggio

            if direzione == "long":
                somma_long += punteggio
            elif direzione == "short":
                somma_short += punteggio
            else:
                somma_neutro += punteggio

            gruppo_basso = gruppo.lower()
            if gruppo_basso not in dettaglio_tf:
                dettaglio_tf[gruppo_basso] = []
            dettaglio_tf[gruppo_basso].append(ind)


            if totale == 0:
                punteggi_per_timeframe[tf] = {
                    "totale": 0,
                    "long": 0,
                    "short": 0,
                    "neutro": 0
                }
                dettagli_per_timeframe[tf] = dettaglio_tf
                continue

        punteggi_per_timeframe[tf] = {
            "totale": totale,
            "long": somma_long,
            "short": somma_short,
            "neutro": somma_neutro
        }
        dettagli_per_timeframe[tf] = dettaglio_tf

        # Totali globali
        totale_long += somma_long
        totale_short += somma_short
        totale_neutro += somma_neutro
        conteggio_timeframe[tf] = totale

    # Calcolo finale
    direzione_finale = "neutro"
    delta = abs(totale_long - totale_short)
    punteggio_totale = totale_long + totale_short
    dominante = "n.d."

    if punteggio_totale > 0:
        dominante = max(conteggio_timeframe.items(), key=lambda x: x[1])[0]

        if totale_long > totale_short:
            direzione_finale = "long"
        elif totale_short > totale_long:
            direzione_finale = "short"

    return {
        "scenario_finale": {
            "valore": direzione_finale.upper(),
            "delta": delta,
            "punteggio_totale": punteggio_totale,
            "timeframe_dominante": dominante,
            "forza_long": totale_long,
            "forza_short": totale_short
        },
        "punteggi_per_timeframe": punteggi_per_timeframe,
        "dettagli_per_timeframe": dettagli_per_timeframe,
        "indicatori_forti": [],
        "riassunto_tecnico": "",
        "riassunto_testuale": ""
    }

def descrivi_indicatori_forti(indicatori_forti):
    if not indicatori_forti:
        return ""

    indicatori_per_tf = defaultdict(list)
    for tf, nome in indicatori_forti:
        indicatori_per_tf[tf].append(nome)

    righe = ["\n🧭 Indicatori forti rilevati:"]
    for tf in sorted(indicatori_per_tf.keys(), reverse=True):
        lista = ", ".join(indicatori_per_tf[tf])
        righe.append(f" - {tf}: {lista}")
    
    return "\n".join(righe)

def costruisci_frase_finale(scenario: dict, analisi: list) -> str:
    direzione = scenario["direzione"]
    punteggio = scenario["punteggio_totale"]
    delta = scenario["delta"]
    forza_long = scenario["forza_long"]
    forza_short = scenario["forza_short"]
    dominante = scenario["timeframe_dominante"]

    descrizione = ""
    analisi_compatta = []
    for r in analisi:
        tf = r['timeframe']
        indicatori = r['core'] + r['optional']
        analisi_compatta.append((tf, indicatori))

    # Estrai lista di tutti gli indicatori da tutti i timeframe
    lista_indicatori = []
    for tf, blocco in analisi_compatta.items():
        lista_indicatori.extend(blocco)
        
    frase = f"""🚀 Scenario finale: {'📈 LONG' if direzione == 'long' else '📉 SHORT' if direzione == 'short' else '⚠️ NEUTRO'}

* 💪 Totale forza long: {forza_long}
* ⚔️ Forza opposta: {forza_short}
* ➖ Delta forza: {delta}
* 📊 Punteggio totale: {punteggio}
"""

    # Seleziona frase finale
    if direzione == "neutro":
        frase_finale = "Il segnale è debole o contrastato: al momento non c'è una chiara direzione prevalente."
    elif punteggio >= 100 and delta >= 50:
        frase_finale = "Segnale molto forte e coerente: la tendenza attuale è chiara e supportata da più timeframe."
    elif punteggio >= 80 and delta >= 30:
        frase_finale = "Segnale forte: la maggior parte degli indicatori e dei timeframe concordano sulla direzione."
    elif punteggio >= 60 and delta >= 15:
        frase_finale = "Segnale moderato: ci sono elementi favorevoli, ma la tendenza non è ancora pienamente confermata."
    elif punteggio >= 40:
        frase_finale = "Segnale debole: è presente una direzione prevalente ma ancora poco supportata."
    else:
        frase_finale = "Il segnale è incerto: attendere conferme da altri indicatori o timeframe."

    frase += f"\n{frase_finale}\n"

    if descrizione:
        frase += descrizione

    return frase
