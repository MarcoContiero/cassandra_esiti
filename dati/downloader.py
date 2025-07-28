import requests
import pandas as pd

def scarica_ohlcv_binance(symbol: str, interval: str, limit: int = 1000) -> pd.DataFrame:
    intervalli_validi = [
        "1m", "3m", "5m", "15m", "30m",
        "1h", "2h", "4h", "6h", "8h", "12h",
        "1d", "3d", "1w", "1M"
    ]
    if interval not in intervalli_validi:
        raise ValueError(f"❌ Interval non valido per Binance: {interval}")
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
