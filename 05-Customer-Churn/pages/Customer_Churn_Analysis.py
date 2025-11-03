# Load libraries
import streamlit as st
from datetime import datetime
import altair as alt
import pandas as pd

# Set page config
st.set_page_config(page_title = 'Customer Churn Exploration', layout = 'wide')

# Title and description
'''
# Customer Churn Exploration
This page shows a quick description and exploration of the data so we know what we're working with before constructing a prediction model.
'''

''
'''
### Raw Data
'''
df = pd.read_csv('/Users/kiroshenouda/Desktop/COMPSCI/DATASETS/Customer Churn/customer_churn_dataset-training-master.csv')
st.dataframe(df)

''
'''
### Dataset Columns
'''
st.dataframe(list(df.columns))

''
'''
### Row Count and Column Distribution
'''
# Display metrics for numerical, categorical columns here
cat_cols = df.select_dtypes(include = 'object').columns
num_cols = df.select_dtypes(include = 'number').columns

with st.container(horizontal = True, gap = 'medium'):
    cols = st.columns(3, gap = 'medium', width = 900)
    with cols[0]:
        st.metric(
            'Row Count',
            len(df),
            width = 'content'
        )
    with cols[1]:
        st.metric(
            'Numerical Column Count',
            len(num_cols),
            width = 'content'
        )
    with cols[2]:
        st.metric(
            'Categorical Column Count',
            len(cat_cols),
            width = 'content'
        )

''
'''
### Data Info and Description
'''
st.dataframe(df.describe())
if(len(cat_cols) > 0):
    for col in cat_cols:
        st.write(f'**{col}**')
        st.write(df[col].value_counts())

''
'''
### Numerical Column Visual Summary
'''
if(len(num_cols) > 0):
    selected_num_col = st.selectbox('Select a numeric column to visualize', num_cols)
    num_hist_chart = (
        alt.Chart(df).mark_bar().encode(
            alt.X(selected_num_col, bin = alt.Bin(maxbins = 30)),
            y = 'count()',
            tooltip = [selected_num_col, 'count()']
        ).properties(height = 300)
    )
    st.altair_chart(num_hist_chart, use_container_width=True)
else:
    st.write('This dataset does not have any numerical columns')

''
'''
### Categorical Column Visual Summary
'''
if(len(cat_cols) > 0):
    selected_cat_col = st.selectbox('Select a categorical column to visualize', cat_cols)
    cat_hist_chart = (
        alt.Chart(df).mark_bar().encode(
            alt.X(selected_cat_col, sort = '-y'), #bin = alt.Bin(maxbins = 30)),
            y = 'count()',
            tooltip = [selected_cat_col, 'count()']
        ).properties(height = 300)
    )
    st.altair_chart(cat_hist_chart, use_container_width = True)
else:
    st.write('This dataset does not have any categorical columns')