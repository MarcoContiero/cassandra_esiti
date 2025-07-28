from collections import defaultdict, Counter
from elaborazione.calcola_range_ingresso import calcola_range_ingresso
from elaborazione.estrai_scenario_dominante import estrai_scenario_dominante

def genera_riepilogo_timeframe(lista_indicatori: list) -> dict:
    """
    Genera un riepilogo per ogni timeframe:
    {
        "15m": {
            "scenario": "Trend forte in atto",
            "punteggio": 32,
            "direzione": "short",
            "range": "3730–3760"
        },
        ...
    }
    """
    tf_riepilogo = defaultdict(list)

    for indicatore in lista_indicatori:
        tf = indicatore.get("timeframe", "n/d")
        tf_riepilogo[tf].append(indicatore)

    risultato = {}

    for tf, indicatori in tf_riepilogo.items():
        totale_punteggio = 0
        punteggi_direzione = defaultdict(float)

        for ind in indicatori:
            punteggio = ind.get("punteggio", 0) or 0
            direzione = ind.get("direzione", "neutro")
            totale_punteggio += punteggio
            punteggi_direzione[direzione] += punteggio

        direzione_dominante = max(punteggi_direzione, key=punteggi_direzione.get, default="neutro")

        risultato[tf] = {
            "scenario": estrai_scenario_dominante(indicatori),
            "punteggio": totale_punteggio,
            "direzione": direzione_dominante,
            "range": calcola_range_ingresso(indicatori)
        }

    return dict(risultato)
