from flask import Flask, Response
import ccxt
import csv
import io

app = Flask(__name__)
exchange = ccxt.binance()

@app.route("/ohlcv/<symbol>/<tf>")
def get_ohlcv(symbol, tf):
    try:
        symbol = symbol.upper().replace("-", "/")  # ETHUSDT → ETH/USDT
        data = exchange.fetch_ohlcv(symbol, timeframe=tf, limit=500)
        
        # Prepara output CSV in memoria
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(["timestamp", "open", "high", "low", "close", "volume"])
        writer.writerows(data)
        output.seek(0)
        
        return Response(output, mimetype="text/csv")
    
    except Exception as e:
        return f"Errore: {e}", 500
