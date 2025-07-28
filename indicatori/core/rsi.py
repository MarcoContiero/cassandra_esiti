import pandas as pd
from utils.validazione import valida_dataframe
import numpy as np

@valida_dataframe
def analizza_rsi(df: pd.DataFrame, timeframe: str) -> dict:
    """
    Analizza il Relative Strength Index (RSI).
    """
    try:
        print(f"\n🔍 DEBUG RSI [{timeframe}]")

        # Controllo validità DataFrame
        print(f"📊 Colonne disponibili: {df.columns.tolist()}")
        if not isinstance(df, pd.DataFrame) or 'close' not in df.columns:
            print("❌ Errore: DataFrame non valido o manca colonna 'close'")
            return {
                "indicatore": "RSI",
                "timeframe": timeframe,
                "scenario": "errore",
                "punteggio": 0,
                "direzione": "neutro"
            }

        print(f"📏 Lunghezza dataframe: {len(df)}")
        if len(df) < 20:
            print("⚠️ Non ci sono abbastanza dati per calcolare l'RSI (minimo 20)")
            return {
                "indicatore": "RSI",
                "timeframe": timeframe,
                "scenario": "errore",
                "punteggio": 0,
                "direzione": "neutro"
            }

        # Calcolo variazioni
        chiusure = df['close']
        delta = chiusure.diff()
        print("📈 Delta:\n", delta.tail(5))

        gain = np.where(delta > 0, delta, 0)
        loss = np.where(delta < 0, -delta, 0)
        print("💚 Gain:", gain[-5:])
        print("💔 Loss:", loss[-5:])

        # Medie mobili
        avg_gain = pd.Series(gain).rolling(window=14).mean()
        avg_loss = pd.Series(loss).rolling(window=14).mean()
        print("📊 Avg Gain (ultimi):", avg_gain.tail(3).tolist())
        print("📊 Avg Loss (ultimi):", avg_loss.tail(3).tolist())

        # RSI
        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))
        print("📉 RSI (ultimi):", rsi.tail(3).tolist())

        ultimo_rsi = rsi.iloc[-1]
        print("🎯 Ultimo RSI:", ultimo_rsi)

        if pd.isna(ultimo_rsi):
            scenario = "neutro"
            punteggio = 0
        elif ultimo_rsi < 30:
            scenario = "long"
            punteggio = 4
        elif ultimo_rsi > 70:
            scenario = "short"
            punteggio = 4
        else:
            scenario = "neutro"
            punteggio = 0

        direzione = "long" if scenario == "long" else "short" if scenario == "short" else "neutro"
        print(f"🧭 Scenario: {scenario}, Punteggio: {punteggio}, Direzione: {direzione}")

        return {
            "indicatore": "RSI",
            "timeframe": timeframe,
            "valore": round(ultimo_rsi, 2) if not pd.isna(ultimo_rsi) else "RSI non disponibile",
            "scenario": scenario,
            "punteggio": punteggio,
            "direzione": direzione
        }

    except Exception as e:
        print(f"❌ Errore in analizza_rsi: {e}")
        return {
            "indicatore": "RSI",
            "timeframe": timeframe,
            "scenario": "errore",
            "punteggio": 0,
            "direzione": "neutro"
        }

