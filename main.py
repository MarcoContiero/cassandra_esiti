from cass_predittiva import run_predittiva
from cass_riflessiva import run_riflessiva
import time

if __name__ == "__main__":
    print("🚀 Avvio ciclo completo Cassandra + Tre Moire")

    run_predittiva()
    print("⏳ Attendo 15 minuti prima della riflessione...")
    time.sleep(15 * 60)

    run_riflessiva()
    print("✅ Ciclo completo concluso.")
