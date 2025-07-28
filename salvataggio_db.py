import sqlite3
import os
import json
from datetime import datetime
from upload_to_drive import carica_db_su_drive
import shutil

def salva_analisi_db(coin: str, timeframe: str, risultato: dict):
    # 📁 Directory dinamica
    base_dir = "/mnt/data" if os.path.exists("/mnt/data") else "."

    # 🕒 Timestamp per nome file
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    # 📄 Nome file dinamico
    nome_file_db = f"cassandra_analisi_{timestamp}.db"
    db_path = os.path.join(base_dir, nome_file_db)

    # 🧠 (Facoltativo) anche una copia "latest"
    latest_path = os.path.join(base_dir, "cassandra_analisi_latest.db")

    # 📦 Crea DB
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Crea tabella se non esiste
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS analisi (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            coin TEXT,
            timeframe TEXT,
            data TEXT,
            scenario TEXT,
            punteggio FLOAT,
            direzione TEXT,
            indicatori_forti TEXT,
            dettagli TEXT
        )
    """)

    # Inserisci i dati
    now = datetime.now().isoformat()
    scenario = risultato.get("scenario", "n.d.")
    punteggio = risultato.get("punteggio", 0.0)
    direzione = risultato.get("direzione", "neutro")
    indicatori = json.dumps(risultato.get("indicatori_forti", []))
    dettagli = json.dumps(risultato)

    cursor.execute("""
        INSERT INTO analisi (coin, timeframe, data, scenario, punteggio, direzione, indicatori_forti, dettagli)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (coin, timeframe, now, scenario, punteggio, direzione, indicatori, dettagli))

    conn.commit()
    conn.close()

    print(f"✅ Analisi salvata su {db_path}")

    # 🧾 Copia come "latest" locale
    try:
        shutil.copyfile(db_path, latest_path)
        print(f"🕒 Copia aggiornata: {latest_path}")
    except Exception as e:
        print(f"⚠️ Errore nel creare copia latest: {e}")

    # ☁️ Upload su Drive
    try:
        carica_db_su_drive(db_path)
    except Exception as e:
        print(f"⚠️ Upload su Google Drive fallito: {e}")
