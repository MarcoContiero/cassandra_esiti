import pandas as pd
from typing import List, Dict, Any
from indicatori.core.rsi import analizza_rsi
from indicatori.core.macd import analizza_macd
from indicatori.core.bollinger import analizza_bollinger
from indicatori.core.ema import analizza_ema
from indicatori.extra.adx import analizza_adx
from indicatori.core.parabolic_sar import analizza_parabolic_sar
from indicatori.optional.ma_cross import analizza_ma_cross
from indicatori.optional.massimi_minimi import analizza_massimi_minimi
from indicatori.optional.pattern_tecnici import analizza_pattern_tecnici
from indicatori.optional.fvg import analizza_fvg
from indicatori.optional.fibonacci import analizza_fibonacci
from indicatori.optional.gann_levels import analizza_gann
from indicatori.extra.ichimoku import analizza_ichimoku
from indicatori.core.volume import analizza_volume
from indicatori.extra.fasi_lunari import analizza_fasi_lunari
from indicatori.extra.elliott import analizza_elliott
from indicatori.optional.analisi_ciclica import analizza_ciclo

def analizza_tutti_indicatori(nome_coin: str, df, timeframes: list) -> dict:
    if not isinstance(df, pd.DataFrame):
        return {
            "errore": "Input non valido: df non è un DataFrame",
            "risultati": [],
            "timeframes": timeframes
        }

    funzioni_callabili = {
        "analizza_rsi": analizza_rsi,
        "analizza_macd": analizza_macd,
        "analizza_bollinger": analizza_bollinger,
        "analizza_ema": analizza_ema,
        "analizza_adx": analizza_adx,
        "analizza_parabolic_sar": analizza_parabolic_sar,
        "analizza_ma_cross": analizza_ma_cross,
        "analizza_massimi_minimi": analizza_massimi_minimi,
        "analizza_pattern_tecnici": analizza_pattern_tecnici,
        "analizza_fvg": analizza_fvg,
        "analizza_fibonacci": analizza_fibonacci,
        "analizza_gann": analizza_gann,
        "analizza_ichimoku": analizza_ichimoku,
        "analizza_volume": analizza_volume,
        "analizza_fasi_lunari": analizza_fasi_lunari,
        "analizza_elliott": analizza_elliott,
        "analizza_ciclo": analizza_ciclo,
    }

    risultati = []
    print(f"\n🔍 DEBUG ➤ Trovate {len(funzioni_callabili)} funzioni indicatore")
    print("────────────────────────────────────────")

    for i, (nome, funzione) in enumerate(funzioni_callabili.items(), start=1):
        print(f"🔍 Funzione #{i}/{len(funzioni_callabili)} ➤ {nome}")
        print(f"➡️  Tipo: {type(funzione)}, Callable: {callable(funzione)}")

        if callable(funzione):
            try:
                risultato = funzione(df, timeframes)
                risultati.append(risultato)
                print(f"✅ {nome} → OK")
            except Exception as e:
                print(f"❌ Errore in {nome}: {e}")
        else:
            print(f"⚠️ Oggetto non callabile ({nome}), ignorato.")
        print("────────────────────────────────────────")

    print(f"\n📦 Totale risultati validi: {len(risultati)}\n")
    return risultati
