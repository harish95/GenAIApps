import streamlit as st
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import google.generativeai as genai
from langchain.vectorstores import FAISS
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains.question_answering import load_qa_chain
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv


load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
    
    return text

def get_text_chunks(text):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=10000,
        chunk_overlap=1000,
        length_function=len
    )
    text_chunks = text_splitter.split_text(text)
    return text_chunks

def create_vector_store(text_chunks):
    embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-exp-03-07")
    vector_store = FAISS.from_texts(text_chunks, embeddings)
    vector_store.save_local("ChatWithPDF_faiss_index")
    return vector_store

def get_coversation_chain(vector_store):
    prompt_template = """Answer the question based on the context provided. If the answer is not in the context, say I don't know
    Context:\n {context} \n
    Question:\n {question} \n
    Answer: 
    """
    model = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0.3)
    prompt = PromptTemplate(template = prompt_template, input_variables=["context", "question"])
    chain = load_qa_chain(model, chain_type="stuff", prompt=prompt)
    return chain

def user_input(user_question):
    embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-exp-03-07")
    vector_store = FAISS.load_local("ChatWithPDF_faiss_index", embeddings,allow_dangerous_deserialization = True)
    docs = vector_store.similarity_search(user_question)
    chain = get_coversation_chain(vector_store)
    response = chain.run(input_documents=docs, question=user_question)
    return response

def main(): 
    st.title("Chat with PDF")
    st.write("Upload your PDF files to chat with them.")
    
    pdf_docs = st.file_uploader("Upload PDF files", type="pdf", accept_multiple_files=True)
    
    if pdf_docs:
        text = get_pdf_text(pdf_docs)
        text_chunks = get_text_chunks(text)
        
        if st.button("Create Vector Store"):
            vector_store = create_vector_store(text_chunks)
            st.success("Vector store created successfully!")
        
        user_question = st.text_input("Ask a question about the PDF:")
        
        if user_question and st.button("Get Answer"):
            response = user_input(user_question)
            st.write(response)

if __name__ == "__main__":
    main()
# This code is a Streamlit application that allows users to upload PDF files and ask questions about the content of those files.
# It uses LangChain and Google Generative AI to process the PDF files, create a vector store for efficient searching, and generate answers to user questions.
# The application includes functions for extracting text from PDFs, splitting the text into chunks, creating a vector store, and generating answers using a conversation chain.
# The main function sets up the Streamlit interface, allowing users to upload PDF files, create a vector store, and ask questions.
# The application is designed to be user-friendly and provides feedback on the status of the vector store creation and the answers to user questions.
# The code uses the PyPDF2 library to read PDF files, the langchain library for text processing and vector storage, and the dotenv library to manage environment variables.
# The application is built using Streamlit, a popular framework for creating web applications in Python.
# The code is structured to be modular, with separate functions for each major task, making it easy to maintain and extend.
# The application is designed to be run in a local environment, and it requires the user to have a Google API key for accessing the Google Ge