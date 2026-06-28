import streamlit as st
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

st.set_page_config(page_title='Machine Diagnostic Analysis', layout='wide')
st.title('Machine Maintenance Diagnostic Analysis')
st.markdown('''
In this application, we will perform diagnostic analytics to understand:
* What factors are most associated with machine failure?
* Which variables differ most between failed and successful machines?
* What thresholds increase failure probability?

This analysis focuses on explanation (diagnostic) rather than prediction

[Dataset source](https://www.kaggle.com/datasets/shivamb/machine-predictive-maintenance-classification)
''')
st.divider()

file = st.sidebar.file_uploader('Upload file', type='csv')

if not file:
    st.info('⬅️ Please upload the predictive maintenance file from the sidebar to start')
else:
    @st.cache_data
    def load_data(df):
        return df
    df = pd.read_csv(load_data(file))
    st.dataframe(df)

    # SIDEBAR
    st.sidebar.divider()

st.divider()
st.caption('Machine Maintenance Diagnostic Analysis Application v1.0, created by Kiro Shenouda')
