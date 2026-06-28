import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px

st.set_page_config(page_title='Casino Gaming Analysis', layout='wide')
st.title('Casino Gaming Analysis')
data_url = 'https://www.kaggle.com/datasets/willianoliveiragibin/casino-gaming-data'
st.markdown('**Source**: [Kaggle](%s)' % data_url)
st.markdown('''

''')

@st.cache_data
def load_data():
    df = pd.read_csv('/Users/kiroshenouda/Desktop/COMPSCI/DATASETS/Casino_Gaming_Data new.csv')
    return df

uploaded = st.file_uploader('', type='csv')
df = pd.read_csv(uploaded)
total_wagers = df['Wagers'].sum()
total_revenue = df['Total Gross Gaming Revenue'].sum()
if uploaded:
    # df = pd.read_csv(uploaded)
    st.dataframe(df)
else:
    st.info('Upload the casino data file')

st.divider()
st.caption('Casino Gaming Analysis Application v1.0, created by Kiro Shenouda')