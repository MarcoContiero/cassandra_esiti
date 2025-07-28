import os
import pandas as pd
from shared.config import PATH_DATI_CSV
from riassunti.struttura_trend import analizza_struttura_trend as struttura_trend
from riassunti.compressione_volatilita import compressione_volatilita
from riassunti.momentum import valuta_momentum as momentum
from riassunti.volumi import analizza_volumi as volumi
from riassunti.conflitti import valuta_conflitti as conflitti
from riassunti.pattern_operativi import analizza_pattern_operativi as pattern_operativi
from riassunti.livelli_tecnici import analizza_livelli_tecnici as livelli_tecnici
from riassunti.chiusura import genera_blocco_chiusura as chiusura
from utils.estrattori import get_timeframes_from_grezzo

def genera_riassunto_blocchi_singolo_tf(lista_indicatori: list, meta_dati_finali: dict, coin: str, tf: str = None) -> dict:
    print(f"📌 DEBUG ➤ genera_riassunto_blocchi | tf: {tf} | coin: {coin}")

    if meta_dati_finali:
        print(f"📌 DEBUG ➤ meta_dati_finali keys: {list(meta_dati_finali.keys())}")

    # Se tf non è fornito, cerchiamo nei meta_dati
    if tf is None and meta_dati_finali:
        timeframes_meta = meta_dati_finali.get("timeframes", [])
        for tf_locale in timeframes_meta:
            print(f"🔍 DEBUG ➤ TF presente: {tf_locale}")
        tf = timeframes_meta[0] if timeframes_meta else "n.d."

    # Protezione su TF non validi
    if tf is None or tf.lower() in ["n.d.", "d"]:
        raise ValueError(f"❌ ERRORE: TF non valido ➤ tf={tf} per coin={coin}")

    timeframes_analizzati = []
    if meta_dati_finali:
        path = meta_dati_finali.get("path_file_grezzo")
        if path:
            timeframes_analizzati = get_timeframes_from_grezzo(path)

    indicatori_tf = [
        x for x in lista_indicatori
        if isinstance(x, dict) and x.get("timeframe") == tf
    ]

    hh = hl = lh = ll = None

    try:
        coin = meta_dati_finali.get("coin", coin).upper()
        path_csv = os.path.join(PATH_DATI_CSV, f"{coin}_{tf}.csv")

        if os.path.exists(path_csv):
            df_csv = pd.read_csv(path_csv)
            lh = df_csv["high"].iloc[-1]
            ll = df_csv["low"].iloc[-1]
            hh = df_csv["high"].max()
            hl = df_csv["low"].min()
            print(f"🧪 DEBUG ➤ CSV trovato per {coin} {tf}")
            print(f"🧪 DEBUG ➤ hh={hh}, hl={hl}, lh={lh}, ll={ll}")
        else:
            print(f"⚠️ CSV mancante ➤ {path_csv}")
    except Exception as e:
        print(f"❌ Errore durante il calcolo dei livelli per struttura_trend ➤ {e}")

    prezzo = meta_dati_finali.get("prezzo", {}).get(tf) if meta_dati_finali else None
    livelli = meta_dati_finali.get("livelli", {}).get(tf) if meta_dati_finali else None

    if (prezzo is None or not livelli) and os.path.exists(path_csv):
        try:
            df_livelli = pd.read_csv(path_csv)
            prezzo = df_livelli["close"].iloc[-1]
            livelli = {
                "resistenza_1": df_livelli["high"].max(),
                "supporto_1": df_livelli["low"].min()
            }
            print(f"✅ DEBUG ➤ Livelli e prezzo ricavati dal CSV ➤ prezzo={prezzo}, livelli={livelli}")
        except Exception as e:
            print(f"⚠️ DEBUG ➤ Errore nel recupero livelli da CSV ➤ {e}")
            prezzo = None
            livelli = None

    if prezzo is None or livelli is None:
        livelli_tecnici_blocco = {
            "nome": "Livelli tecnici",
            "commento": f"⚠️ Livelli non disponibili su {tf}.",
            "alert": False,
            "timeframe": tf
        }
    else:
        livelli_tecnici_blocco = livelli_tecnici(prezzo, livelli, tf)

    blocchi = [
        struttura_trend(hh, hl, lh, ll, tf),
        compressione_volatilita(indicatori_tf, tf, coin),
        momentum(indicatori_tf, tf),
        volumi(indicatori_tf, tf, coin),
        conflitti(indicatori_tf, tf),
        pattern_operativi(indicatori_tf, tf),
        livelli_tecnici_blocco,
        chiusura(indicatori_tf, tf, livelli)
    ]

    commenti_attivi = []
    alert_attivi = []
    blocchi_attivi = []

    for b in blocchi:
        nome = b.get("nome", "sconosciuto")
        commento = b.get("commento", "")
        alert = b.get("alert", False)

        if commento.strip():
            commenti_attivi.append(f"- {commento}")
            blocchi_attivi.append(b)
        if alert:
            alert_attivi.append(nome)

    commento_finale = f"**Timeframe {tf}**\n\n"
    if commenti_attivi:
        commento_finale += "\n".join(commenti_attivi)
    else:
        commento_finale += "Nessun elemento rilevante identificato."

    if timeframes_analizzati:
        commento_finale += f"\n\n⏱️ Timeframe analizzati: {', '.join(timeframes_analizzati)}"

    if alert_attivi:
        elenco = ", ".join(alert_attivi)
        commento_finale += f"\n\n🔔 Alert attivi: {elenco}"

    return {
        "timeframe": tf,
        "commento_riassuntivo": commento_finale,
        "alert_attivi": alert_attivi,
        "blocchi_attivi": blocchi_attivi
    }
