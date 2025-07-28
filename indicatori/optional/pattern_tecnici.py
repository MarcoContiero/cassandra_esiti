import pandas as pd
from utils.validazione import valida_dataframe

@valida_dataframe
def analizza_pattern_tecnici(df: pd.DataFrame, timeframe: str) -> dict:
    """
    Analizza i pattern candlestick principali e assegna punteggio e scenario.
    Include: Engulfing, Doji, Hammer, Evening Star (semplificata).
    """

    def is_bullish_engulfing(prev, curr):
        return (
            prev['close'] < prev['open'] and
            curr['close'] > curr['open'] and
            curr['close'] > prev['open'] and
            curr['open'] < prev['close']
        )

    def is_bearish_engulfing(prev, curr):
        return (
            prev['close'] > prev['open'] and
            curr['close'] < curr['open'] and
            curr['open'] > prev['close'] and
            curr['close'] < prev['open']
        )

    def is_doji(candle):
        return abs(candle['close'] - candle['open']) <= (candle['high'] - candle['low']) * 0.1

    def is_hammer(candle):
        body = abs(candle['close'] - candle['open'])
        lower_shadow = candle['open'] - candle['low'] if candle['open'] < candle['close'] else candle['close'] - candle['low']
        upper_shadow = candle['high'] - max(candle['close'], candle['open'])
        return lower_shadow > 2 * body and upper_shadow < body

    pattern = "Nessun pattern"
    scenario = "neutro"
    direzione = "neutro"
    punteggio = 0

    if len(df) < 4:
        return {
            "indicatore": "Pattern Tecnici",
            "timeframe": timeframe,
            "scenario": scenario,
            "pattern": pattern,
            "punteggio": punteggio,
            "direzione": direzione
        }

    last = df.iloc[-1]
    prev = df.iloc[-2]
    prev2 = df.iloc[-3]

    if is_bullish_engulfing(prev, last):
        pattern = "Bullish Engulfing"
        scenario = "long"
        direzione = "long"
        punteggio = 6
    elif is_bearish_engulfing(prev, last):
        pattern = "Bearish Engulfing"
        scenario = "short"
        direzione = "short"
        punteggio = 6
    elif is_doji(last):
        pattern = "Doji"
        scenario = "neutro"
        direzione = "neutro"
        punteggio = 3
    elif is_hammer(last):
        pattern = "Hammer"
        scenario = "long"
        direzione = "long"
        punteggio = 4
    elif (
        prev2['close'] > prev2['open'] and
        prev['close'] < prev['open'] and
        last['close'] < last['open'] and
        last['close'] < prev['close']
    ):
        pattern = "Evening Star (semplificata)"
        scenario = "short"
        direzione = "short"
        punteggio = 6

    return {
        "indicatore": "Pattern Tecnici",
        "timeframe": timeframe,
        "scenario": scenario,
        "pattern": pattern,
        "punteggio": punteggio,
        "direzione": direzione,
        "valore": pattern
    }

