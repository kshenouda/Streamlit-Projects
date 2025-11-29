import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

st.set_page_config(page_title='Advertising Dashboard', layout='wide')
st.title('Advertising Dashboard')

st.write('''
This dashboard explores the classical Advertising dataset, showing how TV, radio,
and newspaper budgets affect product sales. You can explore distributions, correlations,
and a linear regression model.
''')

@st.cache_data
def load_data():
    df = pd.read_csv('/Users/kiroshenouda/Desktop/COMPSCI/DATASETS/advertising.csv')
    return df

uploaded_file = st.sidebar.file_uploader('Upload Advertising Dataset', type='csv')

if uploaded_file:
    df = pd.read_csv(uploaded_file)
else:
    df = load_data()

def fmt(n): 
    return f'${n:,.2f}'

st.sidebar.header('Dataset Summary')
st.sidebar.write('**Rows**: ', str(len(df)))
st.sidebar.write('**Columns**:', str(len(df.columns)))

st.sidebar.header('Filter options')
tv_range = st.sidebar.slider('TV', df['TV'].min(), df['TV'].max(),
                             (df['TV'].min(), df['TV'].max()))
radio_range = st.sidebar.slider('Radio', df['Radio'].min(), df['Radio'].max(),
                                (df['Radio'].min(), df['Radio'].max()))
newspaper_range = st.sidebar.slider('Newspaper', df['Newspaper'].min(), df['Newspaper'].max(),
                                    (df['Newspaper'].min(), df['TV'].max()))   
sales_range = st.sidebar.slider('Sales', df['Sales'].min(), df['Sales'].max(),
                                (df['Sales'].min(), df['Sales'].max()))   


filtered_df = df[
    (df['TV'].between(tv_range[0], tv_range[1])) &
    (df['Radio'].between(radio_range[0], radio_range[1])) &
    (df['Newspaper'].between(newspaper_range[0], newspaper_range[1])) &
    (df['Sales'].between(sales_range[0], sales_range[1]))
]                               

#remove_outliers = st.sidebar.checkbox('Remove outliers?')
#if remove_outliers:
#    filtered_df = filtered_df[filtered_df['TV'] < filtered_df['TV'].quantile(0.99)]

with st.expander('View raw dataset'):
    st.dataframe(df)

col1, col2 = st.columns(2)

with col1:
    st.subheader('Key Metrics')

    met_col1, met_col2 = st.columns(2)

    avg_tv_spend = filtered_df['TV'].mean()
    avg_radio_spend = filtered_df['Radio'].mean()
    avg_newspaper_spend = filtered_df['Newspaper'].mean()
    avg_sales = filtered_df['Sales'].mean()

    met_col1.metric('Average TV Spend', f'${avg_tv_spend:.2f}')
    met_col2.metric('Average Radio Spend', f'${avg_radio_spend:.2f}')
    met_col1.metric('Average Newspaper Spend',f'${avg_newspaper_spend:.2f}')
    met_col2.metric('Average Sales', f'${avg_sales:.2f}')

with col2:
    st.subheader('Visualizations')
    # selected_column = st.selectbox('Choose a column to visualize', df.columns.unique(), index=None)
    selected_column = st.selectbox('Choose a column to visualize', df.columns.unique())

    if selected_column:
        fig = px.histogram(filtered_df, x=selected_column, nbins=40,
                       title=f'{selected_column} Distribution')
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info('Select a column to visualize')

with st.expander('Linear Regression Model Details'):
    # st.subheader('Linear Regression')
    X = df.drop('Sales', axis=1)
    y = df['Sales']

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=42
    )

    model = LinearRegression()
    model.fit(X_train, y_train)

    r2_col1, r2_col2 = st.columns(2)

    with r2_col1:
        st.subheader('R² Score')
        r2_train = model.score(X_train, y_train)
        st.write(f'**Training R² Score**: {r2_train:.4f}')

        r2_test = model.score(X_test, y_test)
        st.write(f'**Test R² Score**: {r2_test:.4f}')

    with r2_col2:
        st.subheader('RMSE')
        train_rmse = mean_squared_error(y_train, model.predict(X_train), squared=False)
        st.write(f'**Training RMSE**: {train_rmse:.4f}')

        test_rmse = mean_squared_error(y_test, model.predict(X_test), squared=False)
        st.write(f'**Test RMSE**: {train_rmse:.4f}')

    coeff_df = pd.DataFrame({
        'Feature': X.columns,
        'Coefficient': model.coef_
    }).sort_values(by='Coefficient', ascending=False)
    coeff_df

    fig = px.bar(coeff_df, x='Coefficient', y='Feature',
                title='Model Feature Importance',
                orientation='h')
    st.plotly_chart(fig, use_container_width=True)

    train_preds = model.predict(X_train)
    fig = px.scatter(x=y_train, y=train_preds,
                     labels={'x': 'Actual Sales', 'y': 'Predicted Sales'},
                     title = 'Predicted vs. Actual Sales',
                     trendline='ols')
    st.plotly_chart(fig, use_container_width=True)

with st.container():
    with st.expander('Scatter Plots'):
        # st.subheader('Scatter Plots')
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
            fig = px.scatter(filtered_df, x=x_col, y=y_col,
                            title=f'Scatterplot Between {x_col} and {y_col}',
                            trendline='ols')
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info('Please select an X-axis and Y-axis to generate a scatterplot')

    with st.expander('Heatmap'):
        st.subheader('Correlation Heatmap')
        corr = df.corr()
        fig = px.imshow(corr, text_auto=True, title='Correlation Heatmap')
        st.plotly_chart(fig, use_container_width=True)

with st.expander('Try Your Own Ad Budget'):
    # st.subheader('Try Your Own Ad Budget')

    tv = st.slider('TV', 0.0, 300.0, 100.0)
    radio = st.slider('Radio', 0.0, 60.0, 20.0)
    newspaper = st.slider('Newspaper', 0.0, 120.0, 30.0)

    input_data = np.array([[tv, radio, newspaper]])
    prediction = model.predict(input_data[0].reshape(1,-1))
    st.metric('Predicted Sales', f'{prediction}')