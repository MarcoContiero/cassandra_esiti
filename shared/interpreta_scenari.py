
import json
import os

# Percorso del file JSON
PERCORSO_REGOLE = os.path.join("regole", "regole_scenari.json")

# Carica le regole degli scenari
def carica_regole_scenari():
    with open(PERCORSO_REGOLE, "r") as f:
        return json.load(f)

# Valuta una singola condizione tra valore e stringa di confronto
def valuta_condizione(valore, condizione):
    if isinstance(condizione, str):
        condizione = condizione.strip()
        if condizione.startswith("<="):
            return valore <= float(condizione[2:])
        elif condizione.startswith(">="):
            return valore >= float(condizione[2:])
        elif condizione.startswith("<"):
            return valore < float(condizione[1:])
        elif condizione.startswith(">"):
            return valore > float(condizione[1:])
        elif condizione.startswith("=="):
            return valore == float(condizione[2:])
        elif condizione.startswith("!="):
            return valore != float(condizione[2:])
        else:
            # confronto letterale
            return valore == condizione
    return valore == condizione

# Applica le regole a un dizionario di indicatori per identificare lo scenario
def interpreta_scenario(indicatori: dict, scenario_prec: str = None) -> str:
    regole = carica_regole_scenari()
    for nome_scenario, dati in regole.items():
        condizioni = dati["condizioni"]
        tutte_ok = True
        for chiave, atteso in condizioni.items():
            if chiave == "scenario_prec":
                if scenario_prec != atteso:
                    tutte_ok = False
                    break
            elif chiave not in indicatori:
                tutte_ok = False
                break
            elif not valuta_condizione(indicatori[chiave], atteso):
                tutte_ok = False
                break
        if tutte_ok:
            return nome_scenario
    return "nessuno"

