import pandas as pd
import ta.trend

def analizza_macd(df: pd.DataFrame, timeframe: str) -> dict:
    """
    Analizza il MACD sul dataframe fornito e restituisce punteggio e scenario.
    """
    try:
        macd_indicator = ta.trend.MACD(close=df['close'])

        macd_line = macd_indicator.macd()
        signal_line = macd_indicator.macd_signal()
        macd_hist = macd_indicator.macd_diff()

        macd_now = macd_line.iloc[-1]
        signal_now = signal_line.iloc[-1]
        hist_now = macd_hist.iloc[-1]

        macd_prev = macd_line.iloc[-2]
        signal_prev = signal_line.iloc[-2]
        hist_prev = macd_hist.iloc[-2]

        if macd_prev < signal_prev and macd_now > signal_now and hist_now > hist_prev:
            scenario = "incrocio rialzista MACD"
            direzione = "long"
            punteggio = 3
        elif macd_prev > signal_prev and macd_now < signal_now and hist_now < hist_prev:
            scenario = "incrocio ribassista MACD"
            direzione = "short"
            punteggio = 3
        elif macd_now > 0 and abs(hist_now) < 0.1:
            scenario = "debole rialzo MACD"
            direzione = "long"
            punteggio = 2
        elif macd_now < 0 and hist_now < hist_prev:
            scenario = "rafforzamento ribasso MACD"
            direzione = "short"
            punteggio = 2
        else:
            scenario = "neutro"
            direzione = "neutro"
            punteggio = 0

        return {
            "indicatore": "MACD",
            "timeframe": timeframe,
            "valore": f"MACD: {round(macd_now, 2)} / Signal: {round(signal_now, 2)}",
            "scenario": scenario,
            "punteggio": punteggio,
            "direzione": direzione
        }

    except Exception:
        return {
            "indicatore": "MACD",
            "timeframe": timeframe,
            "valore": "Errore",
            "scenario": "errore",
            "punteggio": 0,
            "direzione": "neutro"
        }
