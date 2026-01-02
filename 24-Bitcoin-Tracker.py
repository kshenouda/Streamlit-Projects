import streamlit as st
import pandas as pd
import requests

st.set_page_config(page_title='Bitcoin Tracker', layout='wide')
st.title('Bitcoin Price Tracker - CoinGecko')

price_url = 'https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd'

try:
    price_response = requests.get(price_url, timeout=10)
    price_response.raise_for_status()
    price = price_response.json()['bitcoin']['usd']
    st.metric(label='Bitcoin Price USD', value=f'${price:,}')
except requests.exceptions.RequestException as e:
    st.error(f'Failed to fetch current price {e}')


history_url = 'https://api.coingecko.com/api/v3/coins/bitcoin/market_chart'
params = {
    'vs_currency': 'usd',
    'days': '30',
    'interval': 'daily'
}

try:
    history_response = requests.get(history_url, params=params, timeout=10)
    history_response.raise_for_status()
    prices = history_response.json()['prices']

    df = pd.DataFrame(prices, columns=['Timestamp', 'Price'])
    df['Date'] = pd.to_datetime(df['Timestamp'], unit='ms')
    st.line_chart(df.set_index('Date')['Price'])
except requests.exceptions.RequestException as e:
    st.error(f'Failed to fetch historical data price {e}')