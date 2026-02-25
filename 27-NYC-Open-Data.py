import streamlit as st
import pandas as pd
import requests

st.set_page_config('NYC Open Data', layout='wide')
st.title('NYC Open Data')

datasets = {
    'DOB Job Application Filings': 'ic3t-wcy2',
    'Civil Service List (Active)': 'vx8i-nprf'
}
dataset_info = {
    'DOB Job Application Filings': 'Contains all DOB job applications filed in NYC.',
    'Civil Service List (Active)': 'Active civil service employees in NYC.'
}
selected_dataset = st.selectbox('Choose a dataset to explore', list(datasets.keys()))
page_num = st.slider('Page number', 1, 10)
page_size = st.slider('Page size', 1, 100)
api_token = st.secrets['NYC_OPEN_DATA_API_TOKEN']

@st.cache_data
def get_data(dataset_name, num, size, token):
    dataset_id = datasets[dataset_name]
    url = f'https://data.cityofnewyork.us/api/v3/views/{dataset_id}/query.json?pageNumber={num}&pageSize={size}&app_token={token}'
    # url = f'https://data.cityofnewyork.us/api/v3/views/ic3t-wcy2/query.json?pageNumber={num}&pageSize={size}&app_token={token}'
    response = requests.get(url)
    if response.status_code != 200:
        st.error(f'Error fetching data: {response.status_code}')
        st.stop()
    else:
        data = response.json()
        return pd.DataFrame(data)

with st.spinner('Fetching data...'):
    df = get_data(selected_dataset, page_num, page_size, api_token)
st.dataframe(df, use_container_width=True)
st.markdown(dataset_info[selected_dataset])

#url = 'https://raw.githubusercontent.com/vinit714/Tableau-Dashboards/refs/heads/main/Analyzing%20Amazon%20Sales%20data/Amazon%20Sales%20data.csv'
#df = pd.read_csv(url)
#st.dataframe(df)