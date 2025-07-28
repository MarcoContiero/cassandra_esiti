import importlib
import pkgutil
import inspect

def get_funzioni_indicatori():
    cartelle = [
        "indicatori.core",
        "indicatori.optional",
        "indicatori.extra"
    ]

    funzioni = {}
    nomi_ignorati = ["analizza_singolo_timeframe", "analizza_multi_timeframe"]

    for cartella in cartelle:
        pacchetto = importlib.import_module(cartella)
        for _, nome_modulo, _ in pkgutil.iter_modules(pacchetto.__path__):
            modulo_path = f"{cartella}.{nome_modulo}"
            try:
                modulo = importlib.import_module(modulo_path)
            except Exception as e:
                print(f"❌ Errore importazione {modulo_path}: {e}")
                continue

            for nome, funzione in inspect.getmembers(modulo, inspect.isfunction):
                if nome.startswith("analizza_") and nome not in nomi_ignorati:
                    if callable(funzione):
                        if nome not in funzioni:
                            funzioni[nome] = funzione
                    else:
                        print(f"❌ Funzione non callable: {nome} (tipo: {type(funzione)})")

    for nome, funzione in funzioni.items():
        print(f"  🔹 {nome} ➤ {getattr(funzione, '__name__', str(type(funzione)))}")

    return funzioni

