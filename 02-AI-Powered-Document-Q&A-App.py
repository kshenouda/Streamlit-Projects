# 2. AI-Powered Document Q&A App 🤖📄
# Upload a PDF or text file.
# Use an embedding + retrieval pipeline (FAISS, Chroma) + LLM (Ollama, OpenAI, or Hugging Face).
# Ask questions in natural language, get contextual answers.
# Demonstrates NLP and RAG (retrieval-augmented generation).

import streamlit as st
import PyPDF2
from transformers import pipeline
# import os
# import tempfile
# from langchain.document_loaders import PyPDFLoader
# from langchain_community.document_loaders import PyPDFLoader
# from langchain.text_splitter import RecursiveCharacterTextSplitter
# from langchain.embeddings import OpenAIEmbeddings
# from langchain.vectorstores import FAISS

# Streamlit page config
st.set_page_config(page_title = 'Document Q&A App', initial_sidebar_state = 'auto', layout = 'wide') # initial_sidebar_state = 'expanded'
st.title('AI Document Q&A App (Hugging Face Model)')
st.markdown('##### Upload your PDF and ask questions - the AI will be able to answer using the document.')

# Load Hugging Face Q&A Pipeline
@st.cache_resource
def load_qa_pipeline():
    return pipeline('question-answering', 
                    model = 'deepset/roberta-base-squad2',
                    framework = 'pt')

qa_pipeline = load_qa_pipeline()

uploaded_file = st.file_uploader("Upload a PDF", type=["pdf"])

if uploaded_file:
    # Extract text from PDF
    pdf_reader = PyPDF2.PdfReader(uploaded_file)
    text = ''
    for page in pdf_reader.pages:
        text += page.extract_text() + '\n'
    st.success('✅ PDF text extracted. You can now ask questions!')

    # Input for questions
    question = st.text_input('Ask a question about the document: ')

    if question:
        with st.spinner('Thinking...'):
            result = qa_pipeline(question = question, context = text)
        st.subheader('Answer: ')
        st.write(result['answer'])
