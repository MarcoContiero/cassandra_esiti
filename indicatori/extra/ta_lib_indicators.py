
import pandas_ta as ta

def analizza_ta_lib(df, timeframe):
    risultati = []

    close = df["close"]
    high = df["high"]
    low = df["low"]
    open_ = df["open"]
    volume = df["volume"]

    # EMA 21
    df["ema21"] = ta.ema(close, length=21)
    valore = df["ema21"].iloc[-1]
    direzione = "long" if close.iloc[-1] > valore else "short" if close.iloc[-1] < valore else "neutro"
    scenario = f"prezzo {'sopra' if direzione == 'long' else 'sotto' if direzione == 'short' else 'neutro'} media"
    punteggio = 0 if direzione == "neutro" else 3
    risultati.append({
        "indicatore": "EMA 21", "timeframe": timeframe, "valore": round(valore, 2),
        "scenario": scenario, "direzione": direzione, "punteggio": punteggio, "gruppo": "CORE"
    })

    # EMA 50
    df["ema50"] = ta.ema(close, length=50)
    valore = df["ema50"].iloc[-1]
    direzione = "long" if close.iloc[-1] > valore else "short" if close.iloc[-1] < valore else "neutro"
    scenario = f"prezzo {'sopra' if direzione == 'long' else 'sotto' if direzione == 'short' else 'neutro'} media"
    punteggio = 0 if direzione == "neutro" else 3
    risultati.append({
        "indicatore": "EMA 50", "timeframe": timeframe, "valore": round(valore, 2),
        "scenario": scenario, "direzione": direzione, "punteggio": punteggio, "gruppo": "CORE"
    })

    # RSI
    df["rsi"] = ta.rsi(close, length=14)
    valore = df["rsi"].iloc[-1]
    if valore > 70:
        scenario = "ipercomprato"
        direzione = "short"
    elif valore < 30:
        scenario = "ipervenduto"
        direzione = "long"
    else:
        scenario = "neutro"
        direzione = "neutro"
    punteggio = 0 if direzione == "neutro" else 4
    risultati.append({
        "indicatore": "RSI", "timeframe": timeframe, "valore": round(valore, 2),
        "scenario": scenario, "direzione": direzione, "punteggio": punteggio, "gruppo": "MOMENTUM"
    })

    # MACD
    macd = ta.macd(close)
    valore = macd["MACD_12_26_9"].iloc[-1] - macd["MACDs_12_26_9"].iloc[-1]
    scenario = "segnale MACD positivo" if valore > 0 else "segnale MACD negativo" if valore < 0 else "neutro"
    direzione = "long" if valore > 0 else "short" if valore < 0 else "neutro"
    punteggio = 0 if direzione == "neutro" else 4
    risultati.append({
        "indicatore": "MACD", "timeframe": timeframe, "valore": round(valore, 4),
        "scenario": scenario, "direzione": direzione, "punteggio": punteggio, "gruppo": "MOMENTUM"
    })

    # CCI
    df["cci"] = ta.cci(high, low, close, length=20)
    valore = df["cci"].iloc[-1]
    if valore > 100:
        scenario = "ipercomprato"
        direzione = "short"
    elif valore < -100:
        scenario = "ipervenduto"
        direzione = "long"
    else:
        scenario = "neutro"
        direzione = "neutro"
    punteggio = 0 if direzione == "neutro" else 3
    risultati.append({
        "indicatore": "CCI", "timeframe": timeframe, "valore": round(valore, 2),
        "scenario": scenario, "direzione": direzione, "punteggio": punteggio, "gruppo": "MOMENTUM"
    })

    # ADX
    df["adx"] = ta.adx(high, low, close)["ADX_14"]
    valore = df["adx"].iloc[-1]
    scenario = "trend forte" if valore > 25 else "trend debole"
    direzione = "long" if valore > 25 else "neutro"
    punteggio = 3 if valore > 25 else 1
    risultati.append({
        "indicatore": "ADX", "timeframe": timeframe, "valore": round(valore, 2),
        "scenario": scenario, "direzione": direzione, "punteggio": punteggio, "gruppo": "TREND"
    })

    # STOCH
    stoch = ta.stoch(high, low, close)
    valore = stoch["STOCHk_14_3_3"].iloc[-1]
    if valore > 80:
        scenario = "ipercomprato"
        direzione = "short"
    elif valore < 20:
        scenario = "ipervenduto"
        direzione = "long"
    else:
        scenario = "neutro"
        direzione = "neutro"
    punteggio = 0 if direzione == "neutro" else 3
    risultati.append({
        "indicatore": "STOCH", "timeframe": timeframe, "valore": round(valore, 2),
        "scenario": scenario, "direzione": direzione, "punteggio": punteggio, "gruppo": "MOMENTUM"
    })

    # WILLR
    df["willr"] = ta.willr(high, low, close)
    valore = df["willr"].iloc[-1]
    if valore > -20:
        scenario = "ipercomprato"
        direzione = "short"
    elif valore < -80:
        scenario = "ipervenduto"
        direzione = "long"
    else:
        scenario = "neutro"
        direzione = "neutro"
    punteggio = 0 if direzione == "neutro" else 4
    risultati.append({
        "indicatore": "WILLR", "timeframe": timeframe, "valore": round(valore, 2),
        "scenario": scenario, "direzione": direzione, "punteggio": punteggio, "gruppo": "MOMENTUM"
    })

    # TRIX
    df["trix"] = ta.trix(close).iloc[:, 0]  # ← FIX!
    valore = df["trix"].iloc[-1]
    if valore > 0:
        scenario = "momentum positivo"
        direzione = "long"
    elif valore < 0:
        scenario = "momentum negativo"
        direzione = "short"
    else:
        scenario = "neutro"
        direzione = "neutro"
    punteggio = 0 if direzione == "neutro" else 4
    risultati.append({
        "indicatore": "TRIX", "timeframe": timeframe, "valore": round(valore, 4),
        "scenario": scenario, "direzione": direzione, "punteggio": punteggio, "gruppo": "MOMENTUM"
    })

    # DI+ vs DI-
    di = ta.adx(high, low, close)
    valore = di["DMP_14"].iloc[-1] - di["DMN_14"].iloc[-1]
    if valore > 0:
        scenario = "trend bullish"
        direzione = "long"
    elif valore < 0:
        scenario = "trend bearish"
        direzione = "short"
    else:
        scenario = "neutro"
        direzione = "neutro"
    punteggio = 0 if direzione == "neutro" else 2
    risultati.append({
        "indicatore": "DI+ vs DI-", "timeframe": timeframe, "valore": round(valore, 2),
        "scenario": scenario, "direzione": direzione, "punteggio": punteggio, "gruppo": "TREND"
    })

    # NATR
    df["natr"] = ta.natr(high, low, close)
    valore = df["natr"].iloc[-1]
    risultati.append({
        "indicatore": "NATR", "timeframe": timeframe, "valore": round(valore, 2),
        "scenario": "neutro", "direzione": "neutro", "punteggio": 0, "gruppo": "VOLATILITÀ"
    })

    return risultati
