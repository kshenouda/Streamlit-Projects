import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

st.set_page_config(page_title='Advertising Dashboard', layout='wide')
st.title('Advertising Dashboard')

@st.cache_data
def load_data():
    df = pd.read_csv('/Users/kiroshenouda/Desktop/COMPSCI/DATASETS/advertising.csv')
    return df

df = load_data()

with st.expander('View raw dataset'):
    st.dataframe(df.head())

col1, col2 = st.columns(2)

with col1:
    st.subheader('Key Metrics')

    met_col1, met_col2 = st.columns(2)

    avg_tv_spend = df['TV'].mean()
    avg_radio_spend = df['Radio'].mean()
    avg_newspaper_spend = df['Newspaper'].mean()
    avg_sales = df['Sales'].mean()

    met_col1.metric('Average TV Spend', f'${avg_tv_spend:.2f}')
    met_col2.metric('Average Radio Spend', f'${avg_radio_spend:.2f}')
    met_col1.metric('Average Newspaper Spend',f'${avg_newspaper_spend:.2f}')
    met_col2.metric('Average Sales', f'${avg_sales:.2f}')

with col2:
    st.subheader('Visualizations')
    selected_column = st.selectbox('Choose a column to visualize', df.columns.unique(), index=None)
    fig = px.histogram(df, x=selected_column, nbins=40,
                       title=f'{selected_column} Distribution')
    if selected_column:
        st.plotly_chart(fig, use_container_width=True)
    else:
        pass

st.subheader('Linear Regression')
X = df.drop('Sales', axis=1)
y = df['Sales']

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42
)

model = LinearRegression()
model.fit(X_train, y_train)

r2_train = model.score(X_train, y_train)

st.write(f'**Model R² Score:** {r2_train:.4f}')

coeff_df = pd.DataFrame({
    'Feature': X.columns,
    'Coefficient': model.coef_
}).sort_values(by='Coefficient', ascending=False)
coeff_df

fig = px.bar(coeff_df, x='Coefficient', y='Feature',
             title='Model Feature Importance',
             orientation='h')
st.plotly_chart(fig, use_container_width=True)

st.subheader('Scatter Plots')
col1, col2 = st.columns(2)
all_cols = df.columns
with col1:
    x_col = st.selectbox('Choose an column for the X-axis', df.columns, index=None)
available_cols = [
    col for col in all_cols if col != x_col
]
with col2:
    y_col = st.selectbox('Choose an column for the Y-axis', available_cols, index=None)

if x_col and y_col:
    fig = px.scatter(df, x=x_col, y=y_col,
                     title=f'Scatterplot Between {x_col} and {y_col}')
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info('Please select an X-axis and Y-axis to generate a scatterplot')



# daniel is finishing up capital one
# dan will send to Mina to review with lawyers
# he has drafts with tax returns
# dan finished up to 2022
# execute 