import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px

st.set_page_config(page_title='Data Analysis/Cleaning Application', layout='wide')
st.title('Data Analysis/Cleaning App')
#st.markdown('''
#This application allows users to upload a dataset where they can 
#* View the dataset
#* Read column breakdown (number of columns and column data types)
#* Read percentage of dataset that contains missing data
#* Select what columns to drop
#* Visualize columns
#* Apply transformations
#* Export a cleaned/filtered dataset
#''')
st.markdown('''
This application allows users to upload a dataset where they can read column breakdown 
(number of columns and column data types), read percentage of dataset that contains 
missing data, select what columns to drop, visualize columns, apply transformations,
and export a cleaned/filtered dataset
''')

page_options = [
    'File Preview', 
    'Missing Values',
    'Column Breakdown', 
    'Column Redefinition',
    'Visualizations',
#    'Select Columns to Drop',
#    'Apply Transformations',
#    'Export Cleaned Dataset'
]

def convert_column_dtype(df, column, target_type):
    try:
        if target_type == 'Integer':
            df[column] = pd.to_numeric(df[column], errors='raise').astype('Int64')
        elif target_type == 'Float':
            df[column] = pd.to_numeric(df[column], errors='raise')
        elif target_type == 'Object':
            df[column] = df[column].astype(str)
        elif target_type == 'Boolean':
            df[column] = df[column].astype(bool)
        elif target_type == 'Date':
            # df[column] == pd.to_datetime(df[column], errors='raise').dt.date
            df[column] == pd.to_datetime(df[column], errors='raise')
        elif target_type == 'Datetime':
            df[column] == pd.to_datetime(df[column], errors='raise')
        return True, None

    except Exception as e:
        return False, str(e)

# uploaded_file = st.sidebar.file_uploader('Select a file to upload', type=['csv'], accept_multiple_files=True)
uploaded_file = st.sidebar.file_uploader('Select a file to upload', type=['csv'], key='file_uploader')

if uploaded_file is not None:
    if 'df' not in st.session_state:
        st.session_state.df = None
        
    if 'uploaded_filename' not in st.session_state:
        st.session_state.uploaded_filename = None

    if uploaded_file.name != st.session_state.uploaded_filename:
        st.session_state.uploaded_filename = uploaded_file.name
        st.session_state.df = pd.read_csv(uploaded_file)

    st.sidebar.divider()
    pages = st.sidebar.radio('Pages', page_options)
    st.divider()
    subheader = st.subheader(f'File Name: {uploaded_file.name}')
    df = st.session_state.df
    # df = pd.DataFrame(pd.read_csv(uploaded_file))
    cat_cols = df.select_dtypes(include=['category','object'])
    num_cols = df.select_dtypes(include=['int', 'float'])
    
    if pages == page_options[0]:
        st.write(df)
        st.caption(f'Rows returned: {df.shape[0]}')
        st.caption(f'Columns returned: {df.shape[1]}')

    if pages == page_options[1]:
        st.subheader('Missing Values Summary')
        missing_values = df.isna().sum()
        missing_values_pct = (100 * missing_values / len(df)).round(2)
        if np.count_nonzero(missing_values.values) == 0:
            # st.success(f'{uploaded_file.name} contains no missing values')
            st.success('File contains no missing values')
        else:
            st.dataframe(pd.DataFrame({
                #'Column Name': df.columns,
                'Missing Values': missing_values,
                'Missing Value Percentage': missing_values_pct
            }))
            st.caption(f'Dataset contains {missing_values.sum()} missing values')

    if pages == page_options[2]:
        st.subheader('Column Breakdown')
        col1, col2, col3 = st.columns(3)
        col1.metric('Total columns', df.shape[1])
        col2.metric('Categorical columns', cat_cols.shape[1])
        col3.metric('Numerical columns', num_cols.shape[1])
        st.divider()
        st.dataframe(pd.DataFrame({
            'Column Name': df.columns,
            'Data Type': df.dtypes.astype(str)
        }))

    if pages == page_options[3]:
        st.subheader('Column Redefinition (Optional)')

        col1, col2 = st.columns(2)

        column_selection = col1.selectbox('Select a column',
                                        options = df.columns,
                                        index = None)
        dtype_mapping = [
            'Integer',
            'Float',
            'Object',
            'Boolean',
            'Date',
            'Datetime'
        ]
        data_type_selection = col2.selectbox('Select a new data type',
                                             options = dtype_mapping,
                                             index = None)
        if column_selection and data_type_selection:
            if st.button('Convert Column Data Type'):
                with st.spinner('Converting column...'):
                    success, error = convert_column_dtype(
                        st.session_state.df,
                        column_selection,
                        data_type_selection
                    )
                if success:
                    st.success(f"'{column_selection}' has been successfully convereted to {data_type_selection}")
                else:
                    st.error(f'Conversion failed: {error}')
        st.divider()
        st.dataframe(df.dtypes.astype(str), use_container_width=True)

    if pages == page_options[4]:
        col1, col2 = st.columns([1, 1])
        num_col_selection = col1.selectbox('Select a numerical column to visualize',
                                            options=num_cols.columns, index=None)
        cat_col_selection = col2.selectbox('Select a categorical column to visualize',
                                            options=cat_cols.columns, index=None)
        if num_col_selection:
            fig = px.histogram(df, x=num_col_selection, nbins=20,
                               title=f'Distribution of {num_col_selection}')
            col1.plotly_chart(fig, use_container_width=True)
        if cat_col_selection:
            fig = px.bar(df[cat_col_selection].value_counts().head(20),
                         title=f'Distribution of {cat_col_selection}')
            fig.update_layout(showlegend=False)
            col2.plotly_chart(fig, use_container_width=True)
        
else:
    st.info('Upload a file from the sidebar')

st.divider()
st.caption('Data Analysis/Cleaning Application v1.0, created by Kiro Shenouda')