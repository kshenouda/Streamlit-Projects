import streamlit as st
import numpy as np
import pandas as pd
# import matplotlib.pyplot as plt
# import seaborn as sns
import plotly.express as px
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

st.set_page_config(page_title='Medical Costs Dashboard', 
                   initial_sidebar_state='auto',
                   layout='wide')
st.title('Medical Costs Dashboard')
data_url = 'https://www.kaggle.com/datasets/mirichoi0218/insurance/data'
st.write('**Source**: [Kaggle](%s)' % data_url)
st.write('''
This dashboard explores the Medical Costs dataset, showing how patient information -- 
age, sex, BMI, number of children, region, and whether they smoke -- to determine how
they pay for medical costs. You can explore distributions, correlations, and
a linear regression model.
''')

@st.cache_data
def load_data():
    df = pd.read_csv('/Users/kiroshenouda/Desktop/COMPSCI/DATASETS/medical-costs.csv')
    df['sex'] = df['sex'].str.title()
    df['smoker'] = df['smoker'].str.title()
    df['region'] = df['region'].str.title()
    return df

uploaded = st.sidebar.file_uploader('Upload Medical Costs Dataset', type='csv')
if uploaded:
    df = pd.read_csv(uploaded)
    df['sex'] = df['sex'].str.title()
    df['smoker'] = df['smoker'].str.title()
    df['region'] = df['region'].str.title()
else:
    df = load_data()
# st.dataframe(df.head())

if st.sidebar.button('Reset filters'):
    st.session_state.age_range = (df['age'].min(), df['age'].max())
    st.session_state.sex_filter = df['sex'].unique()
    st.session_state.smoker_filter = df['smoker'].unique()
    st.session_state.region_filter = df['region'].unique()
    # st.session_state.clear()
    st.rerun()

st.sidebar.header('Filter options')
age_range = st.sidebar.slider('Age Range',
                              int(df['age'].min()),
                              int(df['age'].max()),
                              (df['age'].min(), df['age'].max()),
                              key='age_range')
sex_filter = st.sidebar.multiselect('Sex',
                                    df['sex'].unique(),
                                    default=df['sex'].unique(),
                                    key='sex_filter')
smoker_filter = st.sidebar.multiselect('Smoker Status',
                                       df['smoker'].unique(),
                                       default=df['smoker'].unique(),
                                       key='smoker_filter')
region_filter = st.sidebar.multiselect('Region',
                                       df['region'].unique(),
                                       default=df['region'].unique(),
                                       key='region_filter')
filtered_df = df[
    (df['age'].between(age_range[0], age_range[1])) &
    (df['sex'].isin(sex_filter)) &
    (df['smoker'].isin(smoker_filter)) &
    (df['region'].isin(region_filter))
]

df_col1, df_col2 = st.columns(2)

with df_col1:
    with st.expander('View full dataset'):
        st.dataframe(df, use_container_width=True)

with df_col2:
    with st.expander('View filtered dataset'):
        st.dataframe(filtered_df, use_container_width=True)
        st.info(f'{len(filtered_df)} patients match your filters.')
        st.download_button(
            "Download filtered dataset",
            data=filtered_df.to_csv(index=False),
            mime="text/csv",
            file_name="filtered_medical_costs.csv"
        )

st.subheader('Key Metrics')

col1, col2, col3, col4 = st.columns(4)

col1.metric('Total Patients', len(df))
col2.metric('Average Charges', f'${filtered_df.charges.mean():,.2f}')
col3.metric('Average BMI', f'{filtered_df.bmi.mean():,.1f}')
col4.metric('Smokers (%)', f"{(filtered_df.smoker.eq('Yes').mean() * 100):.1f}%")

df_model = pd.get_dummies(df, drop_first=True)

#def train_model(df_model):
#    X = df_model.drop('charges', axis=1)
#    y = df_model['charges']
#    X_train, X_test, y_train, y_test = train_test_split(
#        X, y, test_size=0.3, random_state=42
#    )
#    model = LinearRegression()
#    model.fit(X_train, y_train)
#    return model, X_train, X_test, y_train, y_test

#model, X_train, X_test, y_train, y_test = train_model(df_model)

#col1, col2 = st.columns(2)

#with col1:
#with st.expander('Exploratory Analysis'):
st.subheader('Exploratory Analysis')

tab1, tab2, tab3, tab4, tab5= st.tabs(['Charges Distribution', 'Age vs. Charges', 'BMI Breakdown', 'Regional Charges Breakdown', 'Correlation Heatmap'])

with tab1:
    fig = px.histogram(filtered_df, x='charges', nbins=40,
                    title='Distribution of Medical Charges',
                    color='smoker')
    st.plotly_chart(fig, use_container_width=True)
    st.caption('While they make up only about 20% of all patients\
                in this dataset, patients who smoke generally\
                spend more on their medical costs')

with tab2: 
    fig = px.scatter(filtered_df, x='age', y='charges',
                    title='Scatter Plot of Patient Age vs. Medical Charges',
                    color='smoker')
    st.plotly_chart(fig, use_container_width=True)
    st.caption("Once again, we see that patients who smoke generally\
                have higher medical costs than patients who don't smoke")

with tab3:
    fig = px.box(filtered_df, x='smoker', y='bmi',
                title='BMI Distribution by Smoking Status',
                color='smoker')
    st.plotly_chart(fig, use_container_width=True)
    st.caption("There doesn't seem to be a large difference in BMI between\
                smoker and non-smokers")

with tab4:
    fig = px.box(filtered_df, x='region', y='charges', color='region',
                 title='Breakdown of Medical Charges Across Regions')
    st.plotly_chart(fig, use_container_width=True)
    st.caption('Patients in the Southeastern region of the US have the most\
                variability in medical costs')

with tab5:
    corr = df_model.corr()
    fig = px.imshow(corr, text_auto=True, color_continuous_scale='RdBu_r')
    st.plotly_chart(fig, use_container_width=True)
    st.caption("One of the main factors that contribute to higher medical costs\
                is smoking, with a correlation coefficient of 0.787")

#with col2:
with st.expander('Linear Regression Model and Visualizations'):
    #st.subheader('Linear Regression Model')

    #df_model = pd.get_dummies(df, drop_first=True)
    #X = df_model.drop('charges', axis=1)
    #y = df_model['charges']

    #def train_model(df_model):
    X = df_model.drop('charges', axis=1)
    y = df_model['charges']
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=42
    )
    model = LinearRegression()
    model.fit(X_train, y_train)
    #    return model, X_train, X_test, y_train, y_test

    #model, X_train, X_test, y_train, y_test = train_model(df_model)


    train_preds = model.predict(X_train)
    test_preds = model.predict(X_test)

    r2_co1, r2_col2 = st.columns(2)

    with r2_co1:
        st.subheader('R² Score')
        train_r2 = model.score(X_train, y_train)
        st.write(f'**Train Model R² Score:** {train_r2:.2f}')

        test_r2 = model.score(X_test, y_test)
        st.write(f'**Test Model R² Score:** {test_r2:.2f}')

    with r2_col2:
        st.subheader('RMSE')
        train_rmse = np.sqrt(mean_squared_error(y_train, train_preds))
        st.write(f'**Train Model RMSE:** {train_rmse:.2f}')

        test_rmse = np.sqrt(mean_squared_error(y_test, test_preds))
        st.write(f'**Test Model RMSE:** {test_rmse:.2f}')

    fig = px.scatter(x=y_test, y=test_preds,
                     labels={'x':'Actual Charges', 'y':'Predicted Charges'},
                     title='Actual vs. Predicted Charges')
    fig.add_shape(type='line', line=dict(color='blue'),
                  x0=y_test.min(), y0=y_test.min(),
                  x1=y_test.max(), y1=y_test.max())
    st.plotly_chart(fig, use_container_width=True)

    coeff_df = pd.DataFrame({
        'Feature': X.columns,
        'Coefficient': model.coef_
    }).sort_values(by='Coefficient', ascending=True)

    fig = px.bar(coeff_df, x='Coefficient', y='Feature',
                title='Model Feature Importance',
                orientation='h')
    st.plotly_chart(fig, use_container_width=True)

    test_residuals = y_test - test_preds
    fig = px.histogram(test_residuals, nbins=40,
                       title='Test Residuals Distriubtion')
    st.plotly_chart(fig, use_container_width=True)

st.markdown('''
---
**Medical Costs Dashboard** - v1.0
Built by Kiro Shenouda using Streamlit
''')