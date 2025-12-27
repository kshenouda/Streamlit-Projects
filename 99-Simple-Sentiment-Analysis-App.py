import streamlit as st
import numpy as np
import pandas as pd
from textblob import TextBlob

st.set_page_config(page_title='Simple Sentiment Analysis App', layout='wide')
st.title('Simple Sentiment Analysis App')
st.markdown('''
This is a simple application that allows users to analyze 
the sentiment of their inputted text.
''')

user_input = st.text_area('Enter your text here:', height=100)

if st.button('Analyze Sentiment'):
    if user_input:
        blob = TextBlob(user_input)
        polarity = blob.sentiment.polarity
        subjectivity = blob.sentiment.subjectivity

        st.subheader('Analysis Results:')
        if polarity > 0:
            sentiment = 'Positive 😊'
            st.success(sentiment)
        elif polarity < 0:
            sentiment = 'Negative 😡'
            st.error(sentiment)
        else:
            sentiment = 'Neutral 😐'
            st.info(sentiment)

        st.write(f'Polarity score: {polarity:.2f} (ranges from -1 to 1)')
        st.write(f'Subjectivity score: {subjectivity:.2f} (ranges from 0 to 1, where 1 is very subjective)')
    else:
        st.warning('Please enter some text for analysis')