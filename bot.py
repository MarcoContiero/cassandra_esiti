from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from elaborazione.genera_blocchi_bot import genera_analisi_bot
from analisi.analizza_coin_light import scarica_dati_grezzi
from datetime import datetime

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🤖 Ciao! Mandami il comando /analizza ETHUSDT per iniziare.")

async def analizza(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        coin = context.args[0].upper()

        # 📥 Scarica dati grezzi direttamente
        tf_usati = ["15m", "1h", "4h", "1d", "1w"]
        grezzi_raw = scarica_dati_grezzi(coin, tf_usati)

        if not grezzi_raw:
            await update.message.reply_text(f"❌ Nessun dato trovato per {coin}.")
            return

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # ✅ Costruzione compatibile con Cassandra
        grezzi = {
            "dati": grezzi_raw,
            "_timestamp_download": timestamp,
            "timeframes": tf_usati
        }

        # 📊 Ricostruzione lista completa
        dati = []
        for tf, lista in grezzi["dati"].items():
            for riga in lista:
                riga["timeframe"] = tf
                dati.append(riga)

        # 🧠 Analisi Cassandra
        testo = genera_analisi_bot(coin, dati, data_analisi=timestamp, data_dati=timestamp)

        if testo:
            await update.message.reply_text(f"📈 Analisi {coin}:\n\n{testo[:4000]}")
        else:
            await update.message.reply_text("❌ Errore: analisi non generata.")

    except Exception as e:
        await update.message.reply_text(f"❌ Errore durante l'analisi: {e}")

if __name__ == "__main__":
    TOKEN = "7179795606:AAF8hOrNrMeVxwuzphAwb9VSIw8dmbq5fSc"
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("analizza", analizza))
    print("🚀 Bot avviato...")
    app.run_polling()
