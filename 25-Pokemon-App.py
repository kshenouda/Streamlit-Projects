import streamlit as st
import pandas as pd
import requests

st.set_page_config(page_title='Pokemon App', layout='wide')
st.title('Pokemon App')
st.markdown('''
Search for a Pokemon by ID or by name to view its stats, types, and physical attributes
''')
st.divider()

with st.sidebar:
    st.header('Search')
    pokemon_name = st.text_input(
        'Enter Pokemon name or ID', 
        placeholder='e.g. Pikachu or 25')

@st.cache_data(show_spinner=False)
def get_data(name: str):
    url = f'https://pokeapi.co/api/v2/pokemon/{name}' # total IDs: 1025
    response = requests.get(url, timeout=10)
    if response.status_code != 200:
        return None
    return response.json()

if pokemon_name:
    cleaned_name = pokemon_name.strip().lower()

    with st.spinner('Fetching Pokemon data'):
        data = get_data(cleaned_name)
    if data is None:
        st.error('Pokemon not found. Please check the name or ID and try again')
    else:
        col1, col2 = st.columns(2)
        with col1:
            # Name and image
            st.header(data['name'].title())
            sprite = data['sprites']['front_default']
            if sprite:
                st.image(sprite, width=220)
            # Types
            types = [t['type']['name'].title() for t in data['types']]
            st.markdown('**Type(s):** ' + ', '.join(types))
        with col2:
            # Stats
            stats_df = pd.DataFrame(
                [
                    {
                        'Stat': stat['stat']['name'].title(),
                        'Value': stat['base_stat']
                    }
                    for stat in data['stats']
                ]
            ).set_index('Stat')
            st.subheader('Base Stats')
            st.bar_chart(stats_df)
        st.divider()
        # Physical attributes
        st.subheader('Physical Attributes')
        col1, col2 = st.columns(2)
        col1.metric('Height', f'{data["height"]/10} m')
        col2.metric('Weight', f'{data["weight"]/10} kg')
        # st.write(data)
else:
    st.info('Enter a Pokemon name/ID in the sidebar to get started')


#try:
#    response = requests.get(url, timeout=10)
#    response.raise_for_status()
#    data = response.json()
#    df = pd.DataFrame(data)
#    st.write(df)
#    st.write(data)
#except requests.exceptions.RequestException as e:
#    st.error(f'Failed to fetch current price {e}')