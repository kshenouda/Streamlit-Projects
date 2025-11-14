import streamlit as st
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import LabelEncoder

st.set_page_config(page_title='Bike Shares Regression', layout='wide')
st.title('Bike Shares Regression App')

st.sidebar.header('This predicts bike rentals in Seoul, South Korea based on user input')
st.sidebar.text('This is a web application that will predict bike rentals using a random forest regressor')

raw = pd.read_csv('/Users/kiroshenouda/Desktop/COMPSCI/DATASETS/SeoulBikeData.csv', encoding='latin-1')
df = raw.dropna()
df = df.drop(columns=['Date'])

cat_cols = df.select_dtypes(include='object').columns
for cols in cat_cols:
    df[cols] = pd.to_numeric(df[cols], errors='coerce')

X = df.drop(columns = ['Rented Bike Count'], axis = 1)
y = df['Rented Bike Count'].values

regr = LinearRegression()
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.3, random_state = 1)
regr.fit(X_train, y_train)

def main():
    st.subheader('Raw Data')
    if st.checkbox('Check to preview table'):
        st.write(df.head())

    # with st.form(key='params'):
    st.subheader('Configure parameters')
    hour = st.slider('Enter hour', 0, 23)
    temp = st.slider('Enter temperature (in celsius)', -25, 25)
    humidity = st.slider('Enter humidity', 0, 98)
    wind = st.slider('Enter wind speed', 0.00, 7.40)
    position = st.slider('Enter visibility', 27, 2000)
    dew = st.slider('Enter dew point', -36.6, 27.2)
    solar = st.slider('Enter solar radiation', 0.0, 3.52)
    rainfall = st.slider('Enter rainfall', 0, 35)
    snowfall = st.slider('Enter snowfall', 0.0, 8.8)
    seasons = st.slider('Enter seasons - 0 for spring, 1 for summer, 2 for autumn, and 3 for winter', 0, 3)
    holiday = st.slider('Enter holiday - 0 for no holiday, 1 for holiday', 0, 1)
    functioning_day = st.slider('Etner whether functioning day or not - 0 for no, 1 for yes', 0, 1)

    inputs = [[hour, temp, humidity, wind, position, dew, solar, rainfall, snowfall, seasons, holiday, functioning_day]]

    if st.button('Predict model'):
        result = LinearRegression.predict(inputs)
        updated_res = result.flatten().astype(float)
        st.write(updated_res)

main()