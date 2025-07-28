import pandas as pd
from functools import wraps

def valida_dataframe(f):
    @wraps(f)
    def wrapper(df, *args, **kwargs):
        if not isinstance(df, pd.DataFrame):
            return {
                "scenario": "errore",
                "punteggio": 0,
                "direzione": "neutro",
                "errore": "Input non è un DataFrame"
            }
        try:
            return f(df, *args, **kwargs)
        except Exception as e:
            return {
                "scenario": "errore",
                "punteggio": 0,
                "direzione": "neutro",
                "errore": str(e)
            }
    return wrapper
