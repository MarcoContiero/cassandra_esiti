def analizza_fvg(df, timeframe):
    """
    Funzione generata automaticamente per garantire compatibilità Cassandra.
    """
    try:
        if not hasattr(df, 'columns') or 'close' not in df.columns:
            raise ValueError("DataFrame non valido")

        direzione = "neutro"
        scenario = "neutro"
        punteggio = 0

        if len(df) >= 3:
            high_n2 = df['high'].iloc[-3]
            low_n = df['low'].iloc[-1]
            if low_n > high_n2:
                scenario = "FVG long"
                direzione = "long"
                punteggio = 2
            else:
                high_n = df['high'].iloc[-1]
                low_n2 = df['low'].iloc[-3]
                if high_n < low_n2:
                    scenario = "FVG short"
                    direzione = "short"
                    punteggio = 2

        return {
            "indicatore": "FVG",
            "timeframe": timeframe,
            "scenario": scenario,
            "punteggio": punteggio,
            "direzione": direzione,
            "valore": scenario if scenario != "neutro" else "nessuna FVG"
        }

    except Exception as e:
        return {
            "indicatore": "FVG",
            "timeframe": timeframe,
            "scenario": "errore",
            "punteggio": 0,
            "direzione": "neutro",
            "errore": str(e),
            "valore": "errore"
        }
