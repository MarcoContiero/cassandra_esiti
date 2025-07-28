def scrivi_blocchi_analisi(coin: str, blocchi: dict, modalita: str):
    import os

    # Costruzione del nome file in base alla modalità
    nome_file = f"analisi_finali/analisi_{coin.lower()}_{modalita.lower()}.txt"
    os.makedirs("analisi_finali", exist_ok=True)

    # Blocco sempre presente
    contenuti = [
        "# === RIASSUNTO COMPLETO ===",
        blocchi["blocco_info"],
    ]

    # Riassunto strategico multi-TF sempre presente
    contenuti.append("# === RIASSUNTO STRATEGICO MULTI-TF ===")
    contenuti.append(blocchi["riassunto_multi_tf"])

    if modalita.lower() == "completo":
        contenuti.extend([
            "# === RIASSUNTO CASSANDRA ===\n" + blocchi["riassunto_finale"],
            blocchi["blocco_tf"],
            blocchi["blocco_tech"],
            blocchi["blocco_globale"],
            blocchi["blocco_riepilogo_tf"],
            blocchi["blocco_commento"],
            blocchi["blocco_scenari"],
            blocchi["blocco_commento_scenari"],
            blocchi["blocco_forti"],
            blocchi["blocco_binance"],
            blocchi["blocco_supporti_resistenze"],
            blocchi["blocco_grezzi"]
        ])

    elif modalita.lower() == "cassandra":
        contenuti.extend([
            "# === RIASSUNTO CASSANDRA ===\n" + blocchi["riassunto_finale"],
            blocchi["blocco_tf"],
            blocchi["blocco_tech"],
            blocchi["blocco_globale"],
            blocchi["blocco_riepilogo_tf"],
            blocchi["blocco_commento"],
            blocchi["blocco_scenari"],
            blocchi["blocco_commento_scenari"],
            blocchi["blocco_forti"],
            blocchi["blocco_supporti_resistenze"],
            blocchi["blocco_grezzi"]
        ])

    # modalità "bot" include solo info + riassunto già scritti

    # Salvataggio su file
    with open(nome_file, "w") as f:
        f.write("\n\n".join(contenuti).strip())
