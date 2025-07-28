def analizza_fibonacci(df, timeframe):
    """
    Funzione generata automaticamente per garantire compatibilità Cassandra.
    """
    try:
        if not hasattr(df, 'columns') or 'close' not in df.columns:
            raise ValueError("DataFrame non valido")

        direzione = "neutro"
        scenario = "neutro"
        punteggio = 0

        max_close = df['close'].max()
        min_close = df['close'].min()
        livelli = [
            min_close + (max_close - min_close) * lv
            for lv in [0.236, 0.382, 0.5, 0.618, 0.786]
        ]
        cur = df['close'].iloc[-1]
        for lvl in livelli:
            if abs(cur - lvl) / lvl < 0.005:
                scenario = "vicino Fibonacci"
                direzione = "neutro"
                punteggio = 0
                break

        return {
            "indicatore": "FIBONACCI",
            "timeframe": timeframe,
            "scenario": scenario,
            "punteggio": punteggio,
            "direzione": direzione,
            "valore": f"Prezzo: {round(cur, 2)} | Min: {round(min_close, 2)} | Max: {round(max_close, 2)}"
        }

    except Exception as e:
        return {
            "indicatore": "FIBONACCI",
            "timeframe": timeframe,
            "scenario": "errore",
            "punteggio": 0,
            "direzione": "neutro",
            "errore": str(e),
            "valore": "errore"
        }
