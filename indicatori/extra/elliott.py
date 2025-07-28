import pandas as pd
import numpy as np
from ta.momentum import RSIIndicator

def zigzag_semplificato(df: pd.DataFrame, soglia: float = 0.05) -> pd.DataFrame:
    prezzi = df["close"].values
    direction = None
    last_extreme = prezzi[0]
    punti = []

    for i in range(1, len(prezzi)):
        change = (prezzi[i] - last_extreme) / last_extreme

        if direction is None:
            if abs(change) >= soglia:
                direction = "up" if change > 0 else "down"
                punti.append((i, prezzi[i]))
                last_extreme = prezzi[i]
        elif direction == "up":
            if prezzi[i] > last_extreme:
                last_extreme = prezzi[i]
                punti[-1] = (i, prezzi[i])
            elif (last_extreme - prezzi[i]) / last_extreme >= soglia:
                direction = "down"
                punti.append((i, prezzi[i]))
                last_extreme = prezzi[i]
        elif direction == "down":
            if prezzi[i] < last_extreme:
                last_extreme = prezzi[i]
                punti[-1] = (i, prezzi[i])
            elif (prezzi[i] - last_extreme) / last_extreme >= soglia:
                direction = "up"
                punti.append((i, prezzi[i]))
                last_extreme = prezzi[i]

    df_punti = pd.DataFrame(punti, columns=["index", "price"])
    df_punti["timestamp"] = df.iloc[df_punti["index"]]["timestamp"].values
    return df_punti.reset_index(drop=True)

def aggiungi_rsi_volumi(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["rsi"] = RSIIndicator(close=df["close"], window=14).rsi()
    df["volume_norm"] = (df["volume"] - df["volume"].rolling(20).mean()) / df["volume"].rolling(20).std()
    return df

def analizza_elliott(df, timeframe):
    if not hasattr(df, 'columns') or 'close' not in df.columns or 'timestamp' not in df.columns:
        return {
            'indicatore': 'ELLIOTT',
            'scenario': 'errore',
            'punteggio': 0,
            'direzione': 'neutro',
            'valore': "errore"
        }

    df = aggiungi_rsi_volumi(df)
    swing_df = zigzag_semplificato(df, soglia=0.05)

    if len(swing_df) < 7:
        return {
            "indicatore": "ELLIOTT",
            "scenario": "neutro",
            "punteggio": 0,
            "direzione": "neutro",
            "valore": "zigzag insufficiente"
        }

    ultimi = swing_df.tail(7).reset_index(drop=True)
    tipi = []
    for i in range(1, 6):
        if ultimi.loc[i, "price"] > ultimi.loc[i - 1, "price"]:
            tipi.append("H")
        else:
            tipi.append("L")

    if tipi == ["L", "H", "L", "H", "L"]:
        onda_1 = ultimi.loc[1, "price"] - ultimi.loc[0, "price"]
        onda_3 = ultimi.loc[3, "price"] - ultimi.loc[2, "price"]
        onda_5 = ultimi.loc[5, "price"] - ultimi.loc[4, "price"]
        rsi_5 = df["rsi"].iloc[ultimi.loc[5, "index"]]

        if onda_3 > onda_1 and onda_5 > 0 and rsi_5 > 50:
            return {
                "indicatore": "ELLIOTT",
                "timeframe": timeframe,
                "scenario": "onda impulsiva 5",
                "punteggio": 0,
                "direzione": "long",
                "valore": round(rsi_5, 2)
            }

    if tipi[-4:] == ["H", "L", "H", "L"]:
        a = ultimi.loc[2, "price"]
        b = ultimi.loc[3, "price"]
        c = ultimi.loc[4, "price"]
        rsi_c = df["rsi"].iloc[ultimi.loc[4, "index"]]

        if c < a and b < a and rsi_c < 50:
            return {
                "indicatore": "ELLIOTT",
                "timeframe": timeframe,
                "scenario": "correttiva onda C",
                "punteggio": 0,
                "direzione": "short",
                "valore": round(rsi_c, 2)
            }

    return {
        "indicatore": "ELLIOTT",
        "timeframe": timeframe,
        "scenario": "nessun pattern",
        "punteggio": 0,
        "direzione": "neutro",
        "valore": "nessuna onda rilevata"
    }
