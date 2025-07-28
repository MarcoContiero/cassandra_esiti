import requests
import pandas as pd

def scarica_ohlcv_binance(symbol: str, interval: str, limit: int = 1000) -> pd.DataFrame:
    """
    Scarica dati OHLCV da Binance tramite REST API e restituisce un DataFrame standard.
    """
    symbol = symbol.replace("/", "").upper()
    url = "https://api.binance.com/api/v3/klines"
    params = {"symbol": symbol, "interval": interval, "limit": limit}
    response = requests.get(url, params=params)

    if response.status_code != 200:
        raise RuntimeError(f"Errore API Binance: {response.text}")

    data = response.json()
    if not data:
        raise ValueError(f"Nessun dato ricevuto per {symbol} @ {interval}")

    df = pd.DataFrame(data, columns=[
        "timestamp", "open", "high", "low", "close", "volume",
        "close_time", "quote_asset_volume", "num_trades",
        "taker_buy_base", "taker_buy_quote", "ignore"
    ])

    df = df[["timestamp", "open", "high", "low", "close", "volume"]]
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")

    for col in ["open", "high", "low", "close", "volume"]:
        df[col] = df[col].astype(float)

    return df
