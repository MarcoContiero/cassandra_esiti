import os
import pandas as pd

COIN = "ETHUSDT"
TF = "15m"
FILENAME = f"{COIN.lower()}_{TF}.csv"
FULL_PATH = os.path.join("dati_csv", FILENAME)

print("🔍 INIZIO DEBUG CARICAMENTO CSV")

# === 1. Verifica esistenza directory ===
if not os.path.exists("dati_csv"):
    print("❌ Cartella 'dati_csv/' NON trovata.")
else:
    print("✅ Cartella 'dati_csv/' trovata.")
    print("📂 File presenti:")
    for file in os.listdir("dati_csv"):
        print("  •", file)

# === 2. Verifica esistenza file specifico ===
if not os.path.exists(FULL_PATH):
    print(f"❌ File richiesto NON trovato ➤ {FULL_PATH}")
else:
    print(f"✅ File trovato ➤ {FULL_PATH}")

    # === 3. Caricamento del CSV ===
    try:
        df = pd.read_csv(FULL_PATH)
        df.columns = df.columns.str.lower()

        print(f"✅ CSV caricato con successo ({len(df)} righe, {len(df.columns)} colonne)")
        print("📋 Colonne disponibili:", df.columns.tolist())
        print("🧾 Ultime righe:")
        print(df.tail(3))

        # === 4. Controllo colonne fondamentali ===
        colonne_richieste = ["close", "volume"]
        mancanti = [col for col in colonne_richieste if col not in df.columns]
        if mancanti:
            print(f"⚠️ Colonne mancanti: {mancanti}")
        else:
            print("✅ Colonne fondamentali presenti: close, volume")

    except Exception as e:
        print("❌ Errore nel caricamento CSV:", e)

print("🔚 FINE DEBUG")
