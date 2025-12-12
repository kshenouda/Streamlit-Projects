import streamlit as st
import mysql.connector
#import mysqlclient

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
    st.write(df)
except Exception as e:
    st.error(f'Query error: {e}')

df.shape