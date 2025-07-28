import os
import pandas as pd
from utils.salvataggio import salva_csv
from indicatori.core.rsi import analizza_rsi
from indicatori.core.macd import analizza_macd
from indicatori.core.ema import analizza_ema
from indicatori.core.bollinger import analizza_bollinger
from indicatori.core.parabolic_sar import analizza_parabolic_sar
from indicatori.core.volume import analizza_volume
from indicatori.optional.pattern_tecnici import analizza_pattern_tecnici
from indicatori.optional.fvg import analizza_fvg
from indicatori.optional.gann_levels import analizza_gann
from indicatori.optional.fibonacci import analizza_fibonacci
from indicatori.optional.analisi_ciclica import analizza_ciclo
from indicatori.optional.massimi_minimi import analizza_massimi_minimi
from indicatori.extra.adx import analizza_adx
from indicatori.extra.ichimoku import analizza_ichimoku
from indicatori.extra.fasi_lunari import analizza_fasi_lunari
from shared.caricamento import carica_dati
from indicatori.extra.fasi_lunari import analizza_fasi_lunari
from indicatori.extra.elliott import analizza_elliott
from indicatori.optional.ma_cross import analizza_ma_cross
from costanti import TIMEFRAMES

def carica_e_analizza_dati(nome_coin):
    dfs = {}
    scenari_per_tf = {}
    dettagli_per_timeframe = {}
    


    for tf in TIMEFRAMES:
        try:
            df = carica_dati(tf, nome_coin)
            df.columns = df.columns.str.lower()
            risultati = []

            risultati.extend([
                analizza_rsi(df, tf),
                analizza_macd(df, tf),
                analizza_ema(df, tf),
                analizza_bollinger(df, tf),
                analizza_parabolic_sar(df, tf),
                analizza_volume(df, tf),
            ])

            risultati.extend([
                analizza_pattern_tecnici(df, tf),
                analizza_fvg(df, tf),
                analizza_gann(df, tf),
                analizza_fibonacci(df, tf),
                analizza_ciclo(df, tf),
                analizza_massimi_minimi(df, tf),
                analizza_adx(df, tf),
                analizza_ichimoku(df, tf),
                analizza_fasi_lunari(nome_coin),
            ])

            scenari_per_tf[tf] = risultati
            dettagli_per_timeframe[tf] = risultati
            dfs[tf] = df

            salva_csv(df, f"dati_csv/{nome_coin.lower()}_{tf}.csv")

        except Exception as e:
            print(f"⚠️ Errore analizzando {nome_coin.upper()} [{tf}]: {e}")

    return dfs, scenari_per_tf, dettagli_per_timeframe