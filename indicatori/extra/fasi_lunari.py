def analizza_fasi_lunari(df, timeframe):
    """
    Analizza la fase lunare corrente per fini simbolici.
    """
    try:
        if not hasattr(df, 'columns') or 'close' not in df.columns:
            raise ValueError("DataFrame non valido")

        import ephem
        last_date = df.index[-1]
        luna = ephem.Moon(last_date)

        # Fase: 0 = nuova, 50 = piena, 100 = nuova
        phase_value = luna.phase
        if phase_value < 7:
            scenario = "Luna nuova"
        elif 7 <= phase_value < 14:
            scenario = "Primo quarto"
        elif 14 <= phase_value < 22:
            scenario = "Luna piena"
        elif 22 <= phase_value < 29:
            scenario = "Ultimo quarto"
        else:
            scenario = "Intermedia"

        direzione = "neutro"
        punteggio = 0

        return {
        "indicatore": "FASI LUNARI",
        "timeframe": timeframe,
        "scenario": scenario,
        "punteggio": punteggio,
        "direzione": direzione,
        "valore": f"fase: {round(phase_value, 2)}"
    }

    except Exception as e:
        return {
            "indicatore": "FASI LUNARI",
            "timeframe": timeframe,
            "scenario": "errore",
            "punteggio": 0,
            "direzione": "neutro",
            "errore": str(e),
            "valore": "errore"
        }
