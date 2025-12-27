import streamlit as st
import mysql.connector
import pandas as pd
import plotly.express as px
# import mysqlclient

st.set_page_config(page_title='Uber Ride Bookings', layout='wide')
st.title('Uber Ride Bookings')
st.markdown('''
The following dataset contains ride-sharing data from Uber for the
year 2024, providing insights into booking patterns, vehicle
performance, revenue streams, cancellation behaviors, and
customer satisfaction metrics.
''')

conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='CombatArms12'
)

#st.write(mydb)
try:
    conn = st.connection('mysql', type='sql')
except Exception as e:
    st.error(f'Connection error: {e}')
    st.stop()

try:
    df = conn.query('SELECT * FROM KAGGLE.ride_bookings;')
    df2 = df.copy()
    st.write(df2)
except Exception as e:
    st.error(f'Query error: {e}')

df.shape