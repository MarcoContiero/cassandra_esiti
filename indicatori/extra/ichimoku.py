import pandas as pd
import ta.trend

def analizza_ichimoku(df, timeframe):
    """
    Analizza l'indicatore Ichimoku (solo Kumo + Tenkan/Kijun) e restituisce uno scenario descrittivo.
    """
    if not hasattr(df, 'columns') or 'close' not in df.columns:
        return {
            'indicatore': 'Ichimoku',
            'scenario': 'errore',
            'punteggio': 0,
            'direzione': 'neutro',
            'timeframe': timeframe
        }

    df = df.copy()

    ichimoku = ta.trend.IchimokuIndicator(
        high=df['high'],
        low=df['low'],
        window1=9,
        window2=26,
        window3=52,
        fillna=True
    )

    df['tenkan'] = ichimoku.ichimoku_conversion_line()
    df['kijun'] = ichimoku.ichimoku_base_line()
    df['senkou_a'] = ichimoku.ichimoku_a()
    df['senkou_b'] = ichimoku.ichimoku_b()

    prezzo = df['close'].iloc[-1]
    tenkan = df['tenkan'].iloc[-1]
    kijun = df['kijun'].iloc[-1]
    senkou_a = df['senkou_a'].iloc[-1]
    senkou_b = df['senkou_b'].iloc[-1]

    kumo_high = max(senkou_a, senkou_b)
    kumo_low = min(senkou_a, senkou_b)

    if prezzo > kumo_high:
        scenario = "prezzo sopra Kumo"
        direzione = "long"
        punteggio = 4
    elif prezzo < kumo_low:
        scenario = "prezzo sotto Kumo"
        direzione = "short"
        punteggio = 4
    else:
        scenario = "prezzo dentro Kumo"
        direzione = "neutro"
        punteggio = 0

    # bonus/malus per Tenkan/Kijun
    if tenkan > kijun and direzione == "long":
        punteggio += 2
    elif tenkan < kijun and direzione == "short":
        punteggio += 2

    return {
        "indicatore": "Ichimoku",
        "timeframe": timeframe,
        "scenario": scenario,
        "punteggio": punteggio,
        "direzione": direzione,
        "valore": f"Prezzo: {round(prezzo, 2)} | Kumo: {round(kumo_low, 2)}–{round(kumo_high, 2)}"
    }
