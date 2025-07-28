from indicatori.core.multi_timeframe import costruisci_blocco_multi_tf

def calcola_multi_timeframe(scenari_per_tf):
    try:
        return costruisci_blocco_multi_tf(scenari_per_tf)
    except Exception as e:
        print(f"⚠️ Errore nel calcolo multi-timeframe: {e}")
        return {}, {}
