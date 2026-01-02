import streamlit as st
import numpy as np
import pandas as pd
import seaborn as sns
import plotly.express as px
from ucimlrepo import fetch_ucirepo
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix

st.set_page_config(page_title='Obesity Levels Estimation App', layout='wide')
st.title('Obesity Levels Estimation')

pages = [
    'Home Page',
    'Table Info',
    'Column Overview',
    'Visualizations',
    'Predicting Obesity',
    'Data Dictionary'
]
st.sidebar.title('Page Navigation')
page_options = st.sidebar.radio('Select a page', pages)

@st.cache_data
def load_data():
    try:
        data = fetch_ucirepo(id=544)
        X = data.data.features
        y = data.data.targets
        return data, X, y
    except Exception as e:
        st.error(f'Error loading data: {str(e)}')
        st.stop()

with st.spinner('Loading data...'):
    data, X, y = load_data()
    #st.write(X)
    #st.write(y)

if page_options == pages[0]:
    st.markdown('''
    ### About this Application
    This application will allow users to view, explore,
    and estimate obesity levels in individuals from the 
    countries of Mexico, Peru, nad Colombia, based on
    their eating habits and physical condiitons.
    
    ### Features You Can Explore
    - Person demographics (e.g. age, gender)
    - Physical attributes (e.g. height, weight, and family history of obesity)
    - Diet information (e.g. does the person eat high caloric foods, do they regularly eat vegetables, etc)
    - Day-to-day activities (e.g. exercise, technological device usage)
    
    You can navigate between the different pages of this application
    from the sidebar on the left.

    Source: [UC Irvine Machine Learning Repository](https://archive.ics.uci.edu/dataset/544/estimation+of+obesity+levels+based+on+eating+habits+and+physical+condition)
    ''')

if page_options == pages[1]:
    st.subheader('Table Overview')
    show_rows = st.slider('Number of rows to display', 5, 50, 10, key='show_rows')
    st.dataframe(X.head(show_rows), use_container_width=True)
    st.subheader('Quick Statistics')
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.metric('Average Age', round(X.Age.mean(),1))
    with col2:
        st.metric('Average Height (m)', round(X.Height.mean(),1))
    with col3:
        st.metric('Average Weight (kg)', round(X.Weight.mean(),1))
    with col4:
        st.metric('Male Patients', len(X[X.Gender == 'Male']))
    with col5:
        st.metric('Female Patients', len(X[X.Gender == 'Female']))
    with st.expander('View Column Details'):
        st.dataframe(pd.DataFrame({
            'Column': X.columns,
            'Data Type': X.dtypes,
            'Non-Null Counts': X.isnull().sum(),
            'Unique Values': X.nunique()       
        }))

if page_options == pages[2]:
    st.subheader('Column Overview')
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric('Total columns', len(X.columns))
    with col2:
        st.metric('Numeric columns', len(X.select_dtypes(include=['number', 'float64']).columns.tolist()))
    with col3:
        st.metric('Categorical columns', len(X.select_dtypes(include='object').columns.tolist()))

if page_options == pages[3]:
    st.subheader('Visualizations')
    tab1, tab2 = st.tabs(['Features', 'Target'])
    with tab1:
        st.markdown('''
        Select a numeric and categorical column to visualize.
        ''')
        col1, col2 = st.columns(2)
        with col1:
            num_col_selection = st.selectbox('Numeric columns', X.select_dtypes(include=['number']).columns)
            fig = px.histogram(X, x=num_col_selection, nbins=40,
                               title=f'Distribution of {num_col_selection}')
            st.plotly_chart(fig, use_container_width=True)
        with col2:
            cat_col_selection = st.selectbox('Categorical columns', X.select_dtypes(include='object').columns)
            fig = px.bar(X[cat_col_selection].value_counts(),
                         title=f'Distribution of {cat_col_selection}')
            fig.update_layout(showlegend=False)
            st.plotly_chart(fig, use_container_width=True)
    with tab2:
        #corr = X.select_dtypes(exclude='object').corr()
        #st.write(corr)
        fig = px.bar(y['NObeyesdad'].value_counts(),
                     title=f'Distribution of Target Variable')
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

if page_options == pages[4]:
    st.subheader('Predicting Obesity Levels')
    tab1, tab2 = st.tabs([
        'Step 1 - Dummy Variables', 
        'Step 2 - Splitting Data'
    ])
    with tab1:
        st.markdown('''
        The first step we need to perform is to create dummy variables
        for categorical variables so we can feed it to a Logistic 
        Regression model.

        Below are the newly created dummy variables for the categorical
        columns in the dataset:
        ''')
        cat_cols = X.select_dtypes(include='object').columns
        X_encoded = pd.get_dummies(X, columns=cat_cols)
    with tab2:
        st.markdown('''
        Now that categorical variables are converted, we should split
        the dataset using train_test_split.
        ''')
        X_train, X_test, y_train, y_test = train_test_split(X_encoded, y, test_size=0.3, random_state=42)
        log_model = LogisticRegression()
        log_model.fit(X_train, y_train)

if page_options == pages[5]:
    st.subheader('Abstract')
    st.write(data.metadata.abstract)
    with st.expander('View metadata'):
        st.write(data.metadata)

st.divider()
st.caption('Obesity Levels Estimation Application v 1.0 | Created by Kiro Shenouda')