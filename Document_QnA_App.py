import os
import streamlit as st
from langchain_groq import ChatGroq
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.prompts import ChatPromptTemplate
from langchain.chains import create_retrieval_chain
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings

from dotenv import load_dotenv
load_dotenv()

## load the GROQ API key from the environment variable
groq_api_key = os.getenv("GROQ_API_KEY")
google_api_key = os.getenv("GOOGLE_API_KEY")

st.title("Gemma Model Document Q&A App")

llm = ChatGroq(groq_api_key=groq_api_key, model_name="gemma2-9b-it")

prompt = ChatPromptTemplate.from_template(
    """
    Answer the question based on the provided context.
    Context: {context}
    Question: {input}
    """
)

def vector_embedding():

    if "vectors" not in st.session_state:
        st.session_state.embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001", google_api_key=google_api_key)
        st.session_state.loader = PyPDFDirectoryLoader("./us_census")
        st.session_state.docs = st.session_state.loader.load()
        st.session_state.text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        st.session_state.documents = st.session_state.text_splitter.split_documents(st.session_state.docs)
        st.session_state.vectors = FAISS.from_documents(st.session_state.documents, st.session_state.embeddings)

prompt1 = st.text_input("Ask a question about the documents")

if st.button("Creating Vector Store"):
    vector_embedding()
    st.write("Vector Store Created")

import time

if prompt1:
    document_chain = create_stuff_documents_chain(llm, prompt)
    retriever = st.session_state.vectors.as_retriever()
    retrieval_chain = create_retrieval_chain(retriever, document_chain)

    start = time.process_time()
    response = retrieval_chain.invoke({"input": prompt1})
    st.write(response['answer'])

    with st.expander("Document Similarity Search"):
        for i, doc in enumerate(response["context"]):
            st.write(doc.page_content)
            st.write("--------------------------------")

    print("Response time: --- %s seconds ---" % (time.process_time() - start))
