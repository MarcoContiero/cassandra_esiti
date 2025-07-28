
# 📘 Cassandra — Changelog

### 🧶 Modalità Tre Moire (Work in progress)

*Tessere, misurare, recidere. Il tempo prende forma.*

Cassandra osserva il tempo: ciò che è stato, ciò che è, e ciò che può essere...

Cloto tesse il ricordo dei mercati passati. Lachesi misura l’equilibrio del presente. Atropo osserva il futuro con le forbici in mano.
Ogni movimento ha una storia, una forma e un destino. Cassandra le ascolta tutte, prima di decidere.

🔮 Descrizione concettuale
La Modalità Tre Moire è ispirata alle tre divinità del destino della mitologia greca: Cloto, Lachesi e Atropo. Ognuna incarna un momento chiave della linea temporale e una funzione precisa all'interno del processo di analisi di Cassandra:
* 🧵 Cloto (il Passato) – Filtra la memoria del mercato. → Pattern storici, cicli, comportamenti ricorrenti
* 📏 Lachesi (il Presente) – Valuta la condizione attuale. → Struttura tecnica, volumi, trend, volatilità
* ✂️ Atropo (il Futuro) – Decide il taglio operativo. → Scenari probabilistici, segnali di breakout o inversione
In questa modalità, Cassandra non giudica un segnale in modo univoco, ma lo elabora su tre piani temporali distinti, ognuno con la sua logica, per poi sintetizzare in un’unica visione.

🧠 Funzionamento tecnico
Moira	Analisi tecnica associata	Output tipico
Cloto	Cicli temporali, pattern storici, RSI storica	“Pattern simile nel 2021 → outcome X”
Lachesi	Trend attuale, medie mobili, volumi, BB	“Struttura attuale: compressione + divergenza”
Atropo	Scenari predittivi, breakout, AI (se attiva)	“Alta probabilità di inversione nelle prossime 4 candele”

💬 Output in linguaggio naturale (esempio)
“🧶 Tre Moire attive: Cloto evidenzia un ciclo ricorrente compatibile con il pattern attuale. Lachesi registra compressione di volatilità con trend neutro. Atropo rileva rischio di inversione con break sotto 1.200. ✂️ Decisione: attesa operativa, possibile entrata a conferma.”

🧷 Quando usare questa modalità
* Quando serve una valutazione temporale completa, non solo un’istantanea
* Quando vuoi che Cassandra operi con prudenza strategica, osservando le implicazioni di passato, presente e futuro
* Per analisi multi-timeframe o contesti ad alta incertezza


## ✅ Versione 1.4 (2025-07-27)

- ✅ Riepilogo per timeframe (dashboard avanzata)
- Per ogni coin e timeframe, mostrare:
  `TF | Scenario | Punteggio | Direzione | Range ingresso`
- Da integrare nella **classifica** e nel file `.txt` dell’analisi singola

- ✅ Riepilogo finale con frase personalizzata per scenario
- Frase automatica che cambia in base allo **scenario dominante**
  - Esempi: “Breakout in consolidamento”, “Possibile inversione ribassista”
- Sostituisce la frase finale generica nel report

- ✅ Range d’ingresso suggerito
- Calcolato da livelli tecnici (EMA, Bollinger, FVG, ecc.)
- Mostrato accanto a punteggio e direzione
- Usato anche nel riepilogo per timeframe

- ✅ Alert predittivi e scenario futuro
- Rileva pattern in **formazione imminente** (es. EMA in avvicinamento)
- Mostra punteggio attuale e **punteggio stimato futuro**
- Aggiunge etichetta: `⚠️ Scenario potenziale`

- ✅ Classifica avanzata
- Aggiunta colonne:
  - Coin, Score per TF, Score totale, Direzione prevalente
  - Emoji scenario dominante, Link al file `.txt`
- Interventi minimi su `classifica.csv` e interfaccia Streamlit

---

## ✅ Versione 1.3 (2025-07-20)

### 🧠 Integrazione TA-LIB

- ✅ Aggiunta la libreria **PANDAS-TA** per l'analisi tecnica avanzata
- ✅ Implementati 19 nuovi indicatori tra cui: `EMA 21`, `EMA 50`, `STOCH`, `OBV`, `MFI`, `TRIX`, `ROC`, ecc.
- ✅ Ogni indicatore TA-LIB è stato:
  - Collegato a un gruppo tematico (trend, momentum, volume, ecc.)
  - Integrato nel motore scenari tramite `interpreta_scenario(...)`
  - Associato a un punteggio massimo personalizzato
- ✅ Inclusi nel blocco `Dati Grezzi`, nei calcoli e nel riepilogo tecnico

---

### 🌟 Revisione sistema "Indicatori Forti"

- 🔁 Rimossa la funzione `estrai_indicatori_forti(...)` e il file `estrattori.py`
- ✅ Indicatori forti ora centralizzati nella funzione `blocco_indicatori_forti(...)`
- ✅ Un indicatore è "forte" solo se raggiunge il **punteggio massimo assegnato**
- ❌ Esclusi indicatori con punteggio 0
- ➕ Aggiunta la direzione (long / short / neutro) accanto al punteggio

---

### 🧹 Pulizia e semplificazione del codice

- 🔁 Eliminati loop duplicati nella GUI per gli indicatori forti
- ✅ La GUI usa ora solo `blocco_forti` generato una volta sola
- ❌ Risolta un’importazione circolare tra `calcola_scenario_finale.py` e `genera_blocchi_analisi_finale.py`

---

### 📁 Output migliorati

- 📊 Migliore leggibilità nel blocco `# === INDICATORI FORTI ===`
- ✅ Ordinati per timeframe, con scenario e direzione
- ✅ Rispecchiano esattamente i punteggi definiti

---

## ✅ Versione 1.2 (2025-07-20)
- Integrazione completa del sistema scenari di ChatGPT tramite file esterno (regole_scenari.json)
- Nuova funzione interpreta_scenario() per assegnazione dinamica dello scenario
- Aggiunto blocco scenari per timeframe accanto al blocco tecnico
- Rivisitazione completa di tutti gli indicatori:
- Ogni indicatore ora include il campo "valore" (descrittivo o numerico)
- Rimossi tutti i None, "n.d.", "?" e stringhe ambigue
- Logica coerente anche nei return di errore
- File pattern_tecnici.py, elliott.py, ichimoku.py, macd.py, adx.py e volume.py corretti e completati
- Conclusa la revisione core/, optional/, extra/

---

## 📦 Versione 1.1.1 - Fix compatibilità coin recenti

- ✅ Aggiunto filtro in `scarica_dati_grezzi(...)` per escludere i timeframe con meno di 300 righe
- ✅ Evitati errori critici su coin nuove (es. TRUMPUSDT)
- ✅ Classifica e blocchi analisi ora si generano anche con TF parziali
- ♻️ Nessuna modifica alla struttura di Cassandra 1.1 originale

---

## ✅ Versione 1.1 (2025-07-20)
- Funzione Classifica completata
- Lettura automatica da lista_coin.txt
- Aggiunta manuale coin con pulsante
- Ricalcolo punteggi per ogni coin
- Generazione e download del file classifica.csv
- Salvataggio dei file TXT in analisi_finali/
- Architettura con schermata home (dashboard) e caricamento dinamico modalità

---

## ✅ Versione 1.0 (2025-07-19)
- Analisi completa singola funzionante
- Rilevamento indicatori forti
- Frase finale strategica automatica
- Supporti e resistenze divisi e ordinati
- File TXT esportabile

### ✅ Versione 1.2 (2025-07-20)

- Integrazione completa del sistema **scenari tramite file esterno** (`regole_scenari.json`)
- Nuova funzione `interpreta_scenario()` per assegnazione dinamica dello scenario
- Aggiunto **blocco scenari per timeframe** accanto al blocco tecnico
- Rivisitazione completa di tutti gli indicatori:
  - Ogni indicatore ora include il campo `"valore"` (descrittivo o numerico)
  - Rimossi tutti i `None`, `"n.d."`, `"?"` e stringhe ambigue
  - Logica coerente anche nei `return` di errore
- File `pattern_tecnici.py`, `elliott.py`, `ichimoku.py`, `macd.py`, `adx.py` e `volume.py` corretti e completati
- Conclusa la revisione `core/`, `optional/`, `extra/`
