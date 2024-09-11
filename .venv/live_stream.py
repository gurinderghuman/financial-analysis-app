import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from datetime import datetime, timedelta

class LiveStockAnalyzer:
    def __init__(self, ticker, interval='1m'):
        self.ticker = ticker
        self.interval = interval
        self.stock = yf.Ticker(ticker)
        self.data = pd.DataFrame()
        self.fig, (self.ax1, self.ax2) = plt.subplots(2, 1, figsize=(12, 12), sharex=True)
        self.initialize_plot()

    def fetch_latest_data(self):
        end = datetime.now()
        start = end - timedelta(days=1)  # Fetch last 24 hours of data
        new_data = self.stock.history(start=start, end=end, interval=self.interval)
        self.data = pd.concat([self.data, new_data]).drop_duplicates().sort_index()
        self.data = self.data.tail(390)  # Keep only last 390 minutes (6.5 hours, i.e., one trading day)
        self.calculate_indicators()

    def calculate_indicators(self):
        self.data['MA20'] = self.data['Close'].rolling(window=20).mean()
        self.data['MA50'] = self.data['Close'].rolling(window=50).mean()
        delta = self.data['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        self.data['RSI'] = 100 - (100 / (1 + rs))
        self.data['Signal'] = np.where(self.data['MA20'] > self.data['MA50'], 1, 0)
        self.data['Signal'] = np.where(self.data['MA20'] < self.data['MA50'], -1, self.data['Signal'])

    def initialize_plot(self):
        self.ax1.set_title(f"{self.ticker} Stock Price and Indicators (Live)")
        self.ax1.set_ylabel("Price (USD)")
        self.ax1.grid(True)
        
        self.ax2.set_title("Relative Strength Index (RSI)")
        self.ax2.set_ylabel("RSI")
        self.ax2.set_xlabel("Date")
        self.ax2.axhline(y=70, color='red', linestyle='--')
        self.ax2.axhline(y=30, color='green', linestyle='--')
        self.ax2.grid(True)

    def update_plot(self, frame):
        self.fetch_latest_data()
        
        self.ax1.clear()
        self.ax1.plot(self.data.index, self.data['Close'], label='Close Price')
        self.ax1.plot(self.data.index, self.data['MA20'], label='20-period MA')
        self.ax1.plot(self.data.index, self.data['MA50'], label='50-period MA')
        self.ax1.set_title(f"{self.ticker} Stock Price and Indicators (Live)")
        self.ax1.set_ylabel("Price (USD)")
        self.ax1.legend()
        self.ax1.grid(True)
        
        self.ax2.clear()
        self.ax2.plot(self.data.index, self.data['RSI'], label='RSI', color='purple')
        self.ax2.axhline(y=70, color='red', linestyle='--')
        self.ax2.axhline(y=30, color='green', linestyle='--')
        self.ax2.set_title("Relative Strength Index (RSI)")
        self.ax2.set_ylabel("RSI")
        self.ax2.set_xlabel("Date")
        self.ax2.legend()
        self.ax2.grid(True)
        
        plt.tight_layout()
        
        latest_price = self.data['Close'].iloc[-1]
        latest_rsi = self.data['RSI'].iloc[-1]
        latest_signal = self.data['Signal'].iloc[-1]
        signal_text = 'Buy' if latest_signal == 1 else 'Sell' if latest_signal == -1 else 'Hold'
        
        print(f"\rLatest - Price: ${latest_price:.2f} | RSI: {latest_rsi:.2f} | Signal: {signal_text}", end="")

def main():
    ticker = input("Enter the stock ticker symbol (e.g., AAPL): ").upper()
    analyzer = LiveStockAnalyzer(ticker)
    ani = FuncAnimation(analyzer.fig, analyzer.update_plot, interval=60000)  # Update every 60 seconds
    plt.show()

if __name__ == "__main__":
    main()