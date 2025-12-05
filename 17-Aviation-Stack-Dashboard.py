import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import requests
import datetime
import os

st.set_page_config(page_title='Aviation Stack Dashboard', layout='wide')
st.title('Aviation Stack Dashboard')
st.write('''
This dashboard explores data from the Aviation Stack API. This API provides real-time 
and historical data on flights, airlines, airports, and more. You can explore various 
aspects of aviation data, including flight status, airline information, and airport details.
''')

st.divider()

url = 'https://api.aviationstack.com/v1/'
# api_key = st.secrets['AVIATIONSTACK_API_KEY']
api_key = '04360d2c8eff0da265c69169b6e68b87'
#endpoints = [
#    'flights', 
#    'routes', 
#    'airports', 
#    'airlines', 
#    'airplanes',
#    'aircraft_types',
#    'aviation_taxes',
#    'cities',
#    'countries',
#    'flight_schedules',
#    'future_flight_schedules'
#]
endpoints = [
    'airlines',
    'airplanes',
    'countries'
]
selected_endpoint = st.sidebar.selectbox('Select Endpoint', 
                                         sorted(endpoints),
                                         index=None)
if selected_endpoint:
    st.subheader(f'Selected Endpoint: {selected_endpoint.capitalize().replace("_", " ")}')
else:
    st.info('Select an endpoint from the sidebar to load data.')
    st.stop()

@st.cache_data(ttl=datetime.timedelta(hours=24))
def fetch_data(selected_endpoint):
    response = requests.get(f'{url}{selected_endpoint}?access_key={api_key}&limit=2000')
    data = response.json()

    if 'error' in data:
        st.error(f"API Error: {data['error']['message']}")
        st.stop()

    if response.status_code != 200:
        st.error(f'HTTP {response.status_code}: Unable to fetch data')
        st.stop()

    return pd.json_normalize(data['data'])

with st.spinner('Fetching data...'):
    df = fetch_data(selected_endpoint)
if df.empty:
    st.warning('No data available for the selected endpoint')
    st.stop()
else:
    st.dataframe(df.head(10))

st.write(f'Total records fetched: {len(df)}')
st.caption(f'Dataset limited to {len(df)} records for demonstration purposes.')
st.divider()




if selected_endpoint == 'airlines':
    st.subheader('Airline Information Analysis')
    st.write('This section provides insights into the airline data fetched from the Aviation Stack API.')
    df = df.dropna(subset=['fleet_size', 'fleet_average_age', 'date_founded'])
    
    df['date_founded'] = pd.to_datetime(df['date_founded'], errors='coerce').dt.year
    df['country_name'] = df['country_name'].fillna('Unknown')
    df['fleet_average_age'] = pd.to_numeric(df['fleet_average_age'], errors='coerce')
    df['fleet_size'] = pd.to_numeric(df['fleet_size'], errors='coerce')
    df['status'] = df['status'].fillna('Unknown')
    smallest_fleet_size = df['fleet_size'].min()
    largest_fleet_size = df['fleet_size'].max()
    average_fleet_size = df['fleet_size'].mean().round(2)
    youngest_average_fleet = df['fleet_average_age'].min()
    oldest_average_fleet = df['fleet_average_age'].max()
    average_average_fleet = df['fleet_average_age'].mean().round(2)
    earliest_date_founded = df['date_founded'].min()
    latest_date_founded = df['date_founded'].max()
    first_airline = df.loc[df['date_founded'] == earliest_date_founded, 'airline_name'].values[0]
    latest_airline = df.loc[df['date_founded'] == latest_date_founded, 'airline_name'].values[0]
    country_with_most_airlines = df['country_name'].value_counts().head(1)
    country_with_least_airlines = df['country_name'].value_counts().tail(1)
    china_avg_fleet_size = df.loc[df['country_name'] == 'China', 'fleet_size'].mean().round(2)
    china_avg_fleet_age = df.loc[df['country_name'] == 'China', 'fleet_average_age'].mean().round(2)
    us_number_of_airlines = df.loc[df['country_name'] == 'United States', :].shape[0]
    us_average_fleet_size = df.loc[df['country_name'] == 'United States', 'fleet_size'].mean().round(2)
    us_average_fleet_age = df.loc[df['country_name'] == 'United States', 'fleet_average_age'].mean().round(2)
    active_airlines = df[df['status'] == 'active'].shape[0]
    disabled_airlines = df[df['status'] == 'disabled'].shape[0]
    historical_airlines = df[df['status'] == 'historical'].shape[0]
    most_common_airline_type = df[df['type'].notnull()]['type'].mode()[0]

    st.sidebar.header('Filter Options')
    country_filter = st.sidebar.multiselect(
        'Country', options = sorted(df['country_name'].dropna().unique()),
        default = None
    )
    status_filter = st.sidebar.multiselect(
        'Status', options = sorted(df['status'].dropna().unique()),
        default = None
    )
    type_filter = st.sidebar.multiselect(
        'Type', options = sorted(df['type'].dropna().unique()),
        default = None
    )
    date_filter = st.sidebar.slider(
        'Date Founded Range',
        min_value=df['date_founded'].min(),
        max_value=df['date_founded'].max(),
        value=(df['date_founded'].min(), df['date_founded'].max())
    )

    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        'Fleet Age and Size', 
        'Date Founded', 
        'Airline Countries',
        'Airline Statuses and Types',
        'Filtered Data'
    ])
    with tab1:
        col1, col2, col3 = st.columns(3)
        col1.metric('Smallest Fleet Size', smallest_fleet_size)
        col2.metric('Largest Fleet Size', largest_fleet_size)
        col3.metric('Average Fleet Size', average_fleet_size)
        col1.metric('Youngest Average Fleet Age', f'{youngest_average_fleet} yrs')
        col2.metric('Oldest Average Fleet Age', f'{oldest_average_fleet} yrs')
        col3.metric('Average Fleet Age', f'{average_average_fleet} yrs')
    with tab2:
        col1, col2 = st.columns(2)
        col1.metric('Earliest Date Founded', earliest_date_founded)
        col2.metric('Latest Date Founded', latest_date_founded)
        col1.metric('First Airline', first_airline)
        col2.metric('Latest Airline', latest_airline)
    with tab3:
        col1, col2, col3 = st.columns(3)
        col1.metric('Country with Most Airlines', 
                    country_with_most_airlines.index[0],
                    delta=country_with_most_airlines.values[0])
        col2.metric("China's Average Fleet Size",
                    china_avg_fleet_size)
        col3.metric("China's Average Fleet Age",
                    f'{china_avg_fleet_age} yrs')
        col1.metric('United States Number of Airlines',
                    us_number_of_airlines)
        col2.metric('United States Average Fleet Size',
                    us_average_fleet_size,
                    delta=us_average_fleet_size-china_avg_fleet_size)
        col3.metric('United States Average Fleet Age',
                    f'{us_average_fleet_age} yrs',
                    delta=us_average_fleet_age-china_avg_fleet_age,
                    delta_color='inverse')
    with tab4:
        col1, col2, col3 = st.columns(3)
        col1.metric('Active Airlines', active_airlines)
        col2.metric('Disabled Airlines', disabled_airlines)
        col3.metric('Historical/Defunct Airlines', historical_airlines)
        col1.metric('Most Common Airline Type', most_common_airline_type,
                    delta=df['type'].value_counts().loc[most_common_airline_type])
    with tab5:
        filtered_df = df.copy()
        if country_filter:
            filtered_df = filtered_df[filtered_df['country_name'].isin(country_filter)]
        if status_filter:
            filtered_df = filtered_df[filtered_df['status'].isin(status_filter)]
        if type_filter:
            filtered_df = filtered_df[filtered_df['type'].isin(type_filter)]
        if date_filter:
            filtered_df = filtered_df[filtered_df['date_founded'].between(int(date_filter[0]), int(date_filter[1]))]
        st.dataframe(filtered_df)
        st.write(f'Total records after filtering: {len(filtered_df)}')
        st.caption('NA values have been removed for calculations and display purposes.')

    st.divider()

    st.subheader('Visualizations')
    tab1, tab2 = st.tabs(['Airlines by Country', 'Fleet Size vs. Fleet Age'])
    with tab1:
        fig1 = px.bar(df['country_name'].value_counts(),
                        title='Number of Airlines by Country')
        fig1.update_layout(xaxis_title='Country', 
                           yaxis_title='# of Airlines',
                           showlegend=False)
        st.plotly_chart(fig1, use_container_width=True)
    with tab2:
        fig2 = px.scatter(df, x='fleet_size', y='fleet_average_age',
                          hover_data=['airline_name', 'country_name'],
                          title='Fleet Size vs. Fleet Average Age')
        fig2.update_layout(xaxis_title='Fleet Size', 
                           yaxis_title='Fleet Average Age (years)',
                           showlegend=False)
        st.plotly_chart(fig2, use_container_width=True)




if selected_endpoint == 'airplanes':
    st.subheader('Airplane Information Analysis')
    st.write('This section provides insights into the airplane data fetched from the Aviation Stack API.')
    
    df['delivery_date'] = pd.to_datetime(df['delivery_date'], errors='coerce')
    df['first_flight_date'] = pd.to_datetime(df['first_flight_date'], errors='coerce')
    df['registration_date'] = pd.to_datetime(df['registration_date'], errors='coerce')
    df['rollout_date'] = pd.to_datetime(df['rollout_date'], errors='coerce')
    df['engines_count'] = pd.to_numeric(df['engines_count'], errors='coerce')
    df['plane_age'] = pd.to_numeric(df['plane_age'], errors='coerce')
    first_plane_delivered = df['delivery_date'].min().date()
    latest_plane_delivered = df['delivery_date'].max().date()
    first_registered_plane = df['registration_date'].min().date()
    latest_registered_plane = df['registration_date'].max().date()
    first_rollout_date = df['rollout_date'].min().date()
    latest_rollout_date = df['rollout_date'].max().date()
    min_plane_age = df['plane_age'].min()
    max_plane_age = df['plane_age'].max()
    avg_plane_age = df['plane_age'].mean().round(2)
    total_active_planes = df[df['plane_status'] == 'active'].shape[0]
    total_inactive_planes = df[df['plane_status'] == 'inactive'].shape[0]
    unique_plane_owners = df['plane_owner'].nunique()
    plane_owner_with_most_planes = df['plane_owner'].value_counts().head(1)
    unique_plane_models = df['model_name'].nunique()
    unique_plane_series = df['plane_series'].nunique()
    unique_production_lines = df['production_line'].nunique()

    st.sidebar.header('Filter Options')
    engines_count_filter = st.sidebar.multiselect(
        'Engines Count', options = sorted(df['engines_count'].dropna().unique()),
        default=None, key='engines_count_filter'
    )
    engines_type_filter = st.sidebar.multiselect(
        'Engines Type', options = sorted(df['engines_type'].dropna().unique()),
        default=None, key='engines_type_filter' 
    )
    model_name_filter = st.sidebar.multiselect(
        'Model Name', options = sorted(df['model_name'].dropna().unique()),
        default=None, key='model_name_filter'
    )
    plane_owner_filter = st.sidebar.multiselect(
        'Plane Owner', options = sorted(df['plane_owner'].dropna().unique()),
        default=None, key='plane_owner_filter'
    )
    plane_series_filter = st.sidebar.multiselect(
        'Plane Series', options = sorted(df['plane_series'].dropna().unique()),
        default=None, key='plane_series_filter'
    )
    plane_status_filter = st.sidebar.multiselect(
        'Plane Status', options = sorted(df['plane_status'].dropna().unique()),
        default=None, key='plane_status_filter'
    )
    production_line_filter = st.sidebar.multiselect(
        'Production Line', options = sorted(df['production_line'].dropna().unique()),
        default=None, key='production_line_filter'
    )
    
    tab1, tab2, tab3, tab4 = st.tabs(['Key Metrics', 'Plane Details', 'Visualizations', 'Filtered Data'])
    with tab1:
        col1, col2, col3 = st.columns(3)
        col1.metric('Active Planes', total_active_planes)
        col2.metric('Inactive Planes', total_inactive_planes)
        col3.metric('Unique Plane Owners', unique_plane_owners)
        col1.metric('Unique Plane Models', unique_plane_models)
        col2.metric('Unique Plane Series', unique_plane_series)
        col3.metric('Unique Production Lines', unique_production_lines)
    with tab2:
        col1, col2, col3 = st.columns(3)
        col1.metric('Minimum Plane Age', f'{min_plane_age} yrs')
        col2.metric('Maximum Plane Age', f'{max_plane_age} yrs')
        col3.metric('Average Plane Age', f'{avg_plane_age} yrs')
        col1.metric('Plane Owner with Most Planes', plane_owner_with_most_planes.index[0],
                    delta=plane_owner_with_most_planes.values[0])
        col2.metric('Production Line with Most Planes', df['production_line'].value_counts().idxmax(),
                    delta=df['production_line'].value_counts().max())
        col3.metric('Most Common Engine Type', df['engines_type'].value_counts().idxmax(),
                    delta=df['engines_type'].value_counts().max())
    with tab3:
        col1, col2 = st.columns(2)
        with col1:
            fig1 = px.histogram(df, x='delivery_date', nbins=80,
                                title='Distribution of Plane Delivery Dates')
            fig1.update_layout(xaxis_title='Delivery Date', 
                            yaxis_title='# of Planes',
                            showlegend=False)
            st.plotly_chart(fig1, use_container_width=True)
        with col2:
            fig2 = px.bar(df['plane_owner'].value_counts().head(10),
                          title='Top 10 Plane Owners')
            fig2.update_layout(xaxis_title='Plane Owner',
                               yaxis_title='# of Planes',
                               showlegend=False)
            st.plotly_chart(fig2, use_container_width=True)
    with tab4:
        filtered_df = df.copy()
        if engines_count_filter:
            filtered_df = filtered_df[filtered_df['engines_count'].isin(engines_count_filter)]
        if engines_type_filter:
            filtered_df = filtered_df[filtered_df['engines_type'].isin(engines_type_filter)]
        if model_name_filter:
            filtered_df = filtered_df[filtered_df['model_name'].isin(model_name_filter)]
        if plane_owner_filter:
            filtered_df = filtered_df[filtered_df['plane_owner'].isin(plane_owner_filter)]
        if plane_series_filter:
            filtered_df = filtered_df[filtered_df['plane_series'].isin(plane_series_filter)]
        if plane_status_filter:
            filtered_df = filtered_df[filtered_df['plane_status'].isin(plane_status_filter)]
        if production_line_filter:
            filtered_df = filtered_df[filtered_df['production_line'].isin(production_line_filter)]
        st.dataframe(filtered_df)
        st.write(f'Total records after filtering: {len(filtered_df)}')


st.markdown('---')
st.caption('Data provided by AviationStack API. Dashboard built with Streamlit.')