import pandas as pd
from datetime import datetime
from dati.downloader import scarica_ohlcv_binance

# === Caricamento lista da file ===
def carica_lista_coin():
    with open("config/lista_coin.txt", "r") as f:
        return [riga.strip().upper() for riga in f if riga.strip()]

# === Estrazione massimi per ogni mese ===
def trova_massimi_mensili(df: pd.DataFrame, coin: str) -> pd.DataFrame:
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["anno"] = df["timestamp"].dt.year
    df["mese"] = df["timestamp"].dt.month
    df["giorno"] = df["timestamp"].dt.day

    massimi = []

    for (anno, mese), gruppo in df.groupby(["anno", "mese"]):
        idx_max = gruppo["high"].idxmax()
        riga_max = gruppo.loc[idx_max]
        massimi.append({
            "Coin": coin,
            "Anno": anno,
            "Mese": mese,
            "Giorno Max": riga_max["giorno"],
            "Prezzo Max": riga_max["high"]
        })

    return pd.DataFrame(massimi)

# === Ciclo completo ===
def analizza_massimi_per_classifica():
    lista_coin = carica_lista_coin()
    tutti_massimi = []

    for coin in lista_coin:
        try:
            df = scarica_ohlcv_binance(coin, interval="1d", limit=3000)
            if df is None or df.empty:
                print(f"Nessun dato per {coin}")
                continue
            massimi_df = trova_massimi_mensili(df, coin)
            tutti_massimi.append(massimi_df)
        except Exception as e:
            print(f"❌ Errore con {coin}: {e}")

    if tutti_massimi:
        risultato = pd.concat(tutti_massimi, ignore_index=True)
        risultato.to_csv("massimi_mensili_classifica.csv", sep=";", index=False)
        print("✅ File salvato: massimi_mensili_classifica.csv")
        return risultato
    else:
        print("⚠️ Nessun dato elaborato.")
        return pd.DataFrame()

# === Esecuzione diretta ===
if __name__ == "__main__":
    analizza_massimi_per_classifica()
