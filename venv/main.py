import yfinance as yf
import matplotlib.pyplot as plt

def fetch_stock_data(ticker, start_date, end_date):
    stock = yf.Ticker(ticker)
    data = stock.history(start=start_date, end=end_date)
    return data

def plot_stock_data(data, ticker):
    plt.figure(figsize=(12, 6))
    plt.plot(data.index, data['Close'])
    plt.title(f"{ticker} Stock Price")
    plt.xlabel("Date")
    plt.ylabel("Price (USD)")
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    ticker = "AAPL"  # Apple Inc. as an example
    start_date = "2023-01-01"
    end_date = "2023-12-31"
    
    stock_data = fetch_stock_data(ticker, start_date, end_date)
    plot_stock_data(stock_data, ticker)