import yfinance as yf
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# Define the stock symbols and date range
stock_symbols = ['AAPL', 'MSFT', 'GOOGL']  # List of stock symbols
start_date = '2023-01-01'
end_date = '2023-01-05'

# Create a dictionary to store dataframes for each stock
stock_data = {}

# Fetch historical stock data for each symbol
for symbol in stock_symbols:
    df = yf.download(symbol, start=start_date, end=end_date)
    df['VPT'] = 0  # Initialize a VPT column
    vpt_values = [0]  # Initialize VPT values
    for i in range(1, len(df)):
        price_change = (df['Close'].iloc[i] - df['Close'].iloc[i - 1]) / df['Close'].iloc[i - 1]
        vpt = vpt_values[-1] + price_change * df['Volume'].iloc[i]
        vpt_values.append(vpt)
    df['VPT'] = vpt_values
    stock_data[symbol] = df

# Plot the VPT for each stock
plt.figure(figsize=(12, 6))
for symbol in stock_symbols:
    plt.plot(stock_data[symbol].index, stock_data[symbol]['VPT'], label=symbol)

plt.title('Volume Price Trend (VPT)')
plt.xlabel('Date')
plt.ylabel('VPT Value')
plt.grid(True)
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))  # Format the date ticks
plt.xticks(rotation=45)
plt.legend()
plt.tight_layout()

plt.show()
