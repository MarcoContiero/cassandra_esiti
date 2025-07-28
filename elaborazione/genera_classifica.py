
import os
import pandas as pd
from analisi.analizza_coin_completa import analizza_coin_completa

def genera_classifica_base(lista_path="lista_coin.txt", salva_csv=True):
    with open(lista_path, "r") as f:
        coins = [line.strip().upper() for line in f if line.strip()]

    risultati = []

    for coin in coins:
        print(f"🔄 Analisi in corso per {coin}...")
        try:
            blocchi = analizza_coin_completa(coin)
            scenario = blocchi["risultato_finale"].get("scenario_finale", {})
            risultati.append({
                "Coin": coin,
                "Scenario": scenario.get("valore", "n.d."),
                "Delta": scenario.get("delta", 0),
                "Forza Long": scenario.get("forza_long", 0),
                "Forza Short": scenario.get("forza_short", 0),
                "Punteggio Totale": scenario.get("punteggio_totale", 0),
                "Dominante": scenario.get("timeframe_dominante", "n.d."),
                "File Analisi": f"analisi_{coin}_completa.txt"
            })
        except Exception as e:
            print(f"❌ Errore con {coin}: {e}")
            risultati.append({
                "Coin": coin,
                "Scenario": "errore",
                "Delta": "-",
                "Forza Long": "-",
                "Forza Short": "-",
                "Punteggio Totale": "-",
                "Dominante": "-",
                "File Analisi": "-"
            })

    df = pd.DataFrame(risultati)
    df = df.sort_values(by="Punteggio Totale", ascending=False)

    if salva_csv:
        print("📄 Scrittura file: classifica.csv (base)")
        df.to_csv("classifica.csv", index=False)

    return df
