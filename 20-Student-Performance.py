import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
from ucimlrepo import fetch_ucirepo

st.set_page_config(page_title='Student Performance Analysis', layout='wide')
st.title('Student Performance Analysis')

pages = [
    'Home Page',
    'Table Info',
    'Column Overview',
    'Summary Stats',
    'Visualizations',
    'Data Summary/Dictionary'
]
st.sidebar.title('Student Performance')
st.sidebar.header('Page Navigation')
page_options = st.sidebar.radio('Select a page', pages)

@st.cache_data
def load_data():
    try:
        df_math = pd.read_csv('/Users/kiroshenouda/Desktop/COMPSCI/DATASETS/student/student-mat.csv', sep=';')
        df_port = pd.read_csv('/Users/kiroshenouda/Desktop/COMPSCI/DATASETS/student/student-por.csv', sep=';')
        data = fetch_ucirepo(id=320)
        X = data.data.features
        y = data.data.targets
        return df_math, df_port, X, y
    except FileNotFoundError:
        st.error('Data files not found.')
        st.stop()
    except Exception as e:
        st.error(f'Error loading data: {str(e)}')
        st.stop()

with st.spinner('Loading data...'):
    df_math, df_port, X, y = load_data()

port_num_cols = df_port.select_dtypes(include='number').columns.tolist()
port_cat_cols = df_port.select_dtypes(include='object').columns.tolist()
math_num_cols = df_math.select_dtypes(include='number').columns.tolist()
math_cat_cols = df_math.select_dtypes(include='object').columns.tolist()

if page_options == pages[0]:
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric('Math Students', len(df_math))
    with col2:
        st.metric('Portuguese Students', len(df_port))
    with col3:
        st.metric('Total Features', len(df_math.columns))
    st.markdown('''
    ### About this Application
    This application will allow users to analysis and explore student
    performance in Portuguese and Mathematics courses at two
    different Portuguese schools.

    ### Dataset Information
    - **student-mat.csv**: Mathematics course performance
    - **student-por.csv**: Portuguese course performance

    ### Features You Can Explore:
    - Student demographics (e.g. age, gender, family)
    - Study habits and free time
    - Final grades (G1, G2, G3)
    - Social and health factors

    You can navigate between the different pages of this application
    from the sidebar on the left.

    Source: [UC Irvine Machine Learning Repository](https://archive.ics.uci.edu/dataset/320/student+performance)
    ''')
    
if page_options == pages[1]:
    port_tab, math_tab = st.tabs(['Portuguese Table', 'Mathematics Table'])
    with port_tab:
        st.subheader('Portuguese Table Overview')
        port_col1, port_col2 = st.columns(2)
        with port_col1:
            show_rows = st.slider('Number of rows to display', 5, 50, 10, key='port_slider')
        with port_col2:
            search_col = st.selectbox('Filter by column', df_port.columns, key='port_selectbox')
        st.dataframe(df_port.head(show_rows), use_container_width=True)

        st.subheader('Quick Statistics')
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric('Average Final Grade (G3)', f'{df_port.G3.mean():.2f}')
        with col2:
            st.metric('Pass Rate', f'{(df_port.G3 >= 10).sum() / len(df_port) * 100:.1f}%')
        with col3:
            st.metric('Female Students', f"{(df_port['sex'] == 'F').sum()}")
        with col4:
            st.metric('Male Students', f"{(df_port['sex'] == 'M').sum()}")

        with st.expander('View Column Details'):
            st.dataframe(pd.DataFrame({
                'Column': df_port.columns,
                'Data Type': df_port.dtypes,
                'Non-Null Counts': df_port.count(),
                'Unique Values': df_port.nunique()
            }), use_container_width=True)

    with math_tab:
        st.subheader('Mathematics Table Overview')
        math_col1, math_col2 = st.columns(2)
        with math_col1:
            show_rows = st.slider('Number of rows to display', 5, 50, 10, key='math_slider')
        with math_col2:
            search_col = st.selectbox('Filter by column', df_math.columns, key='math_selectbox')
        st.dataframe(df_math.head(show_rows), use_container_width=True)

        st.subheader('Quick Statistics')
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric('Average Final Grade (G3)', f'{df_math.G3.mean():.2f}')
        with col2:
            st.metric('Pass Rate', f'{(df_math.G3 >= 10).sum() / len(df_math) * 100:.1f}%')
        with col3:
            st.metric('Female Students', f"{(df_math['sex'] == 'F').sum()}")
        with col4:
            st.metric('Male Students', f"{(df_math['sex'] == 'M').sum()}")

        with st.expander('View Column Details'):
            st.dataframe(pd.DataFrame({
                'Column': df_math.columns,
                'Data Type': df_math.dtypes,
                'Non-Null Counts': df_math.count(),
                'Unique Values': df_math.nunique()
            }), use_container_width=True)

if page_options == pages[2]:
    st.subheader('Column Overview')
    col1, col2 = st.columns(2)
    with col1:
        st.metric('Numeric Columns', len(port_num_cols))
    with col2:
        st.metric('Categorical Columns', len(port_cat_cols))

    st.subheader('Missing Values')
    missing_data = df_port.isnull().sum()
    missing_data_pct = (100 * missing_data / len(df_port)).round(2)
    if np.count_nonzero(missing_data.values) == 0:
        st.success('File contains no missing values')
    else:
        st.dataframe(pd.DataFrame({
            'Missing Values': missing_data,
            'Missing Value Percentage': missing_data_pct
        }))
        st.caption(f'Dataset contains {missing_values.sum()} missing values')

if page_options == pages[3]:
    st.subheader('Summary Statistics')
    port_tab, math_tab = st.tabs(['Portuguese', 'Mathematics'])
    lowest_age = df_port['age'].min()
    highest_age = df_port['age'].max()
    average_age = df_port['age'].mean().round(1)
    port_lowest_first_period_grade = df_port['G1'].min()
    port_highest_first_period_grade = df_port['G1'].max()
    port_average_first_period_grade = df_port['G1'].mean().round(1)
    port_lowest_second_period_grade = df_port['G2'].min()
    port_highest_second_period_grade = df_port['G2'].max()
    port_average_second_period_grade = df_port['G2'].mean().round(1)
    port_lowest_third_period_grade = df_port['G3'].min()
    port_highest_third_period_grade = df_port['G3'].max()
    port_average_third_period_grade = df_port['G3'].mean().round(1)
    math_lowest_first_period_grade = df_math['G1'].min()
    math_highest_first_period_grade = df_math['G1'].max()
    math_average_first_period_grade = df_math['G1'].mean().round(1)
    math_lowest_second_period_grade = df_math['G2'].min()
    math_highest_second_period_grade = df_math['G2'].max()
    math_average_second_period_grade = df_math['G2'].mean().round(1)
    math_lowest_third_period_grade = df_math['G3'].min()
    math_highest_third_period_grade = df_math['G3'].max()
    math_average_third_period_grade = df_math['G3'].mean().round(1)
    with port_tab:
        port_col1, port_col2, port_col3 = st.columns(3)
        with port_col1:
            st.metric('Youngest Student Age', lowest_age)
            st.metric('Lowest G1 (First Period) Grade', port_lowest_first_period_grade)
            st.metric('Lowest G2 (Second Period) Grade', port_lowest_second_period_grade)
            st.metric('Lowest G3 (Third Period) Grade', port_lowest_third_period_grade)    
        with port_col2: 
            st.metric('Oldest Student Age', highest_age)
            st.metric('Highest G1 (First Period) Grade', port_highest_first_period_grade)
            st.metric('Highest G2 (Second Period) Grade', port_highest_second_period_grade)
            st.metric('Highest G3 (Third Period) Grade', port_highest_third_period_grade)    
        with port_col3: 
            st.metric('Average Student Age', average_age)
            st.metric('Average G1 (First Period) Grade', port_average_first_period_grade)
            st.metric('Average G2 (Second Period) Grade', port_average_second_period_grade)
            st.metric('Average G3 (Third Period) Grade', port_average_third_period_grade)    
    with math_tab:
        math_col1, math_col2, math_col3 = st.columns(3)
        with math_col1:
            st.metric('Youngest Student Age', lowest_age)
            st.metric('Lowest G1 (First Period) Grade', math_lowest_first_period_grade,
                      delta=math_lowest_first_period_grade-port_lowest_first_period_grade)
            st.metric('Lowest G2 (Second Period) Grade', math_lowest_second_period_grade)
            st.metric('Lowest G3 (Third Period) Grade', math_lowest_third_period_grade)    
        with math_col2: 
            st.metric('Oldest Student Age', highest_age)
            st.metric('Highest G1 (First Period) Grade', math_highest_first_period_grade)
            st.metric('Highest G2 (Second Period) Grade', math_highest_second_period_grade)
            st.metric('Highest G3 (Third Period) Grade', math_highest_third_period_grade,
                      delta=math_highest_third_period_grade-port_highest_third_period_grade)    
        with math_col3: 
            st.metric('Average Student Age', average_age)
            st.metric('Average G1 (First Period) Grade', math_average_first_period_grade,
                      delta=math_average_first_period_grade-port_average_first_period_grade)
            st.metric('Average G2 (Second Period) Grade', math_average_second_period_grade,
                      delta=round(math_average_second_period_grade-port_average_second_period_grade,1))
            st.metric('Average G3 (Third Period) Grade', math_average_third_period_grade,
                      delta=math_average_third_period_grade-port_average_third_period_grade)    
        st.write('Compared the Portuguese course, the students performed slightly worse in the Mathematics course according to their average G1, G2, and G3 grades')

if page_options == pages[4]:
    st.subheader('Visualizations')
    tab1, tab2 = st.tabs(['General Graphs', 'Correlations'])
    with tab1:
        st.markdown('''
        Select a numeric and categorical column to visualize for both the
        Portuguese and Mathematics classes.
        ''')
        col1, col2 = st.columns(2)
        with col1:
            selected_num_col = st.selectbox('Numeric columns',
                                            options=port_num_cols, index=None)
            if selected_num_col is not None:
                port_fig = px.histogram(df_port, x=selected_num_col, nbins=20,
                                        title=f'Distribution of {selected_num_col} for the Portuguese class')
                col1.plotly_chart(port_fig, use_container_width=True)
                math_fig = px.histogram(df_math, x=selected_num_col, nbins=20,
                                        title=f'Distribution of {selected_num_col} for the Mathematics class')
                col1.plotly_chart(math_fig, use_container_width=True)

        with col2:
            selected_cat_col = st.selectbox('Categorical columns',
                                            options=port_cat_cols, index=None)
            if selected_cat_col is not None:
                port_fig = px.bar(df_port[selected_cat_col].value_counts().head(20),
                                        title=f'Distribution of {selected_cat_col} for the Portuguese class')
                port_fig.update_layout(showlegend=False)
                col2.plotly_chart(port_fig, use_container_width=True)
                math_fig = px.bar(df_math[selected_cat_col].value_counts().head(20),
                                        title=f'Distribution of {selected_cat_col} for the Mathematics class')
                math_fig.update_layout(showlegend=False)
                col2.plotly_chart(math_fig, use_container_width=True)
    with tab2:
        st.markdown('''
        Select a numeric column to visualize against G1, G2, or G3 grades to
        view any potential relationships between the two variables.
        ''')
        col1, col2 = st.columns(2)
        with col1:
            st.subheader('Portuguese Class')
            port_selected_num_col = st.selectbox('Numeric column',
                                                options=port_num_cols,
                                                index=None,
                                                key='port_corr_num')
            port_grade = st.selectbox('Grade period',
                                    options=['G1', 'G2', 'G3'],
                                    index=2,
                                    key='port_grade')
            if port_selected_num_col:
                port_fig = px.scatter(df_port, x=port_selected_num_col, y=port_grade,
                                    title=f'Correlation: {port_grade} vs {port_selected_num_col}',
                                    trendline='ols',
                                    trendline_color_override='red')
                st.plotly_chart(port_fig, use_container_width=True)
    
        with col2:
            st.subheader('Mathematics Class')
            math_selected_num_col = st.selectbox('Numeric column',
                                                options=math_num_cols,
                                                index=None,
                                                key='math_corr_num')
            math_grade = st.selectbox('Grade period',
                                    options=['G1', 'G2', 'G3'],
                                    index=2,
                                    key='math_grade')
            if math_selected_num_col:
                math_fig = px.scatter(df_math, x=math_selected_num_col, y=math_grade,
                                    title=f'Correlation: {math_grade} vs {math_selected_num_col}',
                                    trendline='ols',
                                    trendline_color_override='red')
                st.plotly_chart(math_fig, use_container_width=True)

if page_options == pages[5]:
    st.subheader('Data Summary and Dictionary')
    data = fetch_ucirepo(id=320)
    st.write(data.metadata.additional_info)

st.divider()
st.caption('Student Performance Analysis Application v1.0, created by Kiro Shenouda')