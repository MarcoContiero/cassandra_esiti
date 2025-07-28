import pandas as pd
from shared.caricamento import carica_dati

def analizza_volumi(indicatori_tf: list, tf: str, coin: str) -> dict:
    """
    Analizza i volumi e la direzione del prezzo per identificare situazioni anomale o rilevanti.
    Ritorna un blocco con commento, alert e spiegazione.
    """
    try:
        # Prova a caricare i dati dal nome coin passato
        df = carica_dati(coin, tf)
    except Exception as e:
        # Se fallisce, prova a ricavare la coin dagli indicatori
        nomi_coin = [i["coin"] for i in indicatori_tf if "coin" in i]
        if nomi_coin:
            coin2 = nomi_coin[0]
            try:
                df = carica_dati(coin2, tf)
                coin = coin2
            except:
                return {
                    "nome": "Volumi",
                    "commento": f"Errore durante il caricamento dei dati per i volumi su {tf}.",
                    "alert": False,
                    "timeframe": tf
                }
        else:
            return {
                "nome": "Volumi",
                "commento": f"Errore durante il caricamento dei dati per i volumi su {tf}.",
                "alert": False,
                "timeframe": tf
            }

    if len(df) < 3:
        return {
            "nome": "Volumi",
            "commento": f"Dati insufficienti per analizzare i volumi su {tf}.",
            "alert": False,
            "timeframe": tf
        }

    vol_now = df["volume"].iloc[-1]
    vol_prev = df["volume"].iloc[-2]
    close_now = df["close"].iloc[-1]
    close_prev = df["close"].iloc[-2]

    prezzo_in_salida = close_now > close_prev
    volume_in_aumento = vol_now > vol_prev

    if volume_in_aumento and prezzo_in_salida:
        commento = f"Su {tf}, volume in aumento con prezzo in salita."
        alert = True
        spiegazione = "possibile inizio breakout"
    elif volume_in_aumento and not prezzo_in_salida:
        commento = f"Su {tf}, volume in aumento con prezzo in discesa."
        alert = True
        spiegazione = "possibile pressione in vendita"
    elif not volume_in_aumento and prezzo_in_salida:
        commento = f"Su {tf}, prezzo in salita ma volume in calo."
        alert = False
        spiegazione = ""
    elif not volume_in_aumento and not prezzo_in_salida:
        commento = f"Su {tf}, calo di prezzo accompagnato da volumi decrescenti."
        alert = False
        spiegazione = ""
    else:
        commento = f"Situazione neutra sui volumi su {tf}."
        alert = False
        spiegazione = ""

    # Aggiungi la spiegazione nel campo commento se alert attivo
    if alert and spiegazione:
        commento += f": {spiegazione}"

    return {
        "nome": "Volumi",
        "commento": commento,
        "alert": alert,
        "timeframe": tf
    }
