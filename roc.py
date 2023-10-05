import yfinance as yf
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from matplotlib.dates import DateFormatter

# Define the stock symbol and time period
st.sidebar.header('User Input')
time_input = st.sidebar.selectbox("Select Time",['1D','5D','1M','3M','6M','1Y','5Y'])
avg_input = st.sidebar.selectbox("Select Days",[9,20,44,50,100,200])

# User input for stock symbols and date range
stock_symbol = st.sidebar.text_input("Enter Stock Symbols (comma-separated)", "AAPL")
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
# Download historical stock data using yfinance
stock_data = yf.download(stock_symbol, start=start_date, end=end_date)

# Calculate ROC
def calculate_roc(data, period=1):
    data['ROC'] = ((data['Close'] - data['Close'].shift(period)) / data['Close'].shift(period)) * 100
    return data['ROC']

# Calculate ROC for the stock data
roc_period = 1  # You can adjust this period as needed
stock_data['ROC'] = calculate_roc(stock_data, period=roc_period)

st.subheader(f'{stock_symbol}')
fig, ax = plt.subplots(figsize=(12, 6))
ax.plot(stock_data.index, stock_data['ROC'], label=stock_symbol)
ax.set_title(f'Volume Price Trend (VPT) for {stock_symbol}')
ax.set_xlabel('Date')
ax.set_ylabel('VPT Value')
ax.grid(True)
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))  # Format the date ticks
plt.xticks(rotation=45)
ax.legend()
st.pyplot(fig)