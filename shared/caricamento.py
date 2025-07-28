import pandas as pd
import ccxt

def carica_dati(coin: str, timeframe: str, limit: int = 500) -> pd.DataFrame:
    """
    Scarica i dati OHLCV da Binance via ccxt per la coin e timeframe richiesti.
    """
    binance = ccxt.binance()
    symbol = f"{coin.upper().replace('USDT', '')}/USDT"
    tf = timeframe.lower()  # es. '15m'

    try:
        ohlcv = binance.fetch_ohlcv(symbol, timeframe=tf, limit=limit)
        df = pd.DataFrame(ohlcv, columns=["timestamp", "open", "high", "low", "close", "volume"])
        df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
        return df
    except Exception as e:
        raise RuntimeError(f"Errore nel download dei dati per {coin} {timeframe}: {e}")
