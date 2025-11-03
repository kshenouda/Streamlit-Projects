# https://www.alphavantage.co/documentation/
import streamlit as st
import pandas as pd
import requests

# Streamlit page setup
st.set_page_config(page_title = 'Economic Indicator App', initial_sidebar_state = 'auto') # initial_sidebar_state = 'expanded'
st.title('Economic Indicators App')
st.markdown('##### This application will allow users to choose an economic metric like inflation and GDP. Users will see a table of the data, a line chart of the data over time, and two sections showing the data summary statistics and timeframe.')

# Config
API_KEY = '17WR8QUHVSBFK5RA'
# API_KEY = st.secrets['17WR8QUHVSBFK5RA'] # safe and cleaner
# add API key to .streamlit/secrets.toml
BASE_URL = 'https://www.alphavantage.co/query'

# Define economic metrics
metric = {
    'CPI': 'CPI', # Consumer Price Index: average change over time in prices paid by urban consumers for a basket of consumer goods/services
    'Durables' : 'DURABLES', # goods/products that lasts in the long-term (several years)
    'Federal Funds Rate': 'FEDERAL_FUNDS_RATE',
    'Inflation': 'INFLATION', 
    'Real GDP': 'REAL_GDP',
    'Real GDP Per Capita': 'REAL_GDP_PER_CAPITA',
    'Retail Sales': 'RETAIL_SALES',
    'Treasury Yield': 'TREASURY_YIELD',
    'Unemployment': 'UNEMPLOYMENT'
}

# with st.sidebar:
selected_metric = st.selectbox('Select a metric you want to visualize', list(metric.keys()))

interval = {
    'CPI': 'monthly', 
    'Durables' : 'monthly', 
    'Federal Funds Rate': 'monthly',
    'Inflation': 'monthly', 
    'Real GDP': 'daily',
    'Real GDP Per Capita': 'annual',
    'Retail Sales': 'annual',
    'Treasury Yield': 'annual',
    'Unemployment': 'monthly'
}

# selected_interval = st.selectbox('Select a time interval for the data', )

# Cached request
@st.cache_data(ttl=3600, show_spinner='Fetching data...')
def econ_indicator(metric: str) -> pd.DataFrame:
    """Fetch and cache Alpha Vantage economic indicator data"""
    url = f'{BASE_URL}?function={metric}&interval=annual&datatype=json&apikey={API_KEY}'
    r = requests.get(url)
    r.raise_for_status()
    data = r.json()

    # data = r.json()
    # df = pd.DataFrame(data['data'])
    # df2 = df

    # Extract and clean data
    df = pd.DataFrame(data['data'])
    df['value'] = df['value'].astype(float)
    df['date'] = pd.to_datetime(df['date']).dt.date
    return df.sort_values('date', ascending=False)

# Main logic
try: 
    df = econ_indicator(metric[selected_metric])

    st.subheader(f'{selected_metric} Data')
    st.dataframe(df, use_container_width = True)

    st.subheader(f'{selected_metric} Trend')
    st.line_chart(df.set_index('date')['value'])

    # Create two columns of equal width
    col1, col2 = st.columns(2)

    # Summarys statistics
    with(col1):
        st.subheader(f'{selected_metric} Summary Stats')
        st.metric('Average: ', (round(df['value'].mean(), 2)))
        st.metric('Maximum: ', (round(df['value'].max(), 2)))
        st.metric('Minimum: ', (round(df['value'].min(), 2)))
        st.metric('Range: ', (round(df['value'].max() - df['value'].min(), 2)))

    # Data's date range
    with(col2):
        st.subheader(f'{selected_metric} Date Range')
        st.metric('Earliest date', str(df['date'].min().strftime("%B %Y")))
        st.metric('Latest date', str(df['date'].max().strftime("%B %Y")))    

    # Download button
    st.download_button(
        label = 'Download Data as CSV',
        data = df.to_csv(index = False),
        file_name = f'{selected_metric}.csv',
        # type = 'primary',
        mime = 'text/csv',
)

except Exception as e:
    st.error(f'Failed to load data: {e}')