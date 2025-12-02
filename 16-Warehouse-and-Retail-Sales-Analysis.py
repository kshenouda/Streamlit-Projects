import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

st.set_page_config(page_title='Warehouse and Retail Sales Dashboard', layout='wide')
st.title('Warehouse and Retail Sales Dashboard')

data_url = 'https://www.kaggle.com/datasets/divyeshardeshana/warehouse-and-retail-sales'
st.write('**Source**: [Kaggle](%s)' % data_url)
st.write('''
This dashboard explores a Warehouse and Retail Sales dataset, containing a list of monthly 
sales, suppliers, item type and descriptions, etc. You can explore distributions, 
correlations, and a linear regression model.
''')

# Upload file or load default
uploaded = st.sidebar.file_uploader('Upload Warehouse and Retail Sales Dataset', type='csv')
required_columns = {'YEAR', 'MONTH', 'SUPPLIER', 'ITEM TYPE', 'RETAIL SALES'}

@st.cache_data
def load_data():
    if uploaded:
        df = pd.read_csv(uploaded)
        df['YEAR'] = df['YEAR'].astype(int)
        df['MONTH'] = df['MONTH'].astype(str).str.strip().str.title()
        df['SUPPLIER'] = df['SUPPLIER'].astype(str).str.strip()
        df['ITEM TYPE'] = df['ITEM TYPE'].astype(str).str.strip()
        df['DATE'] = pd.to_datetime(df[['YEAR', 'MONTH']].assign(DAY=1))
    else:
        df = pd.read_csv('/Users/kiroshenouda/Desktop/COMPSCI/DATASETS/Warehouse_and_Retail_Sales.csv')
        df['YEAR'] = df['YEAR'].astype(int)
        df['MONTH'] = df['MONTH'].astype(str).str.strip().str.title()
        df['SUPPLIER'] = df['SUPPLIER'].astype(str).str.strip()
        df['ITEM TYPE'] = df['ITEM TYPE'].astype(str).str.strip()
        df['DATE'] = pd.to_datetime(df[['YEAR', 'MONTH']].assign(DAY=1))
        # df['SUPPLIER'] = df['SUPPLIER'].str.title()
    return df

df = load_data()
if not required_columns.issubset(df.columns):
    st.error('Uploaded file must contain required columns')
    st.stop()

st.sidebar.header('Filter options')
year_filter = st.sidebar.multiselect('Year', 
                                     sorted(df['YEAR'].unique()),
                                     default=df['YEAR'].unique(),
                                     key='year_filter')
month_filter = st.sidebar.multiselect('Month',
                                      sorted(df['MONTH'].unique()),
                                      default=df['MONTH'].unique(),
                                      key='month_filter')
supplier_filter = st.sidebar.multiselect('Supplier',
                                         sorted(df['SUPPLIER'].dropna().unique()),
                                         default=sorted(df['SUPPLIER'].dropna().unique()),
                                         key='supplier_filter')
item_type_filter = st.sidebar.multiselect('Item Type',
                                          sorted(df['ITEM TYPE'].dropna().unique()),
                                          default=sorted(df['ITEM TYPE'].dropna().unique()),
                                          key='item_type_filter')
retail_sales_filter = st.sidebar.slider('Retail Sales',
                                        int(df['RETAIL SALES'].min()),
                                        int(df['RETAIL SALES'].max()),
                                        (int(df['RETAIL SALES'].min()), int(df['RETAIL SALES'].max())),
                                        key='retail_sales_filter')
retail_transfers_filter = st.sidebar.slider('Retail Transfers',
                                            int(df['RETAIL TRANSFERS'].min()),
                                            int(df['RETAIL TRANSFERS'].max()),
                                            (int(df['RETAIL TRANSFERS'].min()), int(df['RETAIL TRANSFERS'].max())),
                                            key='retail_transfers_filter')
warehouse_sales_filter = st.sidebar.slider('Warehouse Sales',
                                           int(df['WAREHOUSE SALES'].min()),
                                           int(df['WAREHOUSE SALES'].max()),
                                           (int(df['WAREHOUSE SALES'].min()), int(df['WAREHOUSE SALES'].max())),
                                           key='warehouse_sales_filter')
st.sidebar.button('Reset filters', on_click=lambda: st.session_state.update({
    'year_filter': df['YEAR'].unique().tolist(),
    'month_filter': df['MONTH'].unique().tolist(),
    'supplier_filter': df['SUPPLIER'].unique().tolist(),
    'item_type_filter': df['ITEM TYPE'].unique().tolist(),
    'retail_sales_filter': (int(df['RETAIL SALES'].min()), int(df['RETAIL SALES'].max())),
    'retail_transfers_filter': (int(df['RETAIL TRANSFERS'].min()), int(df['RETAIL TRANSFERS'].max())),
    'warehouse_sales_filter': (int(df['WAREHOUSE SALES'].min()), int(df['WAREHOUSE SALES'].max()))
}))


filtered_df = df[
    (df['YEAR'].isin(year_filter)) &
    (df['MONTH'].isin(month_filter)) &
    (df['SUPPLIER'].isin(supplier_filter)) &
    (df['ITEM TYPE'].isin(item_type_filter)) &
    (df['RETAIL SALES'].between(retail_sales_filter[0], retail_sales_filter[1])) &
    (df['RETAIL TRANSFERS'].between(retail_transfers_filter[0], retail_transfers_filter[1])) &
    (df['WAREHOUSE SALES'].between(warehouse_sales_filter[0], warehouse_sales_filter[1]))
]

if filtered_df.empty:
    st.warning('No data matches your filters. Try adjusting the filter selections and try again.')
    st.stop()

df_col1, df_col2 = st.columns(2)

with df_col1:
    with st.expander('View full dataset'):
        st.dataframe(df.head(10))
        st.write(f'**Rows**: {df.shape[0]}')
        st.write(f'**Columns**: {df.shape[1]}')

with df_col2:
    with st.expander('View filtered dataset'):
        st.dataframe(filtered_df.head(10))
        st.write(f'**Rows**: {filtered_df.shape[0]}')
        st.write(f'**Columns**: {filtered_df.shape[1]}')

st.subheader('Key Metrics')
tab1, tab2 = st.tabs(['Sales Metrics', 'Supplier and Item Metrics'])
with tab1:
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric('Total Retail Sales', f"${filtered_df['RETAIL SALES'].sum():,.2f}")
    with col2:
        st.metric('Total Warehouse Sales', f"${filtered_df['WAREHOUSE SALES'].sum():,.2f}")
    with col3:
        st.metric('Total Retail Transfers', f"${filtered_df['RETAIL TRANSFERS'].sum():,.2f}")
    with col1:
        avg_retail_sales = filtered_df['RETAIL SALES'].mean()
        st.metric('Average Retail Sales', f"${avg_retail_sales:,.2f}")
    with col2:
        avg_warehouse_sales = filtered_df['WAREHOUSE SALES'].mean()
        st.metric('Average Warehouse Sales', f"${avg_warehouse_sales:,.2f}")
    with col3:
        avg_retail_transfers = filtered_df['RETAIL TRANSFERS'].mean()
        st.metric('Average Retail Transfers', f"${avg_retail_transfers:,.2f}")
    with col1:
        month_with_highest_retail_sales = (filtered_df.groupby('MONTH')['RETAIL SALES'].sum().idxmax())
        st.metric('Month with Highest Retail Sales', 
                  month_with_highest_retail_sales,
                  delta=filtered_df.groupby('MONTH')['RETAIL SALES'].sum().max())
    with col2:
        year_with_highest_retail_sales = (filtered_df.groupby('YEAR')['RETAIL SALES'].sum().idxmax())
        st.metric('Year with Highest Retail Sales', 
                  year_with_highest_retail_sales,
                  delta=filtered_df.groupby('YEAR')['RETAIL SALES'].sum().max())
with tab2:
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric('Unique Suppliers', filtered_df['SUPPLIER'].nunique())
    with col2:
        st.metric('Unique Item Types', filtered_df['ITEM TYPE'].nunique())
    with col3:
        st.metric('Unique Item Descriptions', filtered_df['ITEM DESCRIPTION'].nunique())
    with col1:
        top_supplier = (filtered_df.groupby('SUPPLIER')['RETAIL SALES']
                        .sum()
                        .idxmax())
        st.metric('Top Supplier by Retail Sales', top_supplier,
                  delta=filtered_df.groupby('SUPPLIER')['RETAIL SALES'].sum().max())

with st.expander('Visualizations'):
# st.subheader('Visualizations')
    tab1, tab2, tab3, tab4 = st.tabs(['Sales Distributions', 'Sales Over Time', 'Sales by Supplier', 'Correlation Matrix'])
    with tab1:
        fig1 = px.histogram(filtered_df, x='RETAIL SALES', nbins=50, title='Retail Sales Distribution')
        st.plotly_chart(fig1, use_container_width=True)
        fig2 = px.histogram(filtered_df, x='WAREHOUSE SALES', nbins=50, title='Warehouse Sales Distribution')
        st.plotly_chart(fig2, use_container_width=True)
        fig3 = px.histogram(filtered_df, x='RETAIL TRANSFERS', nbins=50, title='Retail Transfers Distribution')
        st.plotly_chart(fig3, use_container_width=True)
    with tab2:
        fig = px.line(filtered_df.groupby('DATE').sum().reset_index(), 
                      x='DATE', 
                      y=['RETAIL SALES', 'WAREHOUSE SALES', 'RETAIL TRANSFERS'],
                      title='Sales Over Time')
        st.plotly_chart(fig, use_container_width=True)
        pass
    with tab3:
        col1, col2 = st.columns(2)
        with col1:
            top_suppliers = (filtered_df.groupby('SUPPLIER')['RETAIL SALES']
                             .sum()
                             .sort_values(ascending=False)
                             .head(10)
                             .reset_index())
            fig = px.bar(top_suppliers, x='SUPPLIER', y='RETAIL SALES',
                         title='Top 10 Suppliers by Retail Sales')
            st.plotly_chart(fig, use_container_width=True)
            st.caption('Supplier E&J Gallo Winery has the highest retail sales among all suppliers')
        with col2:
            item_type_sales = (filtered_df.groupby('ITEM TYPE')['RETAIL SALES']
                               .sum()
                               .sort_values(ascending=False)
                               .reset_index())
            fig = px.bar(item_type_sales, x='ITEM TYPE', y='RETAIL SALES',
                         title='Retail Sales by Item Type')
            #fig = px.pie(item_type_sales, values='RETAIL SALES', names='ITEM TYPE',
            #             title='Retail Sales by Item Type')
            st.plotly_chart(fig, use_container_width=True)
            st.caption('Beverages - liquor, wine, and beer - account for the highest retail sales among all item types sold')
    with tab4:
        corr = filtered_df[['RETAIL SALES', 'WAREHOUSE SALES', 'RETAIL TRANSFERS']].corr()
        fig = px.imshow(corr, text_auto=True, 
                        title='Correlation Matrix of Sales Metrics',
                        color_continuous_scale='RdBu_r')
        st.plotly_chart(fig, use_container_width=True)
        fig.update_layout(margin=dict(l=40, r=40, t=40, b=40))
        st.caption('Retail Sales and Retail Transfers have a strong correlation coefficient of 0.979')
