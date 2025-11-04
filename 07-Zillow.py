import streamlit as st
import numpy as np
import pandas as pd
# from pandas.io.json import json_normalize
import requests

st.set_page_config(page_title = 'Zillow Property Search/Analysis', layout = 'wide')
st.title('Zillow Property Search and Analysis')

with st.form(key='form'):
    city = st.text_input(label='Enter a city:')
    state = st.text_input(label='Enter a state:')
    
    submit_button = st.form_submit_button('Submit')

if submit_button:
    if city and not state or not city and state:
        st.warning('Please enter a city and a state')
    else:
        st.success('Success!')
        
@st.cache_data
def get_search_property_data():
    search_property_url = 'https://zillow56.p.rapidapi.com/search'
    search_property_query_string = {
        'location': f'{city.lower()}' + ', ' + f'{state.lower()}',
        'output': 'csv'
        #'status': 'forSale',
        #'sortSelection': 'priorityscore',
        #'listing_type': 'by_agent',
        #'doz': 'any' # DOZ = days on Zillow
    }
    headers = {
        'x-rapidapi-key': '666e934e24msh842e981f4ebcf90p1369d1jsnfa7f40147688',
        'x-rapidapi-host': 'zillow56.p.rapidapi.com'
    }
    response = requests.get(search_property_url, 
                            headers = headers, 
                            params = search_property_query_string)
    return response.json()

data = get_search_property_data()
data_load_state = st.text('Loading data...')
data_load_state.text('Done! (using st.cache_data)')

st.subheader('Raw Data')
if st.checkbox('Show raw JSON data'):
    st.write(data)

st.subheader('Dataframe')
if st.checkbox('Show data as dataframe'):
    df = pd.DataFrame(data)
    st.write(df)

st.subheader('Categorical Column Description')
if st.checkbox('Show some details on this dataset'):
    st.write(df['homeStatus'].value_counts())
    # cat_cols = df.select_dtypes(include = ['object'])
    # for col in cat_cols:
    #     st.write(df[col].value_counts())