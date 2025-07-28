import pandas as pd
import ta.volatility

def analizza_bollinger(df, timeframe):
    if not hasattr(df, 'columns') or 'close' not in df.columns:
        return {
            'indicatore': 'Bollinger Bands',
            'scenario': 'errore',
            'punteggio': 0,
            'direzione': 'neutro',
            'timeframe': timeframe
        }

    bb = ta.volatility.BollingerBands(close=df["close"], window=20, window_dev=2)
    upper = bb.bollinger_hband()
    lower = bb.bollinger_lband()
    mid = bb.bollinger_mavg()

    prezzo = df["close"].iloc[-1]
    spread = upper.iloc[-1] - lower.iloc[-1]
    bb_width_pct = (spread / mid.iloc[-1]) * 100 if mid.iloc[-1] != 0 else None
    squeeze = spread / mid.iloc[-1] < 0.05

    if prezzo > upper.iloc[-1]:
        scenario = "breakout rialzista"
        punteggio = 3
    elif prezzo < lower.iloc[-1]:
        scenario = "breakout ribassista"
        punteggio = 3
    elif squeeze:
        scenario = "compressione"
        punteggio = 2
    elif abs(prezzo - mid.iloc[-1]) < spread * 0.1:
        scenario = "prezzo vicino alla media"
        punteggio = 0
    else:
        scenario = "neutro"
        punteggio = 0

    direzione = "long" if "rialzista" in scenario else "short" if "ribassista" in scenario else "neutro"

    return {
        "indicatore": "Bollinger Bands",
        "timeframe": timeframe,
        "valore": round(bb_width_pct, 2) if bb_width_pct else "BB non calcolabili",
        "scenario": scenario,
        "punteggio": punteggio,
        "direzione": direzione
    }
