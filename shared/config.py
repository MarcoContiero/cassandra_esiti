# shared/config.py

import os

# Timeframe standard utilizzati in Cassandra
TIMEFRAMES_DEFAULT = ["15m", "1h", "4h", "1d", "1w"]

# Soglia di punteggio oltre la quale scatta un ALERT o segnalazione
SOGLIA_ALERT = 75

# Valore massimo di punteggio totale
MAX_PUNTEGGIO = 100

# Formato file salvataggio dati grezzi (CSV, JSON, Parquet...)
FORMATO_SALVATAGGIO = "json"

# Directory in cui salvare i dati grezzi analizzati
PERCORSO_SALVATAGGIO_DATI = "dati_grezzi"

# Path assoluto per salvataggio
PATH_ANALISI_GREZZE = os.path.join(os.getcwd(), PERCORSO_SALVATAGGIO_DATI)

# Nome del file dati grezzi per singola coin
def nome_file_dati(coin, tf):
    return f"{coin.lower()}_{tf}_grezzi.json"

# Timeframe usati per analisi avanzata (engine)
TIMEFRAMES_ENGINE = ["1h", "4h", "1d"]

PATH_DATI_CSV = "dati_csv"

PATH_ANALISI_FINALI = "analisi_finali"
