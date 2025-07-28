import pandas as pd
from shared.caricamento import carica_dati

def compressione_volatilita(indicatori_tf: list, tf: str, coin: str) -> dict:
    """
    Carica i dati per il timeframe specificato e analizza la compressione delle Bollinger Bands.
    """
    print(f"🐞 DEBUG ➤ Chiamata a carica_dati con coin={coin}, tf={tf}")

    df = carica_dati(coin, tf)
    return analizza_compressione_bollinger(df, tf)

def analizza_compressione_bollinger(df, tf: str) -> dict:
    """
    Analizza la compressione delle Bande di Bollinger e identifica:
    - compressione attiva
    - eventuale rottura (breakout)
    - direzione
    - commento strategico
    - alert operativo

    Richiede un dataframe con colonne: 'close', 'high', 'low', 'volume'
    """
    print(f"📊 DEBUG ➤ Ricevuti {len(df)} dati per TF {tf} (tipo: {type(df)})")

    risultato = {
        "compressione": False,
        "rottura": False,
        "direzione": "neutro",
        "commento": "",
        "alert": False,
        "timeframe": tf
    }

    # Se è una lista, convertila in DataFrame
    if isinstance(df, list):
        print(f"📦 DEBUG ➤ Esempio contenuto lista: {df[:2]}")
        df = pd.DataFrame(df)


    # Verifica presenza colonne richieste
    colonne_richieste = ["close", "high", "low", "volume"]
    if len(df) < 20 or any(col not in df.columns for col in colonne_richieste):
        print(f"⚠️ DEBUG ➤ Colonne disponibili: {df.columns.tolist()}")
        risultato["commento"] = f"Dati insufficienti o non validi per valutare la compressione su {tf}."
        return risultato

    window = 20
    df = df.copy()
    df["ma20"] = df["close"].rolling(window=20).mean()
    df["stddev"] = df["close"].rolling(window=20).std()
    df["boll_upper"] = df["ma20"] + 2 * df["stddev"]
    df["boll_lower"] = df["ma20"] - 2 * df["stddev"]
    df["boll_range"] = df["boll_upper"] - df["boll_lower"]
    df["boll_pct"] = df["boll_range"] / df["ma20"]

    banda_media = df["boll_pct"].iloc[-20:].mean()
    banda_attuale = df["boll_pct"].iloc[-1]
    soglia = 0.75 * banda_media
    in_compressione = banda_attuale < soglia

    chiusura = df["close"].iloc[-1]
    upper = df["boll_upper"].iloc[-1]
    lower = df["boll_lower"].iloc[-1]

    rottura_alto = chiusura > upper
    rottura_basso = chiusura < lower
    rottura = rottura_alto or rottura_basso

    if in_compressione and not rottura:
        risultato.update({
            "compressione": True,
            "commento": f"Compressione attiva sulle bande di Bollinger su {tf}. Il prezzo è ancora dentro il canale. Possibile esplosione imminente.",
            "alert": True,
            "direzione": "neutro"
        })
    elif rottura:
        direzione = "long" if rottura_alto else "short"
        risultato.update({
            "compressione": False,
            "rottura": True,
            "direzione": direzione,
            "commento": f"Rottura {direzione} di una fase di compressione su {tf}. Il prezzo è uscito dalla banda {'superiore' if direzione == 'long' else 'inferiore'}.",
            "alert": True
        })
    else:
        risultato["commento"] = f"Nessuna compressione o breakout rilevante sulle bande di Bollinger su {tf}."

    return risultato
