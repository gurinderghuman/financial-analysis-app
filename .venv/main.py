import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def fetch_stock_data(ticker, start_date, end_date):
    stock = yf.Ticker(ticker)
    data = stock.history(start=start_date, end=end_date)
    return data

def calculate_indicators(data):
    # Calculate 20-day and 50-day moving averages
    data['MA20'] = data['Close'].rolling(window=20).mean()
    data['MA50'] = data['Close'].rolling(window=50).mean()
    
    # Calculate RSI
    delta = data['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    data['RSI'] = 100 - (100 / (1 + rs))
    
    return data

def generate_signals(data):
    data['Signal'] = np.where(data['MA20'] > data['MA50'], 1, 0)
    data['Signal'] = np.where(data['MA20'] < data['MA50'], -1, data['Signal'])
    return data

def plot_stock_data(data, ticker):
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 12), sharex=True)
    
    # Plot stock price and moving averages
    ax1.plot(data.index, data['Close'], label='Close Price')
    ax1.plot(data.index, data['MA20'], label='20-day MA')
    ax1.plot(data.index, data['MA50'], label='50-day MA')
    ax1.set_title(f"{ticker} Stock Price and Indicators")
    ax1.set_ylabel("Price (USD)")
    ax1.legend()
    ax1.grid(True)
    
    # Plot RSI
    ax2.plot(data.index, data['RSI'], label='RSI', color='purple')
    ax2.axhline(y=70, color='red', linestyle='--')
    ax2.axhline(y=30, color='green', linestyle='--')
    ax2.set_title("Relative Strength Index (RSI)")
    ax2.set_ylabel("RSI")
    ax2.set_xlabel("Date")
    ax2.legend()
    ax2.grid(True)
    
    plt.tight_layout()
    plt.show()

def analyze_stock(ticker, start_date, end_date):
    stock_data = fetch_stock_data(ticker, start_date, end_date)
    stock_data = calculate_indicators(stock_data)
    stock_data = generate_signals(stock_data)
    
    plot_stock_data(stock_data, ticker)
    
    print(f"Analysis for {ticker}:")
    print(f"Latest closing price: ${stock_data['Close'][-1]:.2f}")
    print(f"Latest RSI: {stock_data['RSI'][-1]:.2f}")
    print(f"Latest Signal: {'Buy' if stock_data['Signal'][-1] == 1 else 'Sell' if stock_data['Signal'][-1] == -1 else 'Hold'}")

if __name__ == "__main__":
    tickers = ["AAPL", "MSFT", "GOOGL"]  # Example tickers
    start_date = "2023-01-01"
    end_date = "2023-12-31"
    
    for ticker in tickers:
        analyze_stock(ticker, start_date, end_date)