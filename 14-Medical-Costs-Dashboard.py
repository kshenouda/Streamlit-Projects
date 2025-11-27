import streamlit as st
import numpy as np
import pandas as pd
# import matplotlib.pyplot as plt
# import seaborn as sns
import plotly.express as px
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

st.set_page_config(page_title='Medical Costs Dashboard', 
                   initial_sidebar_state='auto',
                   layout='centered')
st.title('Medical Costs Dashboard')
# st.write('A professional analytics dashboard built with Streamlit')

data_url = 'https://www.kaggle.com/datasets/mirichoi0218/insurance/data'
st.write('**Source**: [Kaggle](%s)' % data_url)

@st.cache_data
def load_data():
    df = pd.read_csv('/Users/kiroshenouda/Desktop/COMPSCI/DATASETS/medical-costs.csv')
    df['sex'] = df['sex'].str.title()
    df['smoker'] = df['smoker'].str.title()
    df['region'] = df['region'].str.title()
    return df

df = load_data()
# st.dataframe(df.head())

st.sidebar.header('Filter options')
age_range = st.sidebar.slider('Age Range',
                              int(df['age'].min()),
                              int(df['age'].max()),
                              (df['age'].min(), df['age'].max()))
sex_filter = st.sidebar.multiselect('Sex',
                                    df['sex'].unique(),
                                    default=df['sex'].unique())
smoker_filter = st.sidebar.multiselect('Smoker Status',
                                       df['smoker'].unique(),
                                       default=df['smoker'].unique())
region_filter = st.sidebar.multiselect('Smoker',
                                       df['region'].unique(),
                                       default=df['region'].unique())
filtered_df = df[
    (df['age'].between(age_range[0], age_range[1])) &
    (df['sex'].isin(sex_filter)) &
    (df['smoker'].isin(smoker_filter)) &
    (df['region'].isin(region_filter))
]

st.subheader('Key Metrics')

col1, col2, col3, col4 = st.columns(4)

col1.metric('Total Patients', len(df))
col2.metric('Average Charges', f'${filtered_df.charges.mean():,.2f}')
col3.metric('Average BMI', f'{filtered_df.bmi.mean():,.1f}')
col4.metric('Smokers (%)', f"{(filtered_df.smoker.eq('Yes').mean() * 100):.1f}%")

col1, col2 = st.columns(2)

with col1:
    st.subheader('Exploratory Analysis')

    tab1, tab2, tab3 = st.tabs(['Charges Distribution', 'Age vs. Charges', 'BMI Breakdown'])

    with tab1:
        fig = px.histogram(filtered_df, x='charges', nbins=40,
                        title='Distribution of Medical Charges',
                        color='smoker')
        st.plotly_chart(fig, use_container_width=True)

    with tab2: 
        fig = px.scatter(filtered_df, x='age', y='charges',
                        title='Scatter Plot of Patient Age vs. Medical Charges',
                        color='smoker')
        st.plotly_chart(fig, use_container_width=True)

    with tab3:
        fig = px.box(filtered_df, x='smoker', y='bmi',
                    title='BMI Distribution by Smoking Status',
                    color='smoker')
        st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader('Linear Regression Model')

    df_model = pd.get_dummies(df, drop_first=True)
    X = df_model.drop('charges', axis=1)
    y = df_model['charges']

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=42
    )

    model = LinearRegression()
    model.fit(X_train, y_train)

    r2 = model.score(X_test, y_test)

    st.write(f'**Model R² Score:** {r2:.2f}')

    coeff_df = pd.DataFrame({
        'Feature': X.columns,
        'Coefficient': model.coef_
    }).sort_values(by='Coefficient', ascending=True)

    fig = px.bar(coeff_df, x='Coefficient', y='Feature',
                title='Model Feature Importance',
                orientation='h')
    st.plotly_chart(fig, use_container_width=True)

with st.expander('View Raw Dataset'):
    st.dataframe(filtered_df, use_container_width=True)