import streamlit as st
import pandas as pd
import requests

# Streamlit page setup
st.set_page_config(page_title = 'Economic Indicator App', initial_sidebar_state = 'auto', layout='wide')
st.title('Economic Indicators App')
st.markdown('''
This application will allow users to choose an economic metric 
like inflation and GDP. Users will see a table of the data, a line 
chart of the data over time, and two sections showing the data 
summary statistics and timeframe.

Source: [Alpha Vantage API Documentation](https://www.alphavantage.co/documentation/#)

Choose an economic indicator from the sidebar to view its data.
''')
st.divider()

# Sidebar pages
pages = [
    'Data Table',
    'Graphs',
    'Summary Stats'
]
st.sidebar.subheader('Page Navigation')
selected_page = st.sidebar.radio('Go to', pages)
st.sidebar.divider()
st.sidebar.subheader('Metric Configuration')

# Config
API_KEY = st.secrets['ALPHA_VANTAGE_API_KEY'] # safe and cleaner
BASE_URL = 'https://www.alphavantage.co/query'

# Define economic metrics
metric = {
    'CPI': 'CPI', # Consumer Price Index: average change over time in prices paid by urban consumers for a basket of consumer goods/services, Could not convert string to float error
    'Durables' : 'DURABLES', # goods/products that lasts in the long-term (several years)
    'Federal Funds Rate': 'FEDERAL_FUNDS_RATE',
    'Inflation': 'INFLATION', 
    'Real GDP': 'REAL_GDP',
    'Real GDP Per Capita': 'REAL_GDP_PER_CAPITA',
    'Retail Sales': 'RETAIL_SALES',
    'Treasury Yield': 'TREASURY_YIELD',
    'Unemployment': 'UNEMPLOYMENT' # Could not convert string to float error
}

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

selected_metric = st.sidebar.selectbox('Select a metric', list(metric.keys()))
selected_interval = interval[selected_metric]

# Cached request
@st.cache_data(ttl=3600, show_spinner='Fetching data...')
def econ_indicator(metric: str, interval: str) -> pd.DataFrame:
    """Fetch and cache Alpha Vantage economic indicator data"""
    url = f'{BASE_URL}?function={metric}&interval={interval}&datatype=json&apikey={API_KEY}'
    r = requests.get(url)
    r.raise_for_status()
    data = r.json()

    if 'data' not in data:
        raise ValueError(data.get('Note', 'API Error'))

    # Extract and clean data
    df = pd.DataFrame(data['data'])
    df['value'] = pd.to_numeric(df['value'], errors='coerce') # df['value'].astype(float)
    df['date'] = pd.to_datetime(df['date']).dt.date
    return df.sort_values('date', ascending=False)

# Main logic
try: 
    df = econ_indicator(metric[selected_metric], interval[selected_metric])
    if df.empty:
        st.warning('No data is available for this indicator.')
        st.stop
    start_date, end_date = st.sidebar.slider('Select a date range',
                                 min_value = df['date'].min(),
                                 max_value = df['date'].max(),
                                 value = (df['date'].min(), df['date'].max()))
    df = df[(df['date'] >= start_date) & (df['date'] <= end_date)]
    if selected_page == 'Data Table':
        st.subheader(f'{selected_metric} Data')
        st.dataframe(df, use_container_width = True)
        # Download button
        st.download_button(
            label = 'Download Data as CSV',
            data = df.to_csv(index = False),
            file_name = f'{selected_metric}.csv',
            # type = 'primary',
            mime = 'text/csv',
        )

    if selected_page == 'Graphs':
        st.subheader(f'{selected_metric} Trend')
        st.line_chart(df.set_index('date')['value'])

    if selected_page == 'Summary Stats':
        average = round(df['value'].mean(), 2)
        minimum = round(df['value'].min(), 2)
        maximum = round(df['value'].max(), 2)
        most_recent = df['value'][0]

        st.subheader(f'{selected_metric} Summary Stats')
        col1, col2, col3, col4 = st.columns(4)
        if selected_metric == 'Inflation' or selected_metric == 'Federal Funds Rate' or selected_metric == 'Unemployment':
            col1.metric('Minimum ', f'{minimum:,.2f}%')
            col2.metric('Maximum ', f'{maximum:,.2f}%')
            col3.metric('Average ', f'{average:,.2f}%')
            col4.metric('Most recent', f'{most_recent:,.2f}%')
        else:
            col1.metric('Minimum ', f'${minimum:,.2f}')
            col2.metric('Maximum ', f'${maximum:,.2f}')
            col3.metric('Average ', f'${average:,.2f}')
            col4.metric('Most recent', f'${most_recent:,.2f}')

        # Data's date range
        st.divider()
        st.subheader(f'{selected_metric} Date Range')
        col1, col2 = st.columns(2)
        col1.metric('Earliest date', str(df['date'].min().strftime("%B %Y")))
        col2.metric('Latest date', str(df['date'].max().strftime("%B %Y")))    

except Exception as e:
    st.error(f'Failed to load data: {e}')

st.divider()
st.caption('Economic Indicator Application v2.0 | Created by Kiro Shenouda')