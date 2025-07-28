import os
import json
from utils.salva_analisi_completa import salva_analisi_completa
from indicatori.core.calcola_scenario_finale import calcola_scenario_finale




# Per assegnare i gruppi (core/optional)
GRUPPI_PATH = "dati/gruppi_indicatori.json"
with open(GRUPPI_PATH, "r") as f:
    GRUPPI_INDICATORI = json.load(f)

def genera_risultato_finale(nome_coin, risultati, debug=False):
    print(f"🧠 Avvio generazione file finale per {nome_coin}...")

    # Estraggo i dati grezzi per ogni timeframe
    dettagli_per_timeframe = {}
    for tf, lista in risultati.items():
        if not isinstance(lista, list):
            dettagli_per_timeframe[tf] = {"scenario": "errore", "punteggio": 0, "timeframe": tf}
            continue

        if debug:
            print(f"🔍 DEBUG {tf.upper()} - Inizio analisi indicatori")
            print("📋 Tipo df:", type(lista))
            print("📊 Prime righe df:", lista[:2])
            print(f"📦 DEBUG risultati grezzi per {tf}:")

        # Assegna gruppo mancante usando il file gruppi_indicatori
        for indicatore in lista:
            nome = indicatore.get("indicatore", "").lower()
            if "gruppo" not in indicatore or not indicatore["gruppo"]:
                indicatore["gruppo"] = GRUPPI_INDICATORI.get(nome, "optional")

        dettagli_per_timeframe[tf] = {
            "core": [i for i in lista if i.get("gruppo") == "core"],
            "optional": [i for i in lista if i.get("gruppo") == "optional"]
        }

        if debug:
            for i, indicatore in enumerate(lista):
                print(f"  → [{i}] tipo: {type(indicatore)}, valore: {indicatore}")

    if debug:
        print(f"➡️ dettagli_per_timeframe = {dettagli_per_timeframe}")

    # Calcolo lo scenario finale (passando dfs={} per compatibilità)
    risultato_finale = calcola_scenario_finale(risultati, dfs={})

    sezione_forti = "\n\n🌟 Indicatori forti rilevati:\n\n" + risultato_finale.get("blocco_forti", "")

    risultato_finale["dettagli_per_timeframe"] = dettagli_per_timeframe

    if debug:
        print(f"➡️ punteggi_per_timeframe = {risultato_finale.get('punteggi_per_timeframe')}")

    # Genera il testo finale
    testo = salva_analisi_completa(nome_coin, risultato_finale)
    
    supporti_resistenze = ""
    for r in risultati:
        if r.get("indicatore") in ["Supporto", "Resistenza"]:
            emoji = "📉" if r["indicatore"] == "Supporto" else "📈"
            tipo = r["indicatore"]
            valore = r["valore"]
            forza = r.get("forza", "?")
            scenario = r.get("scenario", "n/d")
            supporti_resistenze += f"{emoji} {tipo} {valore:.2f} | forza: {forza} | tipo: {scenario}\n"

    if supporti_resistenze:
        testo += "\n\n📊 Supporti e Resistenze\n" + supporti_resistenze

    # Salva su file
    cartella_output = "analisi_finali"
    os.makedirs(cartella_output, exist_ok=True)
    path_file = os.path.join(cartella_output, f"analisi_{nome_coin.upper()}_completa_finale.txt")
    with open(path_file, "w") as f:
        f.write(testo)

    print(f"💾 File finale salvato in: {path_file}")
    return testo
