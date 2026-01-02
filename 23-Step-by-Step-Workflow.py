import streamlit as st

st.set_page_config(page_title='Step by Step Workflow', layout='wide')
st.title('Step by Step Workflow')

if 'step' not in st.session_state:
    st.session_state.step = 1
if 'name' not in st.session_state:
    st.session_state.name = ''
if 'choice' not in st.session_state:
    st.session_state.choice = ''
if 'email' not in st.session_state:
    st.session_state.email = ''

def next_step():
    st.session_state.step += 1

def restart():
    st.session_state.step = 1
    st.session_state.name = ''
    st.session_state.choice = ''

if st.session_state.step == 1:
    st.write('Step 1: Enter your name')
    st.text_input('Name', value=st.session_state.name, key='name')
    st.button('Next', on_click=next_step)

elif st.session_state.step == 2:
    st.write(f'Hello {st.session_state.name} Step 2: Choose your preference')
    st.radio('Choose a restaurant', options=['Chipotle', 'Moes'],key='choice')
    st.button('Next', on_click=next_step)

elif st.session_state.step == 3:
    st.write(f'You selected {st.session_state.choice}')
    st.button('Restart', on_click=restart)