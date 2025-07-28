import requests
import pandas as pd
import time

def scarica_ohlcv_binance_completo(symbol: str, interval: str = "1d", giorni: int = 1825) -> pd.DataFrame:
    """
    Scarica dati OHLCV storici da Binance andando indietro nel tempo fino a coprire 'giorni' richiesti.
    """
    base_url = "https://api.binance.com/api/v3/klines"
    df_finale = pd.DataFrame()
    fine = int(time.time() * 1000)

    while giorni > 0:
        limite_batch = min(1000, giorni)
        params = {
            "symbol": symbol,
            "interval": interval,
            "limit": limite_batch,
            "endTime": fine
        }

        try:
            response = requests.get(base_url, params=params, timeout=10)
            response.raise_for_status()
            dati = response.json()
        except Exception as e:
            print(f"❌ Errore durante il download: {e}")
            break

        if not dati:
            print("✅ Fine dati storici raggiunta.")
            break

        df_temp = pd.DataFrame(dati, columns=[
            "open_time", "open", "high", "low", "close", "volume",
            "close_time", "quote_asset_volume", "number_of_trades",
            "taker_buy_base_vol", "taker_buy_quote_vol", "ignore"
        ])
        df_temp["open_time"] = pd.to_datetime(df_temp["open_time"], unit="ms")
        df_finale = pd.concat([df_temp, df_finale], ignore_index=True)

        fine = int(df_temp["open_time"].min().timestamp() * 1000) - 1
        giorni -= limite_batch
        time.sleep(0.3)

    return df_finale

# === ESECUZIONE ===
if __name__ == "__main__":
    print("⏳ Scaricamento dati BTCUSDT (giornalieri, ultimi 5 anni)...")
    df_btc = scarica_ohlcv_binance_completo("BTCUSDT", interval="1d", giorni=1825)
    df_btc.to_csv("btc_storico_5anni.csv", index=False)
    print("✅ Dati salvati in: btc_storico_5anni.csv")
