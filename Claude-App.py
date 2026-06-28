import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

# Page configuration
st.set_page_config(
    page_title="Sales Analytics Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main {
        padding: 0rem 1rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .stMetric {
        background-color: white;
        padding: 15px;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    </style>
    """, unsafe_allow_html=True)

# Generate sample dataset
@st.cache_data
def load_data():
    np.random.seed(42)
    
    # Generate dates for the last 12 months
    end_date = datetime.now()
    start_date = end_date - timedelta(days=365)
    dates = pd.date_range(start=start_date, end=end_date, freq='D')
    
    # Generate sample sales data
    n_records = len(dates) * 5  # 5 transactions per day on average
    
    data = {
        'date': np.random.choice(dates, n_records),
        'product': np.random.choice(['Product A', 'Product B', 'Product C', 'Product D', 'Product E'], n_records),
        'category': np.random.choice(['Electronics', 'Clothing', 'Food', 'Books', 'Home'], n_records),
        'region': np.random.choice(['North', 'South', 'East', 'West'], n_records),
        'customer_type': np.random.choice(['New', 'Returning', 'VIP'], n_records, p=[0.3, 0.5, 0.2]),
        'sales_amount': np.random.gamma(2, 50, n_records),
        'quantity': np.random.randint(1, 20, n_records),
        'discount': np.random.choice([0, 5, 10, 15, 20], n_records, p=[0.5, 0.2, 0.15, 0.1, 0.05])
    }
    
    df = pd.DataFrame(data)
    df['revenue'] = df['sales_amount'] * (1 - df['discount']/100)
    df['profit'] = df['revenue'] * np.random.uniform(0.15, 0.35, n_records)
    df['date'] = pd.to_datetime(df['date'])
    
    return df.sort_values('date')

# Load data
df = load_data()

# Sidebar filters
st.sidebar.header("🔍 Filters")

# Date range filter
date_range = st.sidebar.date_input(
    "Select Date Range",
    value=(df['date'].min(), df['date'].max()),
    min_value=df['date'].min(),
    max_value=df['date'].max()
)

# Region filter
regions = st.sidebar.multiselect(
    "Select Region(s)",
    options=df['region'].unique(),
    default=df['region'].unique()
)

# Category filter
categories = st.sidebar.multiselect(
    "Select Category(ies)",
    options=df['category'].unique(),
    default=df['category'].unique()
)

# Customer type filter
customer_types = st.sidebar.multiselect(
    "Select Customer Type(s)",
    options=df['customer_type'].unique(),
    default=df['customer_type'].unique()
)

# Apply filters
if len(date_range) == 2:
    filtered_df = df[
        (df['date'].dt.date >= date_range[0]) &
        (df['date'].dt.date <= date_range[1]) &
        (df['region'].isin(regions)) &
        (df['category'].isin(categories)) &
        (df['customer_type'].isin(customer_types))
    ]
else:
    filtered_df = df[
        (df['region'].isin(regions)) &
        (df['category'].isin(categories)) &
        (df['customer_type'].isin(customer_types))
    ]

# Main dashboard
st.title("📊 Sales Analytics Dashboard")
st.markdown("---")

# KPI Section
st.header("Key Performance Indicators")

col1, col2, col3, col4, col5 = st.columns(5)

total_revenue = filtered_df['revenue'].sum()
total_profit = filtered_df['profit'].sum()
total_orders = len(filtered_df)
avg_order_value = filtered_df['revenue'].mean()
profit_margin = (total_profit / total_revenue * 100) if total_revenue > 0 else 0

with col1:
    st.metric(
        label="💰 Total Revenue",
        value=f"${total_revenue:,.0f}",
        delta=f"{(total_revenue / 1000000):.2f}M"
    )

with col2:
    st.metric(
        label="📈 Total Profit",
        value=f"${total_profit:,.0f}",
        delta=f"{profit_margin:.1f}% margin"
    )

with col3:
    st.metric(
        label="🛒 Total Orders",
        value=f"{total_orders:,}",
        delta=f"{total_orders/365:.0f}/day avg"
    )

with col4:
    st.metric(
        label="💵 Avg Order Value",
        value=f"${avg_order_value:.2f}",
        delta="Per transaction"
    )

with col5:
    st.metric(
        label="👥 Customer Types",
        value=f"{filtered_df['customer_type'].nunique()}",
        delta=f"{len(filtered_df['customer_type'].unique())} types"
    )

st.markdown("---")

# Charts Section
col1, col2 = st.columns(2)

with col1:
    st.subheader("📅 Revenue Trend Over Time")
    
    # Group by date and sum revenue
    daily_revenue = filtered_df.groupby(filtered_df['date'].dt.date)['revenue'].sum().reset_index()
    daily_revenue.columns = ['Date', 'Revenue']
    
    fig1 = px.line(
        daily_revenue,
        x='Date',
        y='Revenue',
        title='Daily Revenue Trend',
        labels={'Revenue': 'Revenue ($)', 'Date': 'Date'}
    )
    fig1.update_traces(line_color='#1f77b4', line_width=2)
    fig1.update_layout(
        hovermode='x unified',
        plot_bgcolor='white',
        height=400
    )
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    st.subheader("🏷️ Revenue by Category")
    
    category_revenue = filtered_df.groupby('category')['revenue'].sum().reset_index()
    category_revenue = category_revenue.sort_values('revenue', ascending=False)
    
    fig2 = px.bar(
        category_revenue,
        x='category',
        y='revenue',
        title='Total Revenue by Category',
        labels={'revenue': 'Revenue ($)', 'category': 'Category'},
        color='revenue',
        color_continuous_scale='Blues'
    )
    fig2.update_layout(
        showlegend=False,
        plot_bgcolor='white',
        height=400
    )
    st.plotly_chart(fig2, use_container_width=True)

# Second row of charts
col3, col4 = st.columns(2)

with col3:
    st.subheader("🌍 Sales by Region")
    
    region_data = filtered_df.groupby('region').agg({
        'revenue': 'sum',
        'profit': 'sum'
    }).reset_index()
    
    fig3 = go.Figure()
    fig3.add_trace(go.Bar(
        name='Revenue',
        x=region_data['region'],
        y=region_data['revenue'],
        marker_color='lightblue'
    ))
    fig3.add_trace(go.Bar(
        name='Profit',
        x=region_data['region'],
        y=region_data['profit'],
        marker_color='darkblue'
    ))
    
    fig3.update_layout(
        barmode='group',
        title='Revenue vs Profit by Region',
        xaxis_title='Region',
        yaxis_title='Amount ($)',
        plot_bgcolor='white',
        height=400
    )
    st.plotly_chart(fig3, use_container_width=True)

with col4:
    st.subheader("👤 Customer Type Distribution")
    
    customer_revenue = filtered_df.groupby('customer_type')['revenue'].sum().reset_index()
    
    fig4 = px.pie(
        customer_revenue,
        values='revenue',
        names='customer_type',
        title='Revenue Distribution by Customer Type',
        color_discrete_sequence=px.colors.sequential.Blues_r
    )
    fig4.update_traces(textposition='inside', textinfo='percent+label')
    fig4.update_layout(height=400)
    st.plotly_chart(fig4, use_container_width=True)

st.markdown("---")

# Product Performance Section
st.header("🏆 Product Performance")

col5, col6 = st.columns(2)

with col5:
    st.subheader("Top 10 Products by Revenue")
    
    top_products = filtered_df.groupby('product')['revenue'].sum().nlargest(10).reset_index()
    
    fig5 = px.bar(
        top_products,
        x='revenue',
        y='product',
        orientation='h',
        title='Top 10 Products',
        labels={'revenue': 'Revenue ($)', 'product': 'Product'},
        color='revenue',
        color_continuous_scale='Viridis'
    )
    fig5.update_layout(
        showlegend=False,
        plot_bgcolor='white',
        height=400
    )
    st.plotly_chart(fig5, use_container_width=True)

with col6:
    st.subheader("Product Quantity Sold")
    
    product_quantity = filtered_df.groupby('product')['quantity'].sum().nlargest(10).reset_index()
    
    fig6 = px.bar(
        product_quantity,
        x='quantity',
        y='product',
        orientation='h',
        title='Top 10 Products by Quantity',
        labels={'quantity': 'Units Sold', 'product': 'Product'},
        color='quantity',
        color_continuous_scale='Greens'
    )
    fig6.update_layout(
        showlegend=False,
        plot_bgcolor='white',
        height=400
    )
    st.plotly_chart(fig6, use_container_width=True)

st.markdown("---")

# Detailed Data Table
st.header("📋 Detailed Transaction Data")

# Summary statistics
col7, col8 = st.columns(2)

with col7:
    st.subheader("Summary Statistics")
    summary_stats = filtered_df[['revenue', 'profit', 'quantity', 'discount']].describe()
    st.dataframe(summary_stats.style.format("{:.2f}"), use_container_width=True)

with col8:
    st.subheader("Monthly Performance")
    monthly_data = filtered_df.copy()
    monthly_data['month'] = monthly_data['date'].dt.to_period('M')
    monthly_summary = monthly_data.groupby('month').agg({
        'revenue': 'sum',
        'profit': 'sum',
        'product': 'count'
    }).reset_index()
    monthly_summary.columns = ['Month', 'Revenue', 'Profit', 'Transactions']
    monthly_summary['Month'] = monthly_summary['Month'].astype(str)
    st.dataframe(
        monthly_summary.style.format({
            'Revenue': '${:,.2f}',
            'Profit': '${:,.2f}',
            'Transactions': '{:,}'
        }),
        use_container_width=True
    )

# Full data table with search and pagination
st.subheader("Transaction Records")

# Add search functionality
search_term = st.text_input("🔎 Search transactions", "")

if search_term:
    display_df = filtered_df[
        filtered_df.apply(lambda row: search_term.lower() in str(row).lower(), axis=1)
    ]
else:
    display_df = filtered_df

# Display dataframe
st.dataframe(
    display_df[['date', 'product', 'category', 'region', 'customer_type', 
                'quantity', 'sales_amount', 'discount', 'revenue', 'profit']].style.format({
        'date': lambda x: x.strftime('%Y-%m-%d'),
        'sales_amount': '${:.2f}',
        'discount': '{:.0f}%',
        'revenue': '${:.2f}',
        'profit': '${:.2f}'
    }),
    use_container_width=True,
    height=400
)

# Download button
st.download_button(
    label="📥 Download Filtered Data as CSV",
    data=display_df.to_csv(index=False).encode('utf-8'),
    file_name=f'sales_data_{datetime.now().strftime("%Y%m%d")}.csv',
    mime='text/csv',
)

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #666;'>
        <p>Sales Analytics Dashboard | Data updated in real-time | Built with Streamlit</p>
    </div>
    """,
    unsafe_allow_html=True
)