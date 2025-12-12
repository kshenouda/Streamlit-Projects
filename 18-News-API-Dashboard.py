import streamlit as st
import pandas as pd
import requests
import datetime
import os
from textblob import TextBlob

st.set_page_config(page_title='News API App', layout='wide')
st.title('News API Application')
st.write('''
This application lets users request data from the News API. This API provides real-time news
articles from over 150,000 sources and blogs. Users may be able to search for articles on
the web that mention a specific keyword or phrase, or get the current top headlines for a 
country, category, or publisher
''')
st.divider()

api_key = st.secrets['NEWS_API_KEY']
#api_key = 'ca573d9ef5824ade877db187b4fe3b77'

st.subheader('Try requesting an article now!')
st.caption('Note: because of current API plan, we are only able to request articles as far back as 30 days')

with st.expander('Run your own request here!'):

    tab1, tab2 = st.tabs(['Search for a specific topic/keyword', 'Get current top headlines for a country/category'])

    @st.cache_data(ttl=datetime.timedelta(hours=24))
    def fetch_data(query, date, sort, page_size, page, api_key):
        url = f'https://newsapi.org/v2/everything?q={query}&from={date}&sortBy={sort}&pageSize={page_size}&page={page}&apiKey={api_key}'
        response = requests.get(url)
        json_data = response.json()
        # data = response.json()['articles']
        if json_data.get('status') == 'error':
            st.error(f"API Error: {json_data.get('message')}")
            return None
        return json_data.get('articles', [])

    @st.cache_data(ttl=datetime.timedelta(hours=24))
    def fetch_top_headlines(query, category, page_size, page, api_key):
        url = f'https://newsapi.org/v2/top-headlines?q={query}&category={category}&pageSize={page_size}&page={page}&apiKey={api_key}'
        pass

    with tab1:
        with st.form(key='specific_topic_form'):
            subject_input = st.text_input('Enter the subject you want to search for',
                                        placeholder='e.g. US economy',
                                        key='subject_input')
            subject_input = subject_input.replace(' ', '+')
            date_input = st.date_input('Select a date you want your article from')
            sort_input = st.selectbox('Select a field to sort by',
                                    options=['popularity', 'publishedAt', 'relevancy'],
                                    index=1)
            page_size_input = st.number_input('Select the page size', 1, 100, 1)
            page_input = st.number_input('Select a page', 1, 100, 1)
            submit_button = st.form_submit_button('Send Request')

        if submit_button:
            if subject_input and date_input and sort_input:
                with st.spinner('Fetching data...'):
                    articles = fetch_data(subject_input, date_input, sort_input, page_size_input, page_input, api_key)
                df = pd.DataFrame(articles)
                #df['sentiment'] = df['description'].apply(lambda x: TextBlob(x).sentiment.polarity)
                
                if len(df) == 0:
                    st.warning('No articles found for this search')
                    st.caption(f'Returned {df.shape[0]} rows')

                st.dataframe(df)
                st.caption(f'Returned {df.shape[0]} rows')

            else:
                st.warning('Please input a subject to request data about')

        if st.button('Reset Form'):
            # st.session_state.subject_input = ''
            st.rerun()


    with tab2: 
        with st.form(key='top_headlines_form'):
            submit_button = st.form_submit_button('Send Request')