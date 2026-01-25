# Load libraries
from datetime import datetime
from vega_datasets import data
import streamlit as st
import altair as alt
import pandas as pd

# Set Streamlit page config
st.set_page_config(page_title = 'Vega Datasets', layout = 'wide')
# st.title('Seattle Weather')
# st.write("Let's explore the classic Seattle Weather dataset!")
'''
# Vega Datasets
Let's explore tables in the [Vega Datasets](https://vega.github.io/vega-datasets/) package
'''

''
''

# Load dataset
datasets_list = data.list_datasets()

datasets = {
    "airports": data.airports(),
    "barley": data.barley(),
    "budget": data.budget(),
    "cars": data.cars(),
    "climate": data.climate(),
    "co2_concentration": data.co2_concentration(),
    "disasters": data.disasters(),
    "driving": data.driving(),
    #"earthquakes": data.earthquakes(),
    "flights_10k": data.flights_10k(),
    "flights_2k": data.flights_2k(),
    "gapminder": data.gapminder(),
    #"germany": data.germany(),
    "income": data.income(),
    "iowa_electricity": data.iowa_electricity(),
    "iris": data.iris(),
    "jobs": data.jobs(),
    "lookup_groups": data.lookup_groups(),
    "lookup_people": data.lookup_people(),
    "miserables": data.miserables(),
    "monarchs": data.monarchs(),
    "movies": data.movies(),
    "normal_2d": data.normal_2d(),
    "population": data.population(),
    "seattle_temps": data.seattle_temps(),
    "seattle_weather": data.seattle_weather(),
    "sf_temps": data.sf_temps(),
    "sp500": data.sp500(),
    "stocks": data.stocks(),
    #"us_10m": data.us_10m(),  # TopoJSON data
    "us_employment": data.us_employment(),
    "us_state_capitals": data.us_state_capitals(),
    #"us_states": data.us_states(), no dataset named 'us_states'
    "weather": data.weather(),
    "wheat": data.wheat(),
    #"world_110m": data.world_110m()  # TopoJSON data
}

# Print Vega datasets in a selectbox
selected_dataset = st.selectbox('Select a dataset you would like to explore', list(datasets.keys()))

''
'' 

'''
## Raw Data
'''
df = pd.DataFrame(datasets[selected_dataset]) 
# df2 = st.dataframe(datasets[selected_dataset])
st.dataframe(df)
# st.caption(f'Returned rows: {len(df)}')

'''
## Summary Statistics
'''
with st.container(horizontal = True, gap = 'medium'):
    cols = st.columns(2, gap = 'medium', width = 900)
    with cols[0]:
        st.metric(
            'Row Count',
            len(df),
            width = 'content'
        )
    with cols[1]:
        st.metric(
            'Column Count',
            len(df.columns),
            width = 'content'
        )
    cols = st.columns(3, gap = 'medium', width = 900)
    with cols[0]:
        st.metric(
            'Numerical Column Count',
            len(df.select_dtypes(include=["number"]).columns),
            width = 'content'
        )
    with cols[1]:
        st.metric(
            'Categorical Column Count',
            len(df.select_dtypes(include=["object"]).columns),
            width = 'content'
        )
    with cols[2]:
        st.metric(
            'Datetime Column Count',
            len(df.select_dtypes(include=['datetime']).columns),
            width = 'content'
        )

'''
## Descriptive Statistics
'''
st.dataframe(df.describe().transpose())

# Categorical column sumamries
cat_cols = df.select_dtypes(include = ['object']).columns
if len(cat_cols) > 0:
    st.write('## Categorical Features Summary')
    for col in cat_cols:
        st.write(f'**{col}**')
        st.write(df[col].value_counts().head(10))

'''
## Visual Insights
'''
num_cols = df.select_dtypes(include = ['number', 'float']).columns
if len(num_cols) > 0:
    selected_num_col = st.selectbox('Select a numeric column to visualize', num_cols)
    num_hist_chart = (
        alt.Chart(df).mark_bar().encode(
            alt.X(selected_num_col, bin = alt.Bin(maxbins = 30)),
            y = 'count()',
            tooltip = [selected_num_col, 'count()']
        ).properties(height = 300)
    )
    st.altair_chart(num_hist_chart, use_container_width=True)
else:
    st.info('No numeric columns available for this histogram')

# cat_cols = df.select_dtypes(include = ['object']).columns
if len(cat_cols) > 0:
    selected_cat_col = st.selectbox('Select a categorical column to visualize', cat_cols)
    cat_hist_chart = (
        alt.Chart(df).mark_bar().encode(
            alt.X(selected_cat_col, sort = '-y'), #bin = alt.Bin(maxbins = 30)),
            y = 'count()',
            tooltip = [selected_cat_col, 'count()']
        ).properties(height = 300)
    )
    st.altair_chart(cat_hist_chart, use_container_width = True)
else:
    st.info('No categorical columns available for this histogram')