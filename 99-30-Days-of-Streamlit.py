import streamlit as st
import pandas as pd
import requests

st.set_page_config('30 Days of Streamlit')
st.title('30 Days of Streamlit')
st.divider()

st.subheader('Day 14: Streamlit Components')
st.markdown('''
Components are third-party Python modules that extend what we can
do in Streamlit.

There are several dozens of Streamlit components featured
on Streamlit's website.

One example of Streamlit's components is the `streamlit_pandas_profiling`:
''')
import pandas_profiling
from streamlit_pandas_profiling import st_profile_report

st.code('''
df = pd.read_csv('https://raw.githubusercontent.com/dataprofessor/data/master/penguins_cleaned.csv')
st.code("pr = df.profile_report()")
st_profile_report(pr)
''')
st.divider()

st.subheader('Day 21: st.progress')
import time
bar = st.progress(0)

#for percent in range(100):
#    time.sleep(0.05)
#    bar.progress(percent + 1)

#st.balloons()
st.divider()

st.subheader('Day 22: st.form')
import streamlit as st

# Full example of using the with notation
st.header('1. Example of using `with` notation')
st.subheader('Coffee machine')

with st.form('my_form'):
    st.subheader('**Order your coffee**')

    # Input widgets
    coffee_bean_val = st.selectbox('Coffee bean', ['Arabica', 'Robusta'])
    coffee_roast_val = st.selectbox('Coffee roast', ['Light', 'Medium', 'Dark'])
    brewing_val = st.selectbox('Brewing method', ['Aeropress', 'Drip', 'French press', 'Moka pot', 'Siphon'])
    serving_type_val = st.selectbox('Serving format', ['Hot', 'Iced', 'Frappe'])
    milk_val = st.select_slider('Milk intensity', ['None', 'Low', 'Medium', 'High'])
    owncup_val = st.checkbox('Bring own cup')

    # Every form must have a submit button
    submitted = st.form_submit_button('Submit')

if submitted:
    st.markdown(f'''
        ☕ You have ordered:
        - Coffee bean: `{coffee_bean_val}`
        - Coffee roast: `{coffee_roast_val}`
        - Brewing: `{brewing_val}`
        - Serving type: `{serving_type_val}`
        - Milk: `{milk_val}`
        - Bring own cup: `{owncup_val}`
        ''')
else:
    st.write('☝️ Place your order!')


# Short example of using an object notation
st.header('2. Example of object notation')

form = st.form('my_form_2')
selected_val = form.slider('Select a value')
form.form_submit_button('Submit')

st.write('Selected value: ', selected_val)
st.divider()

st.subheader('Day 25: st.session_state')

def lbs_to_kg():
  st.session_state.kg = st.session_state.lbs/2.2046
def kg_to_lbs():
  st.session_state.lbs = st.session_state.kg*2.2046

st.header('Input')
col1, spacer, col2 = st.columns([2,1,2])
with col1:
  pounds = st.number_input("Pounds:", key = "lbs", on_change = lbs_to_kg)
with col2:
  kilogram = st.number_input("Kilograms:", key = "kg", on_change = kg_to_lbs)

st.header('Output')
st.write("st.session_state object:", st.session_state)
st.divider()

st.subheader('Day 26: Building the Bored API App')
st.title('🏀 Bored API app')
st.info('API throwing error. Under investigation.')
#st.sidebar.header('Input')
#selected_type = st.sidebar.selectbox('Select an activity type', ["education", "recreational", "social", "diy", "charity", "cooking", "relaxation", "music", "busywork"])

#suggested_activity_url = f'http://www.boredapi.com/api/activity?type={selected_type}'
#json_data = requests.get(suggested_activity_url)
#suggested_activity = json_data.json()

#c1, c2 = st.columns(2)
#with c1:
#  with st.expander('About this app'):
#    st.write('Are you bored? The **Bored API app** provides suggestions on activities that you can do when you are bored. This app is powered by the Bored API.')
#with c2:
#  with st.expander('JSON data'):
#    st.write(suggested_activity)

#st.header('Suggested activity')
#st.info(suggested_activity['activity'])

#col1, col2, col3 = st.columns(3)
#with col1:
#  st.metric(label='Number of Participants', value=suggested_activity['participants'], delta='')
#with col2:
#  st.metric(label='Type of Activity', value=suggested_activity['type'].capitalize(), delta='')
#with col3:
#  st.metric(label='Price', value=suggested_activity['price'], delta='')
st.divider()

st.subheader('Day 27: Building a draggable and resizable dashboard with Streamlit Elements')
st.markdown('''
First step is to install Streamlit Elements in terminal:
`pip install streamlit-elements==0.1.*`

The goal here is to create a dashboard composed of three material UI cards:
* A first card with a Monaco code editor to input some data
* A second card to display that data in a Nivo Bump chart
* A third card to show a YouTube video URL defined with a `st.text_input`

The data used is from [Nivo Bump demo](https://nivo.rocks/bump/)
''')
import json
from pathlib import Path
from streamlit_elements import elements, dashboard, mui, editor, media, lazy, sync, nivo

st.set_page_config(layout='wide')
st.info('Code throwing error. Under investigation.')
st.divider()

import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
import xgboost
import numpy as np
from streamlit_shap import st_shap
import shap
st.subheader('Day 28: streamlit-shap')

@st.cache_data
def load_data():
    return shap.datasets.adult()

@st.cache_data
def load_model(X, y):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=7)
    d_train = xgboost.DMatrix(X_train, label=y_train)
    d_test = xgboost.DMatrix(X_test, label=y_test)
    params = {
        'eta': 0.01,
        'objective': 'binary:logistic',
        'subsample': 0.5,
        'base_score': np.mean(y_train),
        'eval_metric': 'logloss',
        'n_jobs': -1,
    }
    model = xgboost.train(params, d_train, 10, evals = [(d_test, 'test')], verbose_eval=100, early_stopping_rounds=20)
    return model

st.subheader("`streamlit-shap` for displaying SHAP plots in a Streamlit app")
with st.expander('About the app'):
    st.markdown('''[`streamlit-shap`](https://github.com/snehankekre/streamlit-shap) is a Streamlit component that provides a wrapper to display [SHAP](https://github.com/slundberg/shap) plots in [Streamlit](https://streamlit.io/). 
                    The library is developed by our in-house staff [Snehan Kekre](https://github.com/snehankekre) who also maintains the [Streamlit Documentation](https://docs.streamlit.io/) website.
                ''')

st.subheader('Input data')
X,y = load_data()
X_display,y_display = shap.datasets.adult(display=True)

with st.expander('About the data'):
    st.write('Adult census data is used as the example dataset.')
with st.expander('X'):
    st.dataframe(X)
with st.expander('y'):
    st.dataframe(y)

st.subheader('SHAP output')

model = load_model(X, y)

explainer = shap.Explainer(model, X)
shap_values = explainer(X)

with st.expander('Waterfall plot'):
    st_shap(shap.plots.waterfall(shap_values[0]), height=300)
with st.expander('Beeswarm plot'):
    st_shap(shap.plots.beeswarm(shap_values), height=300)
st.divider()