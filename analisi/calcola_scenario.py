from indicatori.core.calcola_scenario_finale import calcola_scenario_finale

def calcola_scenario(nome_coin, dfs):
    print(f"🧮 DEBUG calcola_scenario per {nome_coin}, dfs disponibili: {list(dfs.keys())}")
    try:
        return calcola_scenario_finale(nome_coin, dfs)
    except Exception as e:
        print(f"⚠️ Errore nel calcolo dello scenario finale: {e}")
        return {}
