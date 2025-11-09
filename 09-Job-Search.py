# API documentation: https://rapidapi.com/letscrape-6bRBa3QguO5/api/jsearch/playground/endpoint_73845d59-2a15-4a88-92c5-e9b1bc90956d
import streamlit as st
import numpy as np
import pandas as pd
import requests

st.set_page_config(page_title = 'Job Search App', layout = 'wide')
st.title('Job Search App')
st.write('Enter an endpoint to send a request to and retrieve data from the Job Search Rapid API')

endpoint_options = ['details', 'estimated-salary', 'search']
endpoint_selected = st.selectbox('Select an endpoint', 
                                    options = endpoint_options,
                                    index=None)

headers = {
    'x-rapidapi-key': '666e934e24msh842e981f4ebcf90p1369d1jsnfa7f40147688',
    'x-rapidapi-host': 'jsearch.p.rapidapi.com'
}

# @st.cache_data(ttl=3600, show_spinner='Fetching data...')
def get_data(endpoint, params):
    url = f'https://jsearch.p.rapidapi.com/{endpoint}'
    response = requests.get(url, 
                            headers=headers,
                            params=params)
    if response.status_code == 200:
        data = response.json()
        return pd.DataFrame(data.get('data', []))
    else:
        st.error(f'Error: {response.status_code}')
        return pd.DataFrame()

if endpoint_selected:
    with st.form(key = 'api_form'):
        st.subheader(f"Customize parameters for {endpoint_selected}")

        if endpoint_selected == 'search':
            query = st.text_input('Job Search Query', 
                                placeholder='e.g. developer jobs in Chicago')
            page = st.number_input('Page number', min_value=1, value=1)
            num_pages = st.number_input('Number of pages', min_value=1, value=1)
            country = st.selectbox('Country', 
                                ['us', 'ca', 'gb', 'au', 'in'], index=0)
            date_posted =  st.selectbox('Date Posted',
                                        ['all', 'today', '3days', 'week', 'month'], index=0)
            params = {
                'query': query,
                'page': str(page),
                'num_pages': str(num_pages),
                'country': country,
                'date_posted': date_posted
            }

        elif endpoint_selected == 'details':
            job_id = st.text_input('Job ID', placeholder='e.g. n20AgUu1KG0BGjzoAAAAAA==')
            country = st.selectbox('Country', 
                                ['us', 'ca', 'gb', 'au', 'in'], index=0)
            params = {
                'job_id': job_id,
                'country': country
            }

        elif endpoint_selected == 'estimated-salary':
            job_title = st.text_input('Job Title',
                                      placeholder='e.g. NodeJS Developer')
            location = st.text_input('Location',
                                     placeholder='e.g. New York')
            location_type = st.selectbox('Location Type',
                                         ['CITY', 'STATE', 'COUNTRY', 'ALL'],
                                         index=0)
            years_of_experience = st.selectbox('Years of experience',
                                               ['LESS_THAN_ONE', 'ONE_TO_THREE', 'FOUR_TO_SIX', 'SEVEN_TO_NINE', 'TEN_TO_FOURTEEN', 'ABOVE_FIFTEEN'],
                                               index=0)
            params = {
                'job_title': job_title,
                'location': location,
                'location_type': location_type,
                'years_of_experience': years_of_experience
            }

        else:
            params = {}

        submit = st.form_submit_button('Submit')

    if submit:
        with st.spinner('Fetching results...'):
            data = get_data(endpoint_selected, params)
            if not data.empty:
                st.success(f'Retrived {len(data)} rows')
                st.dataframe(data)
            else:
                st.warning('No results found')