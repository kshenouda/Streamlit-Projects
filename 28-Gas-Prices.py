import streamlit as st
import pandas as pd
import plotly.express as px
from sklearn.linear_model import LinearRegression

st.set_page_config(page_title='Gas Price Analysis', layout='wide')
st.title('Gas Price Analysis')
st.markdown('''
This application will analyze and predict oil and gas prices in the U.S. \n
The dataset used comes from this [Github page](https://github.com/swoyam2609/Oil-and-Gas-Price-Analysis-and-Prediction/tree/main)
''')
st.divider()

pages = [
    'Home/Raw Data',
    'Summary Statistics',
    'Visualizations',
    'Forecasting'
]
st.sidebar.subheader('Page Navigation')
selected_page = st.sidebar.radio('Select a page', pages)
st.sidebar.divider()

@st.cache_data
def load_data():
    url = 'https://raw.githubusercontent.com/swoyam2609/Oil-and-Gas-Price-Analysis-and-Prediction/refs/heads/main/Datasets/oil%20and%20gas.csv'
    df = pd.read_csv(url)
    return df

df = load_data()
df['Date'] = pd.to_datetime(df['Date'])
# df = df.sort_values('Date')
first_date = min(df['Date'])
last_date = max(df['Date'])

st.sidebar.subheader('Global Filters')
selected_symbols = st.sidebar.multiselect(
    'Select Symbols',
    options=sorted(df['Symbol'].unique()),
    default=sorted(df['Symbol'].unique())
)
date_range = st.sidebar.date_input(
    'Select Date Range',
    [df['Date'].min(), df['Date'].max()]
)

filtered_df = df[
    (df['Symbol'].isin(selected_symbols)) &
    (df['Date'].between(pd.to_datetime(date_range[0]), pd.to_datetime(date_range[1])))
]
filtered_df = filtered_df.copy()

filtered_df['Daily Return'] = (
    filtered_df.groupby('Symbol')['Close'].pct_change()
)

window = st.sidebar.slider('Moving Average Window', 5, 60, 20)
filtered_df['Rolling Mean'] = (
    filtered_df.groupby('Symbol')['Close']
    .transform(lambda x: x.rolling(window).mean())
)

most_volatile = (
    filtered_df.groupby('Symbol')['Daily Return'].std().idxmax()
)

if selected_page == 'Home/Raw Data':
    st.subheader('Raw Data')
    with st.spinner('Loading data...'):
        st.dataframe(filtered_df)

if selected_page == 'Summary Statistics':
    col1, col2 = st.columns(2)
    with col1:
        selected_symbol = st.selectbox('Select a symbol', sorted(filtered_df['Symbol'].unique()))
    with col2:
        selected_metric = st.selectbox('Select a metric', ['Open', 'Close', 'High', 'Low', 'Volume'])
    col1, col2, col3, col4 = st.columns(4)
    col1.metric(f'Minimum {selected_metric}', filtered_df[filtered_df['Symbol'] == selected_symbol][selected_metric].min())
    col2.metric(f'Maximum {selected_metric}', filtered_df[filtered_df['Symbol'] == selected_symbol][selected_metric].max())
    col3.metric(f'Average {selected_metric}', round(filtered_df[filtered_df['Symbol'] == selected_symbol][selected_metric].mean(),2))
    col4.metric(f'Standard Deviation {selected_metric}', round(filtered_df[filtered_df['Symbol'] == selected_symbol][selected_metric].std(),2))

if selected_page == 'Visualizations':
    st.subheader('Visualizations')
    tab1, tab2 = st.tabs(['Line Chart', 'Correlation Matrix'])
    with tab1:
        metric = st.selectbox('Metric', ['Open', 'Close', 'High', 'Low', 'Volume', 'Rolling Mean'])
        fig = px.line(filtered_df, x='Date', y=metric, color='Symbol', title=f'{metric} Over Time')
        vline_date = '2020-03-16'
        fig.add_vline(
            x=vline_date,
            line_width=1,
            line_dash='solid',
            line_color='lightgreen',
        )
        #fig.add_annotation(x=vline_date, 
        #                   text='Covid-19',
        #)
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('''
        It looks like brent oil and crude oil WTI are highly related to each
        other, and are much more volatile in their open prices. \n
        Conversely, natural gas and heating oil are also highly related to each other,
        but much cheaper than the other two resources.
        ''')
        st.info(f'{most_volatile} appears to be the most volatile commodity')
    with tab2:
        pivot_df = filtered_df.pivot(index='Date', columns='Symbol', values='Close')
        corr = pivot_df.corr()
        fig = px.imshow(corr, text_auto=True, title='Correlation Matrix',
                        color_continuous_scale='balance') # balance, bluered
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('''
        Just like the line chart, we can see a close relationship between: \n
        * Brent oil and Heating oil (0.98) \n
        * Brent oil and Crude oil WTI (0.97) \n
        * Crude oil WTI and Heating oil (0.96) \n
        ''')

if selected_page == 'Forecasting':
    st.subheader('Linear Regression Forecasting')
    col1, col2 = st.columns(2)
    with col1:
        forecast_symbol = st.selectbox('Select Symbol for Forecast',
                                        sorted(filtered_df['Symbol'].unique()))
    with col2:
        forecast_days = st.slider('Forecast Horizon (Days)',
                                  7, 180, 30)
    symbol_df = filtered_df[filtered_df['Symbol'] == forecast_symbol].copy()
    symbol_df = symbol_df.sort_values('Date')
    symbol_df['Date_Ordinal'] = symbol_df['Date'].map(pd.Timestamp.toordinal)

    X = symbol_df[['Date_Ordinal']]
    y = symbol_df['Close']

    model = LinearRegression()
    model.fit(X, y)

    r2 = model.score(X, y)

    last_date = symbol_df['Date'].max()
    future_dates = pd.date_range(last_date, periods=forecast_days+1, freq='D')[1:]
    future_df = pd.DataFrame({
        'Date': future_dates
    })
    future_df['Date_Ordinal'] = future_df['Date'].map(pd.Timestamp.toordinal)
    future_df['Predicted Close'] = model.predict(future_df[['Date_Ordinal']])
    fig = px.line(symbol_df, x='Date', y='Close', title=f'{forecast_symbol} Forecast')
    fig.add_scatter(
        x=future_df['Date'],
        y=future_df['Predicted Close'],
        mode='lines',
        name='Forecast'
    )
    st.plotly_chart(fig, use_container_width=True)

    col1, col2 = st.columns(2)
    col1.metric('Model R² Score', round(r2, 4))
    col2.metric('Trend Coefficient (Slope)', round(model.coef_[0], 4))
    st.info('Linear regression assumes a linear trend and does not account for seasonality or volatility.')

st.divider()
st.caption('Gas Price Analysis Application v1.0, created by Kiro Shenouda')