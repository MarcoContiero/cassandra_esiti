def analizza_massimi_minimi(df, timeframe):
    """
    Funzione generata automaticamente per garantire compatibilità Cassandra.
    """
    try:
        if not hasattr(df, 'columns') or 'close' not in df.columns:
            raise ValueError("DataFrame non valido")

        direzione = "neutro"
        scenario = "neutro"
        punteggio = 0

        lookback = min(10, len(df) - 1)
        recent_max = df['high'].iloc[-lookback:].max()
        recent_min = df['low'].iloc[-lookback:].min()
        cur = df['close'].iloc[-1]

        if cur > recent_max:
            scenario = "breakout long"
            direzione = "long"
            punteggio = 0
        elif cur < recent_min:
            scenario = "breakout short"
            direzione = "short"
            punteggio = 0

        return {
            "indicatore": "MASSIMI MINIMI",
            "timeframe": timeframe,
            "scenario": scenario,
            "punteggio": punteggio,
            "direzione": direzione,
            "valore": f"Prezzo: {round(cur, 2)} | Max: {round(recent_max, 2)} | Min: {round(recent_min, 2)}"
        }

    except Exception as e:
        return {
            "indicatore": "MASSIMI MINIMI",
            "timeframe": timeframe,
            "scenario": "errore",
            "punteggio": 0,
            "direzione": "neutro",
            "errore": str(e),
            "valore": "errore"
        }
