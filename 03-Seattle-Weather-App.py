# Load libraries
from datetime import datetime
from vega_datasets import data
import streamlit as st
import altair as alt

# Set Streamlit page config
st.set_page_config(page_title = 'Seattle Weather App', layout = 'wide')
st.title('Seattle Weather')
st.markdown('''
Let's explore the [classic Seattle Weather dataset](https://altair-viz.github.io/case_studies/exploring-weather.html)
from the Vega Altair Datasets package.
''')

pages = [
    'Overview',
    'Year Comparison',
    'Raw Data'
]
st.sidebar.subheader('Page Navigation')
page_options = st.sidebar.radio('Go to', pages)

@st.cache_data
def load_weather_data():
    return data.seattle_weather()

full_df = load_weather_data()

@st.cache_data
def yearly_metrics_with_deltas(df, year):
    year_df = df[df['date'].dt.year == year]
    prev_df = df[df['date'].dt.year == year - 1]
    
    metrics = {
        'max_temp': year_df['temp_max'].max(),
        'min_temp': year_df['temp_min'].min(),        
        'max_precip': year_df['precipitation'].max(),
        'min_precip': year_df['precipitation'].min(),
        'max_wind': year_df['wind'].max(),
        'min_wind': year_df['wind'].min(),
        'most_weather': year_df['weather'].value_counts().head(1).reset_index()['weather'][0].upper(),
        'least_weather': year_df['weather'].value_counts().tail(1).reset_index()['weather'][0].upper()
    }

    if prev_df.empty:
        deltas = {
            'max_temp': None,
            'min_temp': None,
            'max_precip': None,
            'min_precip': None,
            'max_wind': None,
            'min_wind': None,

        }
    else:
        deltas = {
            'max_temp': metrics['max_temp'] - prev_df['temp_max'].max(),
            'min_temp': metrics['min_temp'] - prev_df['temp_min'].min(),
            'max_precip': metrics['max_precip'] - prev_df['precipitation'].max(),
            'min_precip': metrics['min_precip'] - prev_df['precipitation'].min(),
            'max_wind': metrics['max_wind'] - prev_df['wind'].max(),
            'min_wind': metrics['min_wind'] - prev_df['wind'].min()
        }

    return metrics, deltas

selected_year = st.selectbox(
    'Select year for summary',
    sorted(full_df['date'].dt.year.unique(), reverse=True)
)
prev_year = selected_year - 1
st.divider()

def render_overview(df, year):
    # metrics = yearly_metrics(full_df, selected_year)
    metrics, deltas = yearly_metrics_with_deltas(full_df, selected_year)
    st.subheader(f'{selected_year} Overview')

    if deltas is None:
        st.info("Year-over-year comparisons are not available for the first year in the dataset.")

    with st.container(horizontal = True, gap = 'medium'):
        cols = st.columns(4)
        # cols = st.columns(2, gap = 'medium', width = 300)
        with cols[0]:
            st.metric('Max temperature',
                f"{metrics['max_temp']:0.1f}C",
                # delta = f"{metrics['max_temp'] - max_temp_2014:0.1f}C",
                delta = round(deltas['max_temp'], 2),
                width = 'content'
            )
        with cols[1]:
            st.metric('Min temperature', 
                      f"{metrics['min_temp']:0.1f}C",
                      delta = round(metrics['min_temp'], 2),
                      width = 'content'
            )
        with cols[2]:
            st.metric('Max preciptation',
                f"{metrics['max_precip']:0.1f}mm",
                delta = round(deltas['max_precip'], 2),
                width = 'content'
            )
        with cols[3]:
            st.metric('Min preciptation', 
                      f"{metrics['min_precip']:0.1f}mm",
                      delta = round(metrics['min_precip'], 2),
                      width = 'content'
            )
        with cols[0]:
            st.metric('Max wind',
                      f"{metrics['max_wind']:0.1f}m/s",
                      delta = round(metrics['max_wind'], 2),
                      width = 'content')
        with cols[1]:
            st.metric('Min wind',
                      f"{metrics['min_wind']:0.1f}m/s",
                      delta = round(metrics['min_wind'], 2),
                      width = 'content')
        with cols[2]:
            st.metric('Most common weather',
                      metrics['most_weather'],
                      width = 'content')
        with cols[3]:
            st.metric('Least common weather',
                      metrics['least_weather'],
                      width = 'content')

def render_yearly_comparison(df):
    years = sorted(df['date'].dt.year.unique())
    selected_year = st.pills('Years to compare', years, default = years, selection_mode = 'multi')
    if not selected_year:
        st.warning('You must select at least 1 year', icon = ':material/warning:')

    df = df[df['date'].dt.year.isin(selected_year)]

    cols = st.columns(1)

    with cols[0].container(border = True, height = 'stretch'):
        '#### Temperature'
        st.altair_chart(
            alt.Chart(df).mark_bar(width = 1).encode(
                # alt.X('date', timeUnit = 'monthdate').title('Date'),
                alt.X('month(date):O', title='Month'),
                # alt.Y('temp_max').title('Temperature Range (C)'),
                alt.Y('mean(temp_max):Q', title='Avg Max Temp (C)'),
                # alt.Y2('temp_min'),
                alt.Y2('mean(temp_min):Q'),
                # alt.Color('date:N', timeUnit = 'year').title('year'),
                alt.Color('year(date):N', title='Year'),
                alt.XOffset('year(date):N'),
                tooltip=[
                    alt.Tooltip('year(date):N', title='Year'),
                    alt.Tooltip('mean(temp_max):Q', title='Avg Max Temp', format='.1f'),
                    alt.Tooltip('mean(temp_min):Q', title='Avg Min Temp', format='.1f')
                ]
            ).configure_legend(orient = 'bottom')
        )

    with cols[0].container(border = True, height = 'stretch'):
        '#### Wind'
        st.altair_chart(
            alt.Chart(df).transform_window(
                avg_wind = 'mean(wind)',
                std_wind = 'stdev(wind)',
                frame = [0,14],
                groupby=['monthdate(date)']
            ).mark_line(size = 1).encode(
                alt.X('date', timeUnit = 'monthdate').title('Date'),
                alt.Y('avg_wind:Q').title('Avg Wind (m/s, rolling 14 days)'),
                # alt.Color('date:N', timeUnit = 'year').title('year'),
                alt.Color('year(date):N', title='Year'),
            ).configure_legend(orient = 'bottom')
        )

    with cols[0].container(border = True, height = 'stretch'):
        '#### Precipitation'
        st.altair_chart(
            alt.Chart(df).mark_bar().encode(
                # alt.X('date:N', timeUnit = 'month').title('Date'),
                alt.X('month(date):O'),
                alt.Y('precipitation:Q').aggregate('sum').title('Precipitation (mm)'),
                # alt.Color('date:N', timeUnit = 'year').title('year'),
                alt.Color('year(date):N', title='Year'),
            ).configure_legend(orient = 'bottom')
        )
    
    with cols[0].container(border = True, height = 'stretch'):
        '#### Monthly Weather Breakdown'
        st.altair_chart(
            alt.Chart(df).mark_bar().encode(
                alt.X('month(date):O', title = 'month'),
                alt.Y('count():Q', title = 'days').stack('normalize'),
                alt.Color('weather:N'),
                tooltip=['weather', 'count()']
            )
    )

if page_options == 'Overview':
    if selected_year:
        render_overview(full_df, selected_year)

if page_options == 'Year Comparison':
    if selected_year:
        render_yearly_comparison(full_df)

if page_options == 'Raw Data':
    years = st.multiselect(
        'Filter years',
        sorted(full_df['date'].dt.year.unique()),
        default=sorted(full_df['date'].dt.year.unique())
    )
    filtered_df = (full_df[full_df['date'].dt.year.isin(years)])
    st.dataframe(filtered_df)
    st.caption(f'Returned rows: {len(filtered_df)}')