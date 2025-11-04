import streamlit as st
import numpy as np
import pandas as pd
import requests

st.set_page_config(page_title = 'Petfinder', layout = 'wide')
st.title('Petfinder')

# API Credentials
api_key = 'u0QvzCX0moABmnIv4UhDj1qumxsRvTIPixqShClcac32MivY6v'
api_secret = 'kHo5M0KfyhfOwJtLrDF50ZjZXgc25STXWbYz2rOt'

@st.cache_data(ttl = 3600)
def get_access_token():
    token_url = 'https://api.petfinder.com/v2/oauth2/token'
    data = {
        'grant_type': 'client_credentials',
        'client_id': api_key,
        'client_secret': api_secret
    }
    response = requests.post(token_url, data = data)
    if response.status_code == 200:
        token = response.json()['access_token']
        return token
    else:
        st.error(f'Failed to get token: {response.status_code}')
        st.write(response.text)
        return None

token = get_access_token()

with st.form(key = 'endpoint_form'):
    endpoint_options = ['Animals', 'Animal Types', 'Organizations']
    endpoint = st.selectbox('Select an endpoint to retrieve data from',
                            options = endpoint_options)
    endpoint_submit = st.form_submit_button('Submit')

animals_query_params = {
    'size': 'small',
    'age': 'baby'
}

organization_query_params = {
    'location': 'Bayonne, NJ',
    'distance': 100,
    'state': 'NJ',
    'country': 'US'
}

animals_url = 'https://api.petfinder.com/v2/animals'
types_url = 'https://api.petfinder.com/v2/types'
organizations_url = 'https://api.petfinder.com/v2/organizations'

if token and endpoint_submit:
    headers = {'Authorization': f'Bearer {token}'}
    if endpoint_submit and endpoint == 'Animals':
        animals_response = requests.get(animals_url, 
                                        headers=headers,
                                        params=animals_query_params)
        animals_df = pd.DataFrame(animals_response.json()['animals'])
        st.write(animals_df)
        #st.write(animals_response.json()['animals'])
        st.write(f'Current query used the following parameters: {animals_query_params}')

    if endpoint_submit and endpoint == 'Animal Types':
        types_response = requests.get(types_url,
                                      headers=headers)
        types_df = pd.DataFrame(types_response.json()['types'])
        st.write(types_df)
        #st.write(types_response.json())

    if endpoint_submit and endpoint == 'Organizations':
        organizations_response = requests.get(organizations_url, 
                                              headers=headers,
                                              params=organization_query_params)
        orgs_df = pd.DataFrame(organizations_response.json()['organizations'])
        st.write(orgs_df)
        #st.write(organizations_response.json())
        st.write(f'Current query used the following parameters: {organization_query_params}')
