import os
import pandas as pd
from shared.config import PATH_DATI_CSV

def blocco_supporti_resistenze(lista, coin):
    testo = ["# === LIVELLI TECNICI ==="]
    livelli = [r for r in lista if r.get("indicatore") in ["Supporto", "Resistenza"]]
    if not livelli:
        testo.append("Nessun livello tecnico rilevato.")
        return "\n".join(testo)

    supporti = sorted([l for l in livelli if l["indicatore"] == "Supporto"], key=lambda x: -x.get("forza", 0))[:3]
    resistenze = sorted([l for l in livelli if l["indicatore"] == "Resistenza"], key=lambda x: -x.get("forza", 0))[:3]

    testo.append("🔽 **Principali Supporti**")
    for s in supporti:
        testo.append(f"📉 {s['valore']:.2f} | forza: {s.get('forza', '?')} | tipo: {s.get('scenario', 'n/d')}")

    testo.append("\n🔼 **Principali Resistenze**")
    for r in resistenze:
        testo.append(f"📈 {r['valore']:.2f} | forza: {r.get('forza', '?')} | tipo: {r.get('scenario', 'n/d')}")

    path = os.path.join(PATH_DATI_CSV, f"{coin}_1d.csv")
    prezzo = 0
    if os.path.exists(path):
        df = pd.read_csv(path)
        if not df.empty:
            prezzo = df["close"].iloc[-1]

    # Livelli intermedi
    s_max_val = max((s["valore"] for s in supporti), default=0)
    r_min_val = min((r["valore"] for r in resistenze), default=999999)
    intermedi_supporti = [s for s in livelli if s["indicatore"] == "Supporto" and s_max_val < s["valore"] < prezzo]
    intermedi_resistenze = [r for r in livelli if r["indicatore"] == "Resistenza" and prezzo < r["valore"] < r_min_val]
    intermedi = intermedi_supporti + intermedi_resistenze

    if intermedi:
        testo.append("\n⚖️ **Livelli intermedi**")
        for livello in sorted(intermedi, key=lambda x: x["valore"]):
            emoji = "📉" if livello["indicatore"] == "Supporto" else "📈"
            testo.append(f"{emoji} {livello['valore']:.2f} | forza: {livello.get('forza', '?')} | tipo: {livello.get('scenario', 'n/d')}")

    return "\n".join(testo)
