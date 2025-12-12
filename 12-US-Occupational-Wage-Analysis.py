import streamlit as st
import numpy as np
import pandas as pd

st.set_page_config(page_title='US Occupational Wage Analysis App',
                   layout='wide')

page_options = [
    'Intro', 
    '1. Annual Mean Wages',
    '2. Best Wage-to-Employment Efficiency',
    '3. Variation of Employment in California',
    '4. Wage Difference Between Occupations',
    '5. Employment and Wage Relationship',
    '6. Employment and Mean Wage Correlation',
    '7. Tech Occupations Earning Potential',
    '8. Healthcare and Education Occupations'
]
page_select = st.sidebar.radio('Select page', page_options)
data = pd.read_excel('/Users/kiroshenouda/Desktop/COMPSCI/DATASETS/national_M2024_dl.xlsx')
df = pd.DataFrame(data)
cat_cols = df.select_dtypes(include='object')
num_cols = df.select_dtypes(include=['number', 'float'])

if page_select == page_options[0]:
    st.title('US Occupational Wage Analysis App')
    source_url = 'https://platform.stratascratch.com/data-projects/us-wage-analysis'
    data_url = 'https://data.bls.gov/oes/#/industry/000000'
    st.write('**Source**: [Stratascratch](%s)' % source_url)
    st.write('**Dataset**: [US Bureau of Labor Stasitics](%s)' % data_url)
    st.write('The goal of this project is to perform a multi-faceted analysis' \
            'of occupational wage data across the United States. ' \
            'The dataset includes information on employment totals, average ' \
            'wages, occupation categories, and geographic distribution by state and region for the period of May 2024.')
    st.write('Our task is to analyze wage disparities, employment patterns,' \
            'and statistical relationships across different job ' \
            'sectors and states.')
    st.write('''**Objectives**:
    - Investigate wage differences across geographics and job types
    - Test hypotheses using inferential statistics (e.g. Z-test)
    - Build regression models to understand employment-wage relationships
    - Visualize wage distributions, top/bottom states, and occupational trends
    ''')
    st.divider()

    st.subheader('Raw Dataset')
    st.write(df.head(10))

if page_select == page_options[1]:
    st.title('1. Which U.S. states have the highest and lowest annual mean wages across all occupations?')
    st.write("Let's start by taking a quick look at the data")
    st.write(df.head())
    st.write(df.tail())
    ''
    if st.checkbox('Dataset Shape'):
        col1, col2 = st.columns(2)
        col1.metric(label='Rows', value=df.shape[0])
        col2.metric(label='Columns', value=df.shape[1])
    ''
    if st.checkbox('Check for missing values'):
        st.write(df.isnull().sum())
        cols_with_missing_values = df.columns[df.isnull().sum() > 0]
        st.write('Missing values for the following columns:', list(cols_with_missing_values))
    ''
    if st.checkbox('Dataset description'):
        st.write(df.describe())
        st.write("It looks like the column A_MEAN represents annual wages, but it's not showing up in the dataset description. Let's try to find why it's not showing up")
        st.write('A_MEAN data type: ', df['A_MEAN'].dtype)
        df['A_MEAN'] = df['A_MEAN'].replace('*', np.nan)
        df['A_MEAN'] = pd.to_numeric(df['A_MEAN'])
        st.write(df['A_MEAN'].describe())
        st.write('We fixed the column data type mismatch, so we can start analyzing wages')
    ''
    if st.checkbox('States Analysis'):
        st.write(df['AREA_TITLE'].value_counts())
        st.write(df['PRIM_STATE'].value_counts())