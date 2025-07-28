def scrivi_blocchi_analisi(coin: str, blocchi: dict, path: str = None):
    """
    Salva il file completo di analisi Cassandra in formato .txt

    :param coin: codice della coin (es. BTCUSDT)
    :param blocchi: dizionario con tutti i blocchi prodotti da genera_blocchi_analisi_finale
    :param path: percorso personalizzato (default: analisi_{coin}_completa.txt)
    """
    if path is None:
        path = f"analisi_{coin}_completa.txt"

    # === Riassunti per TF ===
    riassunti_tf = blocchi.get("riassunto_per_tf", {})
    contenuto_riassunti_tf = ""
    if isinstance(riassunti_tf, dict):
        for tf, r in riassunti_tf.items():
            contenuto_riassunti_tf += f"\n\n# === RIEPILOGO {tf.upper()} ===\n{r.get('commento_riassuntivo', '').strip()}"

    # === Contenuto finale ===
    contenuto = "\n\n".join([
        blocchi.get("blocco_info", ""),
        blocchi.get("blocco_tf", ""),
        blocchi.get("blocco_tech", ""),
        blocchi.get("blocco_globale", ""),
        blocchi.get("blocco_riepilogo_tf", ""),
        blocchi.get("riassunto_multi_tf", "").strip(),
        contenuto_riassunti_tf.strip(),
        blocchi.get("blocco_commento", ""),
        blocchi.get("blocco_scenari", ""),
        blocchi.get("blocco_commento_scenari", ""),
        blocchi.get("blocco_binance", ""),
        blocchi.get("blocco_forti", ""),
        blocchi.get("blocco_grezzi", ""),
        blocchi.get("blocco_supporti_resistenze", "")
    ])

    # === Scrittura su file ===
    with open(path, "w", encoding="utf-8") as f:
        f.write(contenuto.strip())
