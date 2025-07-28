
import os
import pandas as pd
import json

from indicatori.core.macd import analizza_macd
from indicatori.core.ema import analizza_ema
from indicatori.core.bollinger import analizza_bollinger
from indicatori.core.rsi import analizza_rsi
from indicatori.core.parabolic_sar import analizza_parabolic_sar
from indicatori.core.volume import analizza_volume
from indicatori.optional.fvg import analizza_fvg
from indicatori.optional.gann_levels import analizza_gann
from indicatori.optional.fibonacci import analizza_fibonacci
from indicatori.optional.analisi_ciclica import analizza_ciclo
from indicatori.optional.pattern_tecnici import analizza_pattern_tecnici
from indicatori.optional.massimi_minimi import analizza_massimi_minimi
from indicatori.optional.ma_cross import analizza_ma_cross
from indicatori.extra.ichimoku import analizza_ichimoku
from indicatori.extra.adx import analizza_adx
from indicatori.extra.fasi_lunari import analizza_fasi_lunari
from indicatori.extra.elliott import analizza_elliott

# Config
NOME_COIN = "AVAXUSDT"
TF_LIST = ["15m", "1h", "4h", "1d", "1w"]
CARTELLA_DATI = "dati_csv"
CARTELLA_GREZZI = "dati_grezzi"

# Crea output
risultati = []

for tf in TF_LIST:
    path_csv = os.path.join(CARTELLA_DATI, f"{NOME_COIN.lower()}_{tf}.csv")
    if not os.path.exists(path_csv):
        print(f"⚠️ File mancante: {path_csv}")
        continue

    df = pd.read_csv(path_csv, index_col=0, parse_dates=True)

    # ✅ Conversione stringhe con virgole in float
    for col in ["open", "high", "low", "close", "volume"]:
        df[col] = df[col].astype(str).str.replace(",", ".").astype(float)

    funzioni = [
        analizza_macd,
        analizza_ema,
        analizza_bollinger,
        analizza_rsi,
        analizza_parabolic_sar,
        analizza_volume,
        analizza_fvg,
        analizza_gann,
        analizza_fibonacci,
        analizza_ciclo,
        analizza_pattern_tecnici,
        analizza_massimi_minimi,
        analizza_ma_cross,
        analizza_ichimoku,
        analizza_adx,
        analizza_fasi_lunari,
        analizza_elliott
    ]

    for funzione in funzioni:
        try:
            risultato = funzione(df.copy(), tf)
            if isinstance(risultato, dict):
                risultati.append(risultato)
        except Exception as e:
            print(f"❌ Errore con {funzione.__name__} @ {tf}: {e}")

# Salva il JSON finale
os.makedirs(CARTELLA_GREZZI, exist_ok=True)
output_path = os.path.join(CARTELLA_GREZZI, f"{NOME_COIN.lower()}_grezzi.json")
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(risultati, f, indent=2, ensure_ascii=False)

print(f"✅ File salvato in: {output_path}")
