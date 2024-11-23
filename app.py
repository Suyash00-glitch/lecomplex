from flask import Flask, render_template
import yfinance as yf

app = Flask(__name__)

def fetch_stock_data(stock_symbols):
    stock_data = []
    for symbol in stock_symbols:
        try:
            stock = yf.Ticker(symbol)
            info = stock.info
            cmp = info.get('currentPrice', 'N/A')
            previous_close = info.get('previousClose', 'N/A')
            market_cap = info.get('marketCap', 'N/A')
            volume = info.get('volume', 'N/A')
            if cmp != 'N/A' and previous_close != 'N/A':
                day_change = ((cmp - previous_close) / previous_close) * 100
            else:
                day_change = 'N/A'
            stock_data.append({
                'Symbol': symbol,
                'CMP': cmp,
                'Day Change (%)': round(day_change, 2) if day_change != 'N/A' else 'N/A',
                'Market Cap': market_cap,
                'Volume': volume
            })
        except Exception as e:
            print(f"Error fetching data for {symbol}: {e}")
    return stock_data

@app.route('/')
def index():
    # List of stock symbols
    stock_symbols = [
        "RELIANCE.NS", "TCS.NS", "INFY.NS", "HDFCBANK.NS", 
        "ICICIBANK.NS", "BAJFINANCE.NS", "KOTAKBANK.NS", "SBIN.NS", "BHARTIARTL.NS",
        "ITC.NS", "LT.NS", "M&M.NS", "ULTRACEMCO.NS", "ASIANPAINT.NS",
        "MARUTI.NS", "BAJAJ-AUTO.NS", "HCLTECH.NS", "NTPC.NS", "WIPRO.NS",
        "SUNPHARMA.NS", "HINDUNILVR.NS", "TITAN.NS", "POWERGRID.NS", "DRREDDY.NS",
        "CIPLA.NS", "JSWSTEEL.NS", "HINDALCO.NS", "TECHM.NS", "NESTLEIND.NS"
    ]

    # Fetch stock data
    stock_data = fetch_stock_data(stock_symbols)

    # Sort by Day Change and pick top 10
    stock_data = sorted(stock_data, key=lambda x: x['Day Change (%)'] if x['Day Change (%)'] != 'N/A' else float('-inf'), reverse=True)[:10]

    # Render the data in the HTML page
    return render_template('stock_data.html', stock_data=stock_data)

if __name__ == '__main__':
    app.run(debug=True)
