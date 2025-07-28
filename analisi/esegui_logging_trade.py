from entry_exit.calcola_entry_stop_target import calcola_entry_stop_target
from logs.trade_logger import logga_trade

def esegui_logging_trade(nome_coin, dfs, finale):
    try:
        df_ultimo_tf = dfs.get("1d", list(dfs.values())[-1])
        prezzo_corrente = df_ultimo_tf['close'].iloc[-1]
        if finale.get("direzione") in ["long", "short"]:
            result = calcola_entry_stop_target(finale["direzione"], prezzo_corrente)
            logga_trade(
                coin=nome_coin,
                timeframe="1d",
                punteggio_long=finale.get("punteggio_long", 0),
                punteggio_short=finale.get("punteggio_short", 0),
                scenario=finale.get("direzione"),
                entry=result["entry"],
                stop=result["stop"],
                target=result["target"],
                score=finale.get("punteggio_totale", 0)
            )
    except Exception as e:
        print(f"⚠️ Errore logging trade per {nome_coin.upper()}: {e}")
