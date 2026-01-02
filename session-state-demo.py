import streamlit as st

st.set_page_config(page_title='Session State Demo', layout='centered')
st.title('Session State Demo')

if 'counter' not in st.session_state:
    st.session_state.counter = 0

col1, col2 = st.columns(2)
with col1:
    if st.button('Increment'):
        st.session_state.counter += 1

with col2:
    if st.button('Decrement'):
        st.session_state.counter -= 1

st.write('Counter value: ', str(st.session_state.counter))
st.divider()
####################################################################
if 'name' not in st.session_state:
    st.session_state.name = 'Guest'

name_input = st.text_input('Enter your name', st.session_state.name)

if name_input != st.session_state.name:
    st.session_state.name = name_input

st.write('Hello, ', st.session_state.name)
st.divider()
####################################################################
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    if st.button('Login'):
        st.session_state.logged_in = True
        st.success('You are now logged in!')
else:
    st.write('Welcome back!')
    if st.button('Logout'):
        st.session_state.logged_in = False
    

st.write('Logged in? ', st.session_state.logged_in)