import streamlit as st
import numpy as np
import pandas as pd
import requests

st.set_page_config(page_title='Amazon Data App', layout='wide')
st.title('Real Time Amazon Data App')

endpoints = ['search', 'products-by-category', 'product-details', 'product-reviews', 'product-offers']
selected_endpoint = st.selectbox('Select an endpoint to request data from', 
                                 options = endpoints, 
                                 index = None)

headers = {
	"x-rapidapi-key": "666e934e24msh842e981f4ebcf90p1369d1jsnfa7f40147688",
	"x-rapidapi-host": "real-time-amazon-data.p.rapidapi.com"
}

countries = sorted(['US', 'AU', 'BR', 'CA', 'CN', 'FR', 'DE', 'IN', 'IT', 'MX', 'NL', 'SG', 'ES', 'TR', 'AE', 'GB', 'JP', 'SA', 'PL', 'SE', 'BE', 'EG'])
sort_by_options = ['RELEVANCE', 'LOWEST_PRICE', 'HIGHEST_PRICE', 'REVIEWS', 'NEWEST', 'BEST_SELLERS']
product_conditions_options = ['ALL', 'NEW', 'USED', 'RENEWED', 'COLLECTIBLE']
product_conditions_offers_options = ['NEW', 'USED_LIKE_NEW', 'USED_VERY_GOOD', 'USED_GOOD', 'USED_ACCEPTABLE']
deals_and_discounts_options = ['NONE', 'ALL_DISCOUNTS', 'TODAYS_DEALS']
star_rating_options = ['ALL', '5_STARS', '4_STARS', '3_STARS', '2_STARS', '1_STARS', 'POSITIVE', 'CRITICAL']

def get_data(endpoint, params):
    url = f'https://real-time-amazon-data.p.rapidapi.com/{endpoint}'
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        st.error(f'Error: {response.status_code}')

if selected_endpoint:
    with st.form(key='send_request'):
        st.subheader(f'Customize parameters for {selected_endpoint}')

        if selected_endpoint == 'search':
            query = st.text_input('Enter query/search',
                                  placeholder='e.g. Phone')
            page = st.number_input('Enter page number (optional)', 1)
            country = st.selectbox('Enter country', options=countries, index=None)
            sort_by = st.selectbox('Enter sort by field', options=sort_by_options, index=None)
            product_condition = st.selectbox('Enter product condition', options=product_conditions_options, index=None)
            is_prime = st.radio('Enter if product is prime', ['true', 'false'])
            deals_and_discounts = st.selectbox('Enter any deals/discounts:', options=deals_and_discounts_options, index=None)

            params = {
                'query': query,
                'page': page,
                'country': country,
                'sort_by': sort_by,
                'product_condition': product_condition,
                'is_prime': is_prime,
                'deals_and_discounts': deals_and_discounts
            }

        if selected_endpoint == 'products-by-category':
            category_id = st.text_input('Enter category ID',
                                        placeholder='281407')
            page = st.number_input('Enter page number (optional)', 1)
            country = st.selectbox('Enter country', options=countries, index=None)
            sort_by = st.selectbox('Enter sort by field', options=sort_by_options, index=None)
            product_condition = st.selectbox('Enter product condition', options=product_conditions_options, index=None)
            is_prime = st.radio('Enter if product is prime', ['true', 'false'])
            deals_and_discounts = st.selectbox('Enter any deals/discounts:', options=deals_and_discounts_options, index=None)

            params = {
                'category_id': category_id,
                'page': page,
                'country': country,
                'sort_by': sort_by,
                'product_condition': product_condition,
                'is_prime': is_prime,
                'deals_and_discounts': deals_and_discounts
            }

        if selected_endpoint == 'product-details':
            asin = st.text_input('Enter product ASIN',
                                 placeholder='B07ZPKBL9V')
            country = st.selectbox('Enter country', options=countries, index=None)

            params = {
                'asin': asin,
                'country': country
            }

        if selected_endpoint == 'product-reviews':
            asin = st.text_input('Enter product ASIN',
                        placeholder='B07ZPKN6YR')
            country = st.selectbox('Enter country (optional)', options=countries, index=None)
            page = st.number_input('Enter page number (optional)', 1)
            sort_by = st.selectbox('Enter sort by field (optional)', options=['TOP_REVIEWS', 'MOST_RECENT'], index=None)
            star_rating = st.selectbox('Enter star rating (optional)', options=star_rating_options, index=None)
            verified_purchases_only = st.radio('Are purchases verified? (optional)', options=['true', 'false'])
            images_or_videos_only = st.radio('Return reviews containing images and/or videos only? (optional)', options=['true', 'false'])

            params = {
                'asin': asin,
                'country': country,
                'page': page,
                'sort_by': sort_by,
                'star_rating': star_rating,
                'verified_purchases_only': verified_purchases_only,
                'images_or_videos_only': images_or_videos_only
            }

        if selected_endpoint == 'product-offers':
            asin = st.text_input('Enter product ASIN',
                                 placeholder='B09SM24S8C')
            page = st.number_input('Enter page number (optional)', 1)
            country = st.selectbox('Enter country (optional)', options=countries, index=None)
            product_condition = st.selectbox('Enter product condition (optional)', options=product_conditions_offers_options, index=None)
            delivery = st.selectbox('Enter delivery options (optional)', options=['FREE_DELIVERY', 'PRIME_ELIGIBLE,FREE_DELIVERY'], index=None)
            limit = st.number_input('Enter maximum number of offers to return (optional)', 100)

            params = {
                'asin': asin,
                'page': page,
                'country': country,
                'product_condition': product_condition,
                'delivery': delivery,
                'limit': limit
            }
        
        else:
            params = {}

        submit = st.form_submit_button('Submit')

    if submit:
        with st.spinner('Fetching data...'):
            data = get_data(selected_endpoint, params)
            if data:
                st.success(f'Retrieved {len(data)} rows')
                st.dataframe(data)
            else:
                st.warning('No results found')