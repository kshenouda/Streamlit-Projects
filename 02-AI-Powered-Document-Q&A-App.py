import streamlit as st
import numpy as np
import PyPDF2
import faiss
import hashlib
from sentence_transformers import SentenceTransformer
from transformers import pipeline

st.set_page_config(
    page_title='AI Document Q&A',
    layout = 'wide'
)
st.title('AI-Powered Document Q&A')
st.markdown('''
Upload your PDF and ask questions using retrieval-augmented AI pipeline.
''')

# Load models
@st.cache_resource
def load_models():
    embedder = SentenceTransformer('all-MiniLM-L6-v2')
    qa_model = pipeline(
        'question-answering',
        model='deepset/roberta-base-squad2'   
    )
    return embedder, qa_model
    #return pipeline('question-answering', 
    #                model = 'deepset/roberta-base-squad2',
    #                framework = 'pt')

embedder, qa_pipeline = load_models()

# Helpers
def extract_text(file):
    reader = PyPDF2.PdfReader(file)
    return '\n'.join(
        page.extract_text() for page in reader.pages if page.extract_text()
    )

def chunk_text(text, chunk_size=500, overlap=50):
    words = text.split()
    chunks = []
    i = 0
    while i < len(words):
        chunk = words[i:i + chunk_size]
        chunks.append(' '.join(chunk))
        i += chunk_size - overlap
    return chunks

def build_vector_store(chunks):
    embeddings = embedder.encode(chunks)
    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(np.array(embeddings))
    return index, embeddings

def retrieve_chunks(question, chunks, index, k=3):
    q_embedding = embedder.encode([question])
    distances, indices = index.search(np.array(q_embedding), k)
    return [chunks[i] for i in indices[0]]

# App logic
uploaded_file = st.sidebar.file_uploader("Upload a PDF", type=["pdf"])

if uploaded_file:
    with st.spinner('Processing document...'):
        text = extract_text(uploaded_file)
        chunks = chunk_text(text)
        index, _ = build_vector_store(chunks)

    st.success('Document processed successfully!')

    question = st.text_input('Ask a question about the document')

    if question:
        with st.spinner('Searching for answers...'):
            relevant_chunks = retrieve_chunks(question, chunks, index)
            context = ' '.join(relevant_chunks)
            answers = qa_pipeline(
                question=question,
                context=context
            )
        st.subheader('Answer')
        st.write(answers['answer'])
        
        with st.expander('Retrieved Context:'):
            for i, chunk in enumerate(relevant_chunks, 1):
                st.markdown(f'**Chunk {i}:** {chunk}')
else:
    st.info('Please upload a PDF document to get started.')