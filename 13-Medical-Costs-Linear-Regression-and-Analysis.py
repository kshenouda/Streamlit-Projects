import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import kagglehub
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from statsmodels.stats.outliers_influence import variance_inflation_factor

from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import Ridge
import joblib
from pathlib import Path

st.set_page_config(page_title='Insurance Analysis', layout='wide')
st.title('Medical Costs Linear Regression and Analysis')

data_url = 'https://www.kaggle.com/datasets/mirichoi0218/insurance/data'
st.write('**Source**: [Kaggle](%s)' % data_url)

@st.cache_data(ttl=3600)
def load_data_from_file(file):
    return pd.read_csv(file)

uploaded_file = st.file_uploader('Select the Medical Costs dataset to upload', type='csv')

if uploaded_file is not None:
    data = load_data_from_file(uploaded_file)
    df = pd.DataFrame(data)

    st.write(df.head())

    num_features = ['age', 'bmi', 'children']
    cat_features = ['sex', 'smoker', 'region']

    num_pipeline = Pipeline([
        ('scaler', StandardScaler())
    ])

    cat_pipeline = Pipeline([
        ('onehot', OneHotEncoder(handle_unknown='ignore', sparse=False))
    ])

    preprocessor = ColumnTransformer(transformers=[
        ('num', num_pipeline, num_features),
        ('cat', cat_pipeline, cat_features)
    ])    

    pipeline = Pipeline([
        ('preprocess', preprocessor),
        ('model', Ridge(alpha=1.0))
    ])

    X = df[num_features + cat_features]
    y = df['charges']


    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=23
    )
    # pipeline.fit(X_train, y_train)

    MODEL_PATH = Path('models')
    MODEL_PATH.mkdir(exist_ok=True)

    @st.cache_resource
    def train_and_cache_pipeline(_pipeline, X_train, y_train):
        pipeline.fit(X_train, y_train)
        joblib.dump(pipeline, MODEL_PATH / 'ridge_pipeline.joblib')
        return pipeline
    
    model = train_and_cache_pipeline(pipeline, X_train, y_train)

    y_pred = model.predict(X_test)
    rmse = mean_squared_error(y_test, y_pred, squared=False)
    r2 = r2_score(y_test, y_pred)
    mae = mean_absolute_error(y_test, y_pred)

    col1, col2, col3 = st.columns(3)
    col1.metric('R²', f'{r2:.2f}')
    col2.metric('Root Mean Squared Error', f'{rmse:.2f}')
    col3.metric('Mean Absolute Error', f'{mae:.2f}')

    # Residual plots
    fig, ax = plt.subplots()
    ax.scatter(y_pred, y_test - y_pred, alpha=0.6)
    ax.axhline(0, color='k', linestyle='--')
    ax.set_title('Residuals vs. Predicted Charges')
    ax.set_xlabel('Predicted Charges')
    ax.set_ylabel('Residuals')
    st.pyplot(fig)

    def load_model(path='models/ridge_pipeline.joblib'):
        return joblib.load(path)

    X_trans = preprocessor.fit_transform(X)
    cols = []
    num_cols = num_features
    cat_onehot_names = preprocessor.named_transformers_['cat']['onehot'].get_feature_names_out(cat_features)
    cols = list(num_cols) + list(cat_onehot_names)
    X_trans_df = pd.DataFrame(X_trans, columns=cols)

    vif_data = pd.DataFrame({
        'feature': X_trans_df.columns,
        'VIF': [variance_inflation_factor(X_trans_df.values, i) for i in range(X_trans_df.shape[1])]
    })
    st.dataframe(vif_data.sort_values('VIF', ascending=False))

    min_age = df['age'].min()
    max_age = df['age'].max()
    mean_age = round(df['age'].mean())

    male_count = len(df[df['sex'] == 'male'])
    female_count = len(df[df['sex'] == 'female'])

    min_bmi = df['bmi'].min()
    max_bmi = df['bmi'].max()
    mean_bmi = round(df['bmi'].mean())

    min_children = df['children'].min()
    max_children = df['children'].max()
    mean_children = round(df['children'].mean())

    smoker_count = len(df[df['smoker'] == 'yes'])
    non_smoker_count = len(df[df['smoker'] == 'no'])

    region_southwest = len(df[df['region'] == 'southwest'])
    region_southeast = len(df[df['region'] == 'southeast'])
    region_northwest = len(df[df['region'] == 'northwest'])
    region_northeast = len(df[df['region'] == 'northeast'])

    min_charges = round(df['charges'].min(),2)
    max_charges = round(df['charges'].max(),2)
    mean_charges = round(df['charges'].mean(),2)

    if st.checkbox('Click to show summary statistics for each column'):
        tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
            'Age',
            'Sex',
            'BMI',
            'Children',
            'Smoker',
            'Region',
            'Charges'
        ])

        with tab1:
            col1, col2, col3 = st.columns(3)
            col1.metric(label='Min Age', value=min_age)
            col2.metric(label='Max Age', value=max_age)
            col3.metric(label='Average Age', value=mean_age)
        with tab2:
            col1, col2 = st.columns(2)
            col1.metric(label='Number of Male Patients', value=male_count)
            col2.metric(label='Number of Female Patients', value=female_count)
        with tab3:
            col1, col2, col3 = st.columns(3)
            col1.metric(label='Min BMI', value=min_bmi)
            col2.metric(label='Max BMI', value=max_bmi)
            col3.metric(label='Average BMI', value=mean_bmi)
        with tab4:
            col1, col2, col3 = st.columns(3)
            col1.metric(label='Min Number of Children', value=min_children)
            col2.metric(label='Max Number of Children', value=max_children)
            col3.metric(label='Average Number of Children', value=mean_children)
        with tab5:
            col1, col2 = st.columns(2)
            col1.metric(label='Number of Smokers', value=smoker_count)
            col2.metric(label='Number of Non-Smokers', value=non_smoker_count)
        with tab6:
            col1, col2, col3, col4 = st.columns(4)
            col1.metric(label='Southwest Patients', value=region_southwest)
            col2.metric(label='Southeast Patients', value=region_southeast)
            col3.metric(label='Northwest Patients', value=region_northwest)
            col4.metric(label='Northeast Patients', value=region_northeast)
        with tab7:
            col1, col2, col3 = st.columns(3)
            col1.metric(label='Min Charges', value=min_charges)
            col2.metric(label='Max Charges', value=max_charges)
            col3.metric(label='Average Charges', value=mean_charges)

    df_encoded = pd.get_dummies(df,
                                columns=['sex', 'smoker', 'region'],
                                drop_first=True,
                                dtype=int)

    indep_variables = df_encoded.drop(labels='charges', axis=1)
    dep_variables = df_encoded['charges']
    cat_cols = []
    num_cols = []

    for col in df.columns:
        if df[col].dtype == 'object':
            cat_cols.append(col)
        else:
            num_cols.append(col)

    #fig, ax = plt.subplots(figsize=(8,6))
    #sns.boxplot(x=df['sex'], y=df['age'], 
    #            data=df, ax=ax)
    #plt.title('Patient Age Distributed by Sex')
    #plt.xlabel('Sex')
    #plt.ylabel('Age')
    #st.plotly_chart(fig)

    if st.checkbox('Click to see Age boxplots'):
        fig1 = px.box(df, x='sex', y='age',
                    title='Boxplot of Patient Age by Sex',
                    #points = 'all',
                    color = 'sex')
        st.plotly_chart(fig1, use_container_width=True)

        fig2 = px.box(df, x='smoker', y='age',
                    title='Boxplot of Patient Age by Smoker Status',
                    color='smoker')
        st.plotly_chart(fig2, use_container_width=True)

        fig3 = px.box(df, x='region', y='age',
                    title='Boxplot of Patient Age by Region',
                    color='region')
        st.plotly_chart(fig3, use_container_width=True)

    if st.checkbox('Click to see BMI boxplots'):
        fig1 = px.box(df, x='sex', y='bmi',
                    title='Boxplot of Patient BMI by Sex',
                    #points = 'all',
                    color = 'sex')
        st.plotly_chart(fig1, use_container_width=True)

        fig2 = px.box(df, x='smoker', y='bmi',
                    title='Boxplot of Patient BMI by Smoker Status',
                    color='smoker')
        st.plotly_chart(fig2, use_container_width=True)

        fig3 = px.box(df, x='region', y='bmi',
                    title='Boxplot of Patient BMI by Region',
                    color='region')
        st.plotly_chart(fig3, use_container_width=True)

    if st.checkbox('Click to see Children boxplots'):
        fig1 = px.box(df, x='sex', y='children',
                    title='Boxplot of Patient Children by Sex',
                    #points = 'all',
                    color = 'sex')
        st.plotly_chart(fig1, use_container_width=True)

        fig2 = px.box(df, x='smoker', y='children',
                    title='Boxplot of Patient Children by Smoker Status',
                    color='smoker')
        st.plotly_chart(fig2, use_container_width=True)

        fig3 = px.box(df, x='region', y='children',
                    title='Boxplot of Patient Children by Region',
                    color='region')
        st.plotly_chart(fig3, use_container_width=True)

    if st.checkbox('Click to see Charges boxplots'):
        fig1 = px.box(df, x='sex', y='charges',
                    title='Boxplot of Patient Charges by Sex',
                    #points = 'all',
                    color = 'sex')
        st.plotly_chart(fig1, use_container_width=True)

        fig2 = px.box(df, x='smoker', y='charges',
                    title='Boxplot of Patient Charges by Smoker Status',
                    color='smoker')
        st.plotly_chart(fig2, use_container_width=True)

        fig3 = px.box(df, x='region', y='charges',
                    title='Boxplot of Patient Charges by Region',
                    color='region')
        st.plotly_chart(fig3, use_container_width=True)


    # st.write(df.isnull().sum())
    # No missing values

    corr = df_encoded.corr()
    fig, ax = plt.subplots()
    sns.set_theme(font_scale=0.8)
    sns.heatmap(corr, annot=True, cmap='coolwarm')
    # st.pyplot(fig)

    if st.checkbox('Click to see VIF of Independent Variables'):
        vif = pd.DataFrame()
        vif['VIF'] = [variance_inflation_factor(indep_variables.values, i) for i in range(indep_variables.shape[1])]
        vif['Features'] = indep_variables.columns
        st.subheader('VIF (Variance Inflation Factor) of Independent Variables')
        vif
        st.write('Since BMI has a VIF of 11.3584, we will create a copy of the dataset without it')

    df_encoded_copy = df_encoded.copy()
    df_encoded_copy.drop('bmi', axis=1, inplace=True)

    fig = plt.figure(figsize=(12,4))
    ax = fig.add_subplot(121)
    sns.histplot(df['charges'], bins=50, ax=ax)
    ax.set_title('Distribution of Insurance Charges')

    ax = fig.add_subplot(122)
    sns.histplot(np.log10(df['charges']), bins=50, ax=ax)
    ax.set_title('Distribution of Insurance Chages in Log Scale')
    # st.pyplot(fig)

    box_fig = plt.figure(figsize=(14,6))
    sns.boxplot(x='children', y='charges', data=df, hue='sex')
    plt.title('Boxplot of Charges vs. Number of Children')
    # st.pyplot(box_fig)

    # df_encoded.groupby('children').agg(['mean','min','max'])['charges']

    fig = plt.figure(figsize=(14, 6))
    ax = fig.add_subplot(121)
    sns.scatterplot(x='age', y='charges', hue='smoker', data=df, ax=ax)
    ax.set_title('Scatter Plot of Charges vs. Age')

    ax = fig.add_subplot(122)
    sns.scatterplot(x='bmi', y='charges', hue='smoker', data=df, ax=ax)
    ax.set_title('Scatter Plot of Charges vs. BMI')
    # st.pyplot(fig)

    X = df_encoded.drop(labels='charges', axis=1)
    y = df_encoded['charges']

    #X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=0.3,random_state=23)

    #lin_reg = LinearRegression()
    #lin_reg.fit(X_train, y_train)