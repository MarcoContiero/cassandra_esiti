import csv

def genera_classifica_avanzata(dati_classifica: dict, percorso_csv: str = "classifica_avanzata.csv") -> None:
    if not dati_classifica:
        print("⚠️ Nessun dato ricevuto per la classifica avanzata. CSV non generato.")
        return
    """
    Genera un file CSV con la classifica avanzata, includendo per ogni TF:
    - direzione dominante
    - punteggio della direzione dominante
    - delta tra long e short

    E in più:
    - Score totale
    - Direzione globale
    - Delta forza globale
    - TF dominante coerente
    - Emoji scenario
    - Link al file di analisi
    """
    output = []

    for coin, tf_data in dati_classifica.items():
        score_totale = 0
        total_long = 0
        total_short = 0
        tf_riga = {}

        for tf in ["15m", "1h", "4h", "1d", "1w"]:
            if tf not in tf_data:
                tf_riga[f"{tf}_dir"] = "n.d."
                tf_riga[f"{tf}_scr"] = 0
                tf_riga[f"{tf}_dlt"] = 0
                continue

            d = tf_data[tf]
            dir_vincente = d["direzione"]
            punteggio = d.get(f"punteggio_{dir_vincente}", 0)
            delta = abs(d.get("punteggio_long", 0) - d.get("punteggio_short", 0))

            score_totale += d.get("punteggio_long", 0) + d.get("punteggio_short", 0)
            total_long += d.get("punteggio_long", 0)
            total_short += d.get("punteggio_short", 0)

            tf_riga[f"{tf}_dir"] = dir_vincente
            tf_riga[f"{tf}_scr"] = punteggio
            tf_riga[f"{tf}_dlt"] = delta

        # Direzione globale
        if total_long > total_short:
            direzione_globale = "long"
        elif total_short > total_long:
            direzione_globale = "short"
        else:
            direzione_globale = "neutro"

        delta_direzionale = abs(total_long - total_short)

        # TF dominante: massimo delta tra quelli coerenti
        tf_dominante = max(
            [tf for tf in ["15m", "1h", "4h", "1d", "1w"] if tf_riga.get(f"{tf}_dir") == direzione_globale],
            key=lambda x: tf_riga.get(f"{x}_dlt", 0),
            default="n.d."
        )

        emoji = {"long": "📈", "short": "📉", "neutro": "⚠️"}.get(direzione_globale, "❔")

        output.append({
            "Coin": coin,
            **tf_riga,
            "Score Totale": score_totale,
            "Direzione Globale": direzione_globale,
            "Delta Direzione": delta_direzionale,
            "TF Dominante": tf_dominante,
            "Scenario": emoji,
            "Link": tf_data.get("path", "n.d.")
        })

    # Salva CSV
    with open(percorso_csv, mode="w", newline="", encoding="utf-8") as f:
        if not output:
            print("⚠️ Nessun dato da esportare. Classifica avanzata vuota.")
            return
        writer = csv.DictWriter(f, fieldnames=output[0].keys(), delimiter=";")
        writer.writeheader()
        writer.writerows(output)
