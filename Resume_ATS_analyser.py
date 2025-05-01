from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import os
from PIL import Image
import pdf2image
import google.generativeai as genai
import io, base64

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input, pdf_content, prompt):
    model = genai.GenerativeModel('gemini-2.5-flash-preview-04-17')
    response = model.generate_content([input, pdf_content[0], prompt])
    return response.text

def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
        images = pdf2image.convert_from_bytes(uploaded_file.read())
        first_page = images[0]

        # Convert to bytes
        img_byte_arr = io.BytesIO()
        first_page.save(img_byte_arr, format='JPEG')
        img_byte_arr = img_byte_arr.getvalue()
        pdf_parts = [ { "mime_type": "image/jpeg", "data": base64.b64encode(img_byte_arr).decode() } ]
        return pdf_parts
    else:
        raise FileNotFoundError("No file uploaded")

## Stramlit App

st.set_page_config(page_title="ATS Resume Analyzer")
st.header("ATS Tracking System")
input_text = st.text_area("Job Description: ", key="input")
uploaded_file = st.file_uploader("Upload your resume (PDF)...", type=["pdf"])

if uploaded_file is not None:
    st.write("PDF Uploaded Successfully")

submit1 = st.button("Tell Me About the Resume")
submit2 = st.button("How Can I Improvise my Skills")
submit3 = st.button("Percentage match")
submit4 = st.button("What are the keywords that are missing")

input_prompt1 = """
You are an experienced Technical Human Resource Manager with a deep understanding of the technical aspects of recruitment and hiring. Your task is to review the provided resume in detail. 
Please share your professional evaluation of the candidate, highlighting their technical expertise and match with the given job description. 
Highlight missing keywords with technical skills and highlight the additional ones as well.
"""

input_prompt2 = """
You are an experienced Technical Human Resource Manager with a deep understanding of the technical aspects of recruitment and hiring. Your task is to review the provided resume in detail. 
Within 3-4 lines, please evaluate the candidate's professional experience, technical skills, and overall suitability for the role. 
Focus on identifying areas where the candidate's technical skills align with the required skills for the job.
"""


input_prompt3 = """
You are an expert with and Deep ATS functionality with a deep understanding of the technical aspects of recruitment and hiring. Your task is to review the provided resume in detail. 
please evaluate the candidate's professional experience, technical skills, and overall suitability for the role. 
provide the percentage match 
"""

input_prompt4 = """
You are an experienced Technical Human Resource Manager with a deep understanding of the technical aspects of recruitment and hiring. Your task is to review the provided resume in detail. 
Please share your professional evaluation of the candidate, highlighting their technical expertise and match with the given job description. 
Highlight missing keywords with technical skills and highlight the additional ones as well.
"""


if submit1:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_prompt1, pdf_content, input_text)
        st.subheader("The Response is")
        st.write(response)
    else:
        st.write("Please upload the resume")

if submit2:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_prompt2, pdf_content, input_text)
        st.subheader("The Response is")
        st.write(response)
    else:
        st.write("Please upload the resume")

if submit3:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_prompt3, pdf_content, input_text)
        st.subheader("The Response is")
        st.write(response)
    else:
        st.write("Please upload the resume")

if submit4:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_prompt4, pdf_content, input_text)
        st.subheader("The Response is")
        st.write(response)
    else:
        st.write("Please upload the resume")





