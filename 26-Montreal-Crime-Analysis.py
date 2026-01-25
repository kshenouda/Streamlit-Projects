import streamlit as st
import pandas as pd
# import plotly.express as px
import altair as alt
import json

st.set_page_config(page_title='Montreal Crime Analysis App', layout='wide')
st.title('Montreal Crime Analysis')

uploaded_file = st.sidebar.file_uploader('Upload the crimes dataset', type='csv')

if uploaded_file is None:
    st.info('Please upload the CSV file from the sidebar to begin')
    st.stop()
df = pd.read_csv(uploaded_file)

page_options = [
    'Home/Raw Data',
    'Column Analysis',
    'Top Three Crimes',
    'Part of Day with Most Incidents',
    'Top PDQ with Most/Fewest Complaints',
    'Time-Based Incident Analysis',
    'Crime Map'
]
pages = st.sidebar.radio('Pages', page_options)

@st.cache_data
def clean_data(df):
    df = df.copy()
    df['DATE'] = pd.to_datetime(df['DATE'], errors='coerce')
    df['MONTH'] = df['DATE'].dt.month #.astype('object')
    df['DAY'] = df['DATE'].dt.day #.astype('object')
    df['YEAR'] = df['DATE'].dt.year #.astype('object')
    return df
df2 = clean_data(df)

df3 = df2.rename(columns = {
    'CATEGORIE': 'CATEGORY',
    'QUART': 'TIME_OF_DAY',
    'PDQ': 'POLICE_PRECINCT_NUM',
    'LONGITUDE': 'LON',
    'LATITUDE': 'LAT'
})

@st.cache_data
def rename_values(df):
    df = df.copy()
    df['CATEGORY'] = df['CATEGORY'].replace('Introduction', 'Breaking and Entering')
    df['CATEGORY'] = df['CATEGORY'].replace('Vol dans / sur véhicule à moteur', 'Theft from/to a motor vehicle')
    df['CATEGORY'] = df['CATEGORY'].replace('Vol de véhicule à moteur', 'Theft, Motor Vehicle')
    df['CATEGORY'] = df['CATEGORY'].replace('Méfait', 'Mischief')
    df['CATEGORY'] = df['CATEGORY'].replace('Vols qualifiés', 'Robbery')
    df['CATEGORY'] = df['CATEGORY'].replace('Infractions entrainant la mort', 'Murder')
    df['TIME_OF_DAY'] = df['TIME_OF_DAY'].replace('jour', 'Day')
    df['TIME_OF_DAY'] = df['TIME_OF_DAY'].replace('soir', 'Evening')
    df['TIME_OF_DAY'] = df['TIME_OF_DAY'].replace('nuit', 'Night')
    return df

df4 = rename_values(df3)

selected_years = st.sidebar.multiselect(
    'Filter by year',
    sorted(df4['YEAR'].unique()),
    default=sorted(df4['YEAR'].unique())
)
filtered_df = df4[df4['YEAR'].isin(selected_years)]

if pages == 'Home/Raw Data':
    st.markdown('''
    **Assignment**: Analyze the crime data from Canada's Open Government portal
    to draw conclusions on the distribution and nature of crime in Montreal City.
    In this analysis, we'll include maps that visualize the location of
    different incidents globally and in relation to police districts.
    My analysis may also provide answers to the following questions:
    1. What are the top 3 prevalent crimes or offenses committed in Montreal?
    2. What part of the day did most crime incidents occur?
    3. Which top 5 police precincts (PDQ) got the most crime complaints?
    4. Which are the top 3 PDQs that got the least crime complaints?
    5. Which neighborhoods recorded the highest crime incidents and what are the crime types in those neighborhoods?
    6. Which neighborhood has the most cases of murder?

    **Source**: [Government of Canada Open Data](https://open.canada.ca/data/en/dataset/5829b5b0-ea6f-476f-be94-bc2b8797769a/resource/82ee07b0-ef6f-43fb-9844-3980e72811ec)
    ''')
    st.divider()
    st.subheader(f'Raw Dataset for File Name: {uploaded_file.name}')
    if uploaded_file is None:
        st.info('Use the sidebar on the left to upload the file')
    else:
        st.dataframe(df)
        st.caption(f'Number of rows: {len(df):,}')
        st.caption(f'Number of columns: {len(df.columns)}')   

if pages == 'Column Analysis':
    tab1, tab2, tab3, tab4 = st.tabs([
        'Column Translations', 
        'Column Data Types',
        'Column Renaming',
        'Categorical Value Renaming'
    ])
    with tab1:
        st.subheader('Column Translations/Definitions')
        st.markdown('''
        Since the column names are in French, below are their translations
        and relevance to the dataset:
        ''')
        with st.expander('View column information'):
            st.markdown('''
            **CATEGORIE**: nature/category of the event which include:
            * Introduction: breaking and entering into public/private property, theft of a firearm from a residence
            * Vol dans / sur véhicule à moteur: theft from/to a motor vehicle, theft of the contents of a motor vehicle (car, truck, bike, etc.) or of a vehicle part (wheel, bumper, etc.)
            * Vol de véhicule à moteur: theft of a motor vehicle
            * Méfait: mischief (e.g. graffiti, damage to property or vehicles)
            * Vol qualifié: robbery
            * Infraction entraînant la mort: murder resulting in death
            
            **QUART**: time of day the event was reported to the SPVM:

            * jour: day between 8:01am and 4:00pm
            * soir: evening between 4:01pm and midnight
            * nuit: night between 0:01am and 8:00am
            
            **PDQ**: number of the police precinct covering the territory where the event took place
            
            **X** and **Y**: geospatial position in MTM8 projection (SRID 2950)
            ''')
    with tab2:
        st.subheader('Column Data Types')
        st.write(pd.DataFrame({
                'Column Name': df.columns,
                'Data Type': df.dtypes
        }))
        st.markdown('''
        Some of the columns in the dataset need to be reformatted to
        another data type, like the date and geospatial coordinates.
        
        For example, to update the date column, we can do so using this code:
        ''')
        st.code("df['DATE'] = pd.to_datetime(df['DATE'], errors='coerce').dt.date")
        st.markdown('''
        After creating a function to convert the date column from an
        object to a date type, the updated column types should be:
        ''')
        st.write(pd.DataFrame({
                'Column Name': df2.columns,
                'Data Type': df2.dtypes
        }))
        st.markdown('''
        I've also created a column for the month, day, and year for further
        analysis.
        ''')
    with tab3:
        st.subheader('Renaming Columns')
        st.markdown('''
        To make our analysis more clear, we'll translate the column names,
        which are in French, to English
        We created a function to replace the French names with English,
        so the columns should look like this:
        ''')
        st.dataframe(pd.DataFrame(df3))
    with tab4:
        st.subheader('Renaming Values in Dataset')
        st.markdown('''
        Now that the columns have been renamed from French to English, we can do 
        the same with the categorical values within the dataset.
        Creating another function to translate the values from French
        to English results in the following dataset:
        ''')
        st.dataframe(pd.DataFrame(df4))

if pages == 'Top Three Crimes':
    st.subheader('Top Three Crimes in Montreal')
    st.markdown('''
    Let's start by looking what kind of incidents are included in the dataset:
    ''')
    st.dataframe(filtered_df['CATEGORY'].unique())
    st.markdown('''
    We can see how many instances of each incident occurred using the value_counts function:
    ''')
    st.code("df['CATEGORY'].value_counts()")
    with st.expander('View incident counts:'):
        st.dataframe(filtered_df['CATEGORY'].value_counts())
    top_crimes = filtered_df['CATEGORY'].value_counts().head(3)
    st.markdown('''
    We can see that the top three crimes occurring in Montreal are:
    ''')
    for crime, count in top_crimes.items():
        st.write(f'- {crime}: {count:,} incidents')


if pages == 'Part of Day with Most Incidents':
    st.subheader('Part of Day with Most Crime Incidents')
    st.markdown('''
    Let's confirm that there are only three parts of the day:
    ''')
    st.dataframe(filtered_df['TIME_OF_DAY'].unique())
    st.markdown('''
    Let's measure how many incidents occurred throughout the day
    using the same value_counts function as before to measure
    number of instances per incident
    ''')
    st.dataframe(filtered_df['TIME_OF_DAY'].value_counts())
    st.markdown('''
    We can see that most incidents occur:
    * During the Day time with 173,825 incidents (which is between 8:01am and 4:00pm)
    
    To see a reference of the what times of the day each part of the day
    lands on, go to the Column Translations tab in the Column Analysis page.
    ''')

if pages == 'Top PDQ with Most/Fewest Complaints':
    st.subheader('Top Five Police Precincts with the Most Crime Complaints')
    st.markdown('''
    Let's start by seeing what police precincts are available in the dataset,
    as well as the number of complaints per precinct:''')
    st.dataframe(filtered_df['POLICE_PRECINCT_NUM'].value_counts())
    st.markdown('''
    It looks like the top five police precincts with the most complaints are:
    1. 38th Precinct with 24,726 complaints
    2. 21st Precinct with 22,631 complaints
    3. 20th Precinct with 19,814 complaints
    4. 48th Precinct with 15,996 complaints
    5. 26th Precinct with 15,680 complaints
    
    On the other hand, the top three precincts with the fewest complaints are:
    1. 55th Precinct with 141 complaints
    2. 24th Precinct with 2,532 complaints
    3. 50th Precinct with 2,661 complaints
    
    We'll use the coordinates in the table to visualize where these
    precincts are later on.
    ''')

if pages == 'Time-Based Incident Analysis':
    st.subheader('Incidents by Month, Day, and Year')
    st.markdown('''
    Since we created a column for Month, Day, and Year based on the given
    Date column, we can look at how many incidents occur in each category,
    the most common incident occurred, etc.

    Let's start by seeing how many incidents occurred by Month:
    ''')
    filtered_df['MONTH_NAME'] = pd.to_datetime(filtered_df['MONTH'], format='%m').dt.month_name()
    monthly_counts = (filtered_df.groupby('MONTH').size().reset_index(name='monthly_incident_count'))
    monthly_chart = (alt.Chart(monthly_counts).mark_bar().encode(
        x = alt.X('MONTH:O', title = 'Month', sort=list(range(1, 13))),
        y = alt.Y('monthly_incident_count:Q', title = 'Number of Incidents'),
        tooltip = ['MONTH', 'monthly_incident_count']
    ))
    st.altair_chart(monthly_chart, use_container_width=True)
    st.markdown('''
    October had the most incidents with 31,971 and February had the 
    fewest incidents with 23,069.

    Next, we'll look at the number of incidents per Day:
    ''')
    daily_counts = (filtered_df.groupby('DAY').size().reset_index(name='daily_incident_count'))
    daily_chart = (alt.Chart(daily_counts).mark_bar().encode(
        x = alt.X('DAY:O', title = 'Day', sort=list(range(1,32))),
        y = alt.Y('daily_incident_count:Q', title = 'Number of Incidents'),
        tooltip = ['DAY', 'daily_incident_count']
    ))
    st.altair_chart(daily_chart, use_container_width=True)
    st.markdown('''
    The 17th day had the most incidents with 11,558, and the 31st day had the fewest
    incidents with 6,200. Because half of the months of the year only have 30 days
    and not 31, the day with the second-fewest incidents is the 30th with 9,899.

    Finally, let's look at the number of incidents per Year:
    ''')
    yearly_counts = (filtered_df.groupby('YEAR').size().reset_index(name='yearly_incident_count'))
    yearly_chart = (alt.Chart(yearly_counts).mark_bar().encode(
        x = alt.X('YEAR:O', title = 'Year'), # sort=list(range(1,32))),
        y = alt.Y('yearly_incident_count:Q', title = 'Number of Incidents'),
        tooltip = ['YEAR', 'yearly_incident_count']
    ))
    st.altair_chart(yearly_chart, use_container_width=True)
    st.markdown('''
    Excluding 2026, 2015 had the most incidents with 35,609, and 2020 had the fewest incidents
    with 25,460 (probably because of the Covid-19 pandemic).
    ''')

if pages == 'Crime Map':
    st.subheader('Crime Map')
    col1, col2 = st.columns(2)
    # selected_year = col1.selectbox('Filter by year', sorted(filtered_df['YEAR'].unique()))
    selected_year = col1.slider('Filter by year', 2015, 2026)
    selected_category = col2.multiselect('Filter by category', 
                                         sorted(filtered_df['CATEGORY'].unique()),
                                         default=sorted(filtered_df['CATEGORY'].unique()))
    map_df = filtered_df[
        (filtered_df['YEAR'] == selected_year) &
        (filtered_df['CATEGORY'].isin(selected_category))
    ][['LAT', 'LON']].dropna()
    st.map(map_df)
    st.caption(f'Number of incidents in {selected_year}: {len(map_df)}')

st.divider()
st.caption('Montreal Crime Analysis Application v1.0 | Kiro Shenouda | Jan 19, 2026')