import numpy as np
import pandas as pd
import streamlit as st
import pdfplumber
import pytesseract
import openpyxl
import os
import tempfile
from PIL import Image
from io import BytesIO

st.set_page_config('File Processing Automation App', layout = 'wide')
st.title('File Processing Automation App')

uploaded_file = st.file_uploader('Upload a file', type=['jpg', 'jpeg', 'png', 'pdf'])

def extract_text_from_pdf(file):
    all_text = ''
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                all_text += text + '\n'
            else:
                image = page.to_image(resolution=300).original
                all_text += pytesseract.image_to_string(image) + '\n'
    return all_text

def extract_text_from_image(file):
    image = Image.open(file)
    return pytsseract.image_to_string(image)

if uploaded_file is not None:
    st.success('File uploaded successfully!')

    if st.button('Process File'):
        with st.spinner('Processing file...'):
            if uploaded_file.type == 'application/pdf':
                text_data = extract_text_from_pdf(uploaded_file)
            else:
                text_data = extract_text_from_image(uploaded_file)

        if text_data.strip():
            st.subheader('Extracted Text')
            st.text_area('Output', text_data, height=400)
        else:
            st.warning('No text could be extracted from this file.')