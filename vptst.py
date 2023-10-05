import yfinance as yf
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from matplotlib.dates import DateFormatter

st.title('Volume Price Trend (VPT) Analysis')
st.sidebar.header('User Input')
time_input = st.sidebar.selectbox("Select Time",['1D','5D','1M','3M','6M','1Y','5Y'])
avg_input = st.sidebar.selectbox("Select Days",[9,20,44,50,100,200])

# User input for stock symbols and date range
stock_symbols = st.sidebar.text_input("Enter Stock Symbols (comma-separated)", "AAPL")
time_interval_mapping = {
    '1D': timedelta(days=1),
    '5D': timedelta(days=5),
    '1M': timedelta(days=30),  # Assuming 1 month is approximately 30 days
    '3M': timedelta(days=90),
    '6M': timedelta(days=180),
    '1Y': timedelta(days=365),  # Assuming 1 year is approximately 365 days
    '5Y': timedelta(days=5 * 365),  
}

selected_time_interval = time_interval_mapping.get(time_input, timedelta(days=1))
end_date = datetime.now().date()
start_date = end_date - selected_time_interval
stock_symbols = [symbol.strip() for symbol in stock_symbols.split(',')]
stock_data = {}
def vpt():
    for symbol in stock_symbols:
        df = yf.download(symbol, start=start_date, end=end_date)
        df['VPT'] = 0  
        vpt_values = [0]  
        for i in range(1, len(df)):
            price_change = (df['Close'].iloc[i] - df['Close'].iloc[i - 1]) / df['Close'].iloc[i - 1]
            vpt = vpt_values[-1] + price_change * df['Volume'].iloc[i]
            vpt_values.append(vpt)
        df['VPT'] = vpt_values
        stock_data[symbol] = df
    st.header('Volume Price Trend (VPT) Analysis')
    for symbol in stock_symbols:
        st.subheader(f'{symbol}')
        fig, ax = plt.subplots(figsize=(12, 6))
        ax.plot(stock_data[symbol].index, stock_data[symbol]['VPT'], label=symbol)
        ax.set_title(f'Volume Price Trend (VPT) for {symbol}')
        ax.set_xlabel('Date')
        ax.set_ylabel('VPT Value')
        ax.grid(True)
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))  # Format the date ticks
        plt.xticks(rotation=45)
        ax.legend()
        st.pyplot(fig)

def moving():
    stock_data = yf.download(stock_symbols, start=start_date, end=end_date)
    moving_average_period = avg_input  # Change to your desired moving average period

    # Download historical stock data using yfinance
    stock_data = yf.download(stock_symbols, start=start_date, end=end_date)

    # Calculate Simple Moving Average (SMA)
    stock_data['SMA'] = stock_data['Close'].rolling(window=moving_average_period).mean()

    # Calculate Exponential Moving Average (EMA)
    stock_data['EMA'] = stock_data['Close'].ewm(span=moving_average_period, adjust=False).mean()


    # Create a Matplotlib figure and axis
    fig, ax = plt.subplots(figsize=(12, 6))

    # Customize date formatting
    date_format = DateFormatter("%Y-%m-%d")

    # Plotting the stock data
    ax.plot(stock_data.index, stock_data['EMA'], label=f'EMA ({time_input})', color='blue')
    ax.plot(stock_data.index, stock_data['Close'], label=f'Close ({time_input})', color='red')
    ax.plot(stock_data.index, stock_data['SMA'], label=f'SMA ({time_input})', color='black')

    # Adding labels and title
    ax.set_ylabel('Price')
    ax.set_title(f'Stock Price Over Time ({time_input})')

    # Customize date formatting for the x-axis
    ax.xaxis.set_major_formatter(date_format)

    # Adding a legend
    ax.legend()

    # Customize the x-axis label
    ax.set_xlabel('Date')

    # Display the plot using Streamlit
    st.pyplot(fig)

def calculate_rsi(data, period):
    delta = data['Close'].diff(1)
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)

    avg_gain = gain.rolling(window=period).mean()
    avg_loss = loss.rolling(window=period).mean()

    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))

    return rsi
def rsi():
    stock_data = yf.download(stock_symbols, start=start_date, end=end_date)

    # Calculate RSI for the stock data
    rsi_period = avg_input  # You can adjust this period as needed
    stock_data['RSI'] = calculate_rsi(stock_data, period=rsi_period)

    # Create a Matplotlib figure
    st.subheader(f'{stock_symbols}')
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(stock_data.index, stock_data['RSI'], label=stock_symbols)
    ax.plot(stock_data.index, stock_data['Close'], label=stock_symbols, color='black')
    ax.axhline(y=70, color='red', linestyle='--', label='Overbought (70)')
    ax.axhline(y=30, color='green', linestyle='--', label='Oversold (30)')
    ax.set_title(f'Relative Strenth Index (RSI) for {stock_symbols}')
    ax.set_xlabel('Date')
    ax.set_ylabel('VPT Value')
    ax.grid(True)
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))  # Format the date ticks
    plt.xticks(rotation=45)
    ax.legend()
    st.pyplot(fig)

def calculate_mfi(data, period=14):
    typical_price = (data['High'] + data['Low'] + data['Close']) / 3
    raw_money_flow = typical_price * data['Volume']
    
    positive_flow = (raw_money_flow.where(data['Close'] > data['Close'].shift(1), 0)).rolling(window=period).sum()
    negative_flow = (raw_money_flow.where(data['Close'] < data['Close'].shift(1), 0)).rolling(window=period).sum()
    
    money_flow_ratio = positive_flow / negative_flow
    mfi = 100 - (100 / (1 + money_flow_ratio))
    
    return mfi
def mfi():
    stock_data = yf.download(stock_symbols, start=start_date, end=end_date)
    mfi_period = 14  # You can adjust this period as needed
    stock_data['MFI'] = calculate_mfi(stock_data, period=mfi_period)
    st.subheader(f'{stock_symbols}')
    fig, ax = plt.subplots(figsize=(12, 6))
    plt.plot(stock_data.index, stock_data['MFI'], label='MFI', color='purple')
    plt.axhline(y=70, color='red', linestyle='--', label='Overbought (70)')
    plt.axhline(y=30, color='green', linestyle='--', label='Oversold (30)')
    ax.set_title(f'Money Flow Index (MFI) for {stock_symbols}')
    ax.set_xlabel('Date')
    ax.set_ylabel('MFI Value')
    ax.grid(True)
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))  # Format the date ticks
    plt.xticks(rotation=45)
    ax.legend()
    st.pyplot(fig)

vpt()
moving()
rsi()
mfi()