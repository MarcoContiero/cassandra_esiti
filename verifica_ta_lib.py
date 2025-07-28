
import pandas as pd
from indicatori.extra.ta_lib_indicators import analizza_ta_lib
from dati.downloader import scarica_ohlcv_binance

def test_ta_lib():
    coin = "BTCUSDT"
    timeframe = "1h"
    df = scarica_ohlcv_binance(coin, timeframe, limit=300)

    risultati = analizza_ta_lib(df, timeframe)

    errori = []
    for r in risultati:
        if r["punteggio"] < 0:
            errori.append(f"❌ ERRORE: {r['indicatore']} ha punteggio negativo: {r['punteggio']}")
        if r["direzione"] == "neutro" and r["punteggio"] != 0:
            errori.append(f"❌ ERRORE: {r['indicatore']} è neutro ma ha punteggio {r['punteggio']}")
        if r["direzione"] in ["long", "short"] and r["punteggio"] == 0:
            errori.append(f"❌ ERRORE: {r['indicatore']} ha direzione {r['direzione']} ma punteggio 0")

    if not errori:
        print("✅ Tutti gli indicatori TA-Lib sono corretti.")
    else:
        print("\n".join(errori))

if __name__ == "__main__":
    test_ta_lib()
