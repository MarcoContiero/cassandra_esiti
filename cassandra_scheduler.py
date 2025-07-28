import time
from datetime import datetime
from cass_predittiva import run_predittiva
from cass_riflessiva import run_riflessiva

INTERVALLO_MINUTI = 15

def loop_menti():
    print("🧠 Cassandra Scheduler avviato.")
    while True:
        ora_attuale = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"🔮 [{ora_attuale}] Esecuzione mente predittiva...")
        try:
            run_predittiva()
        except Exception as e:
            print(f"❌ Errore predittiva: {e}")

        print(f"⏳ Attendo {INTERVALLO_MINUTI} minuti per verifica...")
        time.sleep(INTERVALLO_MINUTI * 60)

        ora_attuale = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"🔍 [{ora_attuale}] Esecuzione mente riflessiva...")
        try:
            run_riflessiva()
        except Exception as e:
            print(f"❌ Errore riflessiva: {e}")

        print(f"🔁 Attendo altri {INTERVALLO_MINUTI} minuti per nuovo ciclo.\n")
        time.sleep(INTERVALLO_MINUTI * 60)

if __name__ == "__main__":
    loop_menti()
