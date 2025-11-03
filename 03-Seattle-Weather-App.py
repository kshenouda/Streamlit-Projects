# Load libraries
from datetime import datetime
from vega_datasets import data
import streamlit as st
import altair as alt

df = data

# Set Streamlit page config
st.set_page_config(page_title = 'Seattle Weather App', layout = 'wide')
# st.title('Seattle Weather')
# st.write("Let's explore the classic Seattle Weather dataset!")
'''
# Seattle Weather
Let's explore the [classic Seattle Weather dataset](https://altair-viz.github.io/case_studies/exploring-weather.html)
'''

'' # Adds a little vertical space, same as st.write('')
'' 

'''
## 2015 Summary
'''

''

# Load Seattle Weather dataset
full_df = data.seattle_weather()
# st.write(full_df)

# Create subsets of data to filter specific years
df_2015 = full_df[full_df['date'].dt.year == 2015]
df_2014 = full_df[full_df['date'].dt.year == 2014]
df_2013 = full_df[full_df['date'].dt.year == 2013]
df_2012 = full_df[full_df['date'].dt.year == 2012]

# Find min/max precipitation for each year
min_precipitation_2015 = df_2015['precipitation'].min()
min_precipitation_2014 = df_2014['precipitation'].min()
min_precipitation_2013 = df_2013['precipitation'].min()
min_precipitation_2012 = df_2012['precipitation'].min()

max_precipitation_2015 = df_2015['precipitation'].max()
max_precipitation_2014 = df_2014['precipitation'].max()
max_precipitation_2013 = df_2013['precipitation'].max()
max_precipitation_2012 = df_2012['precipitation'].max()

# Find max temp_max for each year
max_temp_2015 = df_2015['temp_max'].max()
max_temp_2014 = df_2014['temp_max'].max()
max_temp_2013 = df_2013['temp_max'].max()
max_temp_2012 = df_2012['temp_max'].max()

# Find min temp_min for each year
min_temp_2015 = df_2015['temp_min'].min()
min_temp_2014 = df_2014['temp_min'].min()
min_temp_2013 = df_2013['temp_min'].min()
min_temp_2012 = df_2012['temp_min'].min()

# Find min/max wind for each year
min_wind_2015 = df_2015['wind'].min()
min_wind_2014 = df_2014['wind'].min()
min_wind_2013 = df_2013['wind'].min()
min_wind_2012 = df_2012['wind'].min()

max_wind_2015 = df_2015['wind'].max()
max_wind_2014 = df_2014['wind'].max()
max_wind_2013 = df_2013['wind'].max()
max_wind_2012 = df_2012['wind'].max()

# Find unique weather conditions
# df_weather = full_df['weather'].unique()

with st.container(horizontal = True, gap = 'medium'):
    cols = st.columns(2, gap = 'medium', width = 300)
    with cols[0]:
        st.metric(
            'Max temperature',
            f'{max_temp_2015:0.1f}C',
            delta = f'{max_temp_2015 - max_temp_2014:0.1f}C',
            width = 'content'
        )
    with cols[1]:
        st.metric(
            'Min temperature',
            f'{min_temp_2015:0.1f}C',
            delta = f'{min_temp_2015 - min_temp_2014:0.1f}C',
            width = 'content'
        )

    cols = st.columns(2, gap = 'medium', width = 300)
    with cols[0]:
        st.metric(
            'Max precipitation',
            f'{max_precipitation_2015:0.1f}C',
            delta = f'{max_precipitation_2015 - max_precipitation_2014:0.1f}C',
            width = 'content'
        )

    with cols[1]:
        st.metric(
            'Min precipitation',
            f'{min_precipitation_2015:0.1f}C',
            delta = f'{min_precipitation_2015 - min_precipitation_2014:0.1f}C',
            width = 'content'
        )

with st.container(horizontal = True, gap = 'medium'):
    cols = st.columns(2, gap = 'medium', width = 300)
    with cols[0]:
        st.metric(
            'Max wind',
            f'{max_wind_2015:0.1f}m/s',
            delta = f'{max_wind_2015 - max_wind_2014:0.1f}m/s',
            width = 'content'
        )
    with cols[1]:
        st.metric(
            'Min wind',
            f'{min_wind_2015:0.1f}m/s',
            delta = f'{min_wind_2015 - min_wind_2014:0.1f}m/s',
            width = 'content'
        )

    cols = st.columns(2, gap = 'medium', width = 300)
    with cols[0]:
        weather_name = (
            full_df['weather'].value_counts().head(1).reset_index()['weather'][0]
        )
        st.metric(
            'Most common weather',
            f'{weather_name.upper()}'
        )
    with cols[1]:
        weather_name = (
            full_df['weather'].value_counts().tail(1).reset_index()['weather'][0]
        )
        st.metric(
            'Least common weather',
            f'{weather_name.upper()}'
        )

''
''

'''
## Compare different years
'''
years = full_df['date'].dt.year.unique()
selected_years = st.pills('Years to compare', years, default = years, selection_mode = 'multi')

if not selected_years:
    st.warning('You must select at least 1 year', icon = ':material/warning:')

df = full_df[full_df['date'].dt.year.isin(selected_years)]

cols = st.columns([3, 1])

with cols[0].container(border = True, height = 'stretch'):
    '#### Temperature'
    st.altair_chart(
        alt.Chart(df).mark_bar(width = 1).encode(
            alt.X('date', timeUnit = 'monthdate').title('Date'),
            alt.Y('temp_max').title('Temperature Range (C)'),
            alt.Y2('temp_min'),
            alt.Color('date:N', timeUnit = 'year').title('year'),
            alt.XOffset('date:N', timeUnit = 'year'),
        ).configure_legend(orient = 'bottom')
    )

with cols[1].container(border = True, height = 'stretch'):
    '#### Weather Distribution'
    st.altair_chart(
        alt.Chart(df).mark_arc().encode(
           alt.Theta('count()'),
           alt.Color('weather:N'),
       ).configure_legend(orient = 'bottom')
    )

cols = st.columns(2)

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
            alt.Y('avg_wind:Q').title('WindAverage Wind Past 2 Weeks (m/s)'),
            alt.Color('date:N', timeUnit = 'year').title('year'),
        ).configure_legend(orient = 'bottom')
    )

with cols[1].container(border = True, height = 'stretch'):
    '#### Precipitation'
    st.altair_chart(
        alt.Chart(df).mark_bar().encode(
            alt.X('date:N', timeUnit = 'month').title('Date'),
            alt.Y('precipitation:Q').aggregate('sum').title('Precipitation (mm)'),
            alt.Color('date:N', timeUnit = 'year').title('year'),
        ).configure_legend(orient = 'bottom')
    )

cols = st.columns(2)

with cols[0].container(border = True, height = 'stretch'):
    '#### Monthly Weather Breakdown'
    st.altair_chart(
        alt.Chart(df).mark_bar().encode(
            alt.X('month(date):O', title = 'month'),
            alt.Y('count():Q', title = 'days').stack('normalize'),
            alt.Color('weather:N'),
        )
    )

with cols[1].container(border = True, height = 'stretch'):
    '#### Raw Data'
    st.dataframe(df)