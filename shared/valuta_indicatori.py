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

# EXTRA se presenti
from indicatori.extra.adx import analizza_adx
from indicatori.extra.ichimoku import analizza_ichimoku
from indicatori.extra.fasi_lunari import analizza_fasi_lunari
from indicatori.extra.elliott import analizza_elliott
from indicatori.optional.ma_cross import analizza_ma_cross

def valuta_indicatori(df, tf: str) -> list:
    """
    Valuta tutti gli indicatori su un dataframe e timeframe dati.
    Restituisce una lista di dizionari con i risultati, ognuno dei quali
    include anche il gruppo: 'core' o 'optional'.
    """
    risultati = []

    # === CORE ===
    core_funcs = [
        analizza_rsi,
        analizza_macd,
        analizza_ema,
        analizza_bollinger,
        analizza_parabolic_sar,
        analizza_volume,
    ]
    for func in core_funcs:
        try:
            r = func(df.copy(), tf)
            if r:  # se non None
                r["gruppo"] = "core"
                risultati.append(r)
        except Exception as e:
            print(f"⚠️ Errore {func.__name__}: {e}")

    # === OPTIONAL ===
    optional_funcs = [
        analizza_pattern_tecnici,
        analizza_fvg,
        analizza_gann,
        analizza_fibonacci,
        analizza_ciclo,
        analizza_massimi_minimi,
        analizza_adx,
        analizza_ichimoku,
        analizza_ma_cross,
    ]
    for func in optional_funcs:
        try:
            r = func(df.copy(), tf)
            if r:
                r["gruppo"] = "optional"
                risultati.append(r)
        except Exception as e:
            print(f"⚠️ Errore {func.__name__}: {e}")

    return risultati