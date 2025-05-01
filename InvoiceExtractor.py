from dotenv import load_dotenv
import os
import streamlit as st
from PIL import Image
import google.generativeai as genai

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

## function to load gemini pro vision model
model = genai.GenerativeModel('gemini-2.0-flash')

def get_gemini_response(input,image,prompt):
    """
    Function to get response from Gemini Pro Vision model
    """
    response = model.generate_content([input,image[0],prompt])

    return response.text

# intialize the streamlit app
st.set_page_config(page_title="Invoice Extractor", page_icon=":money_with_wings:")
st.title("Invoice Extractor")
st.write("This app extracts information from invoices using Google Gemini Pro Vision model.")
st.write("Upload an invoice image and get the extracted information.")
# upload the image
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='Uploaded Image.', use_column_width=True)

def input_image_setup(uploaded_file):
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        image_parts = [
            {
                "mime_type": uploaded_file.type,
                "data": bytes_data,
            }
        ]
        return image_parts
    else:
        raise ValueError("No image uploaded")


input = st.text_input("Enter the information you want to extract from the invoice:")

submit = st.button("Extract Information From Invoice")

input_prompt = """Your are an expert in extracting information from invoice. \n
            We have uploded am image of invoice. 
            Answer the following questions based on the image. \n"""


if submit:
    image_data = input_image_setup(uploaded_file)
    response = get_gemini_response(input_prompt, image_data, input)
    st.subheader("Extracted Information")
    st.write(response)
    st.write("Please check the extracted information and let us know if you have any questions.")
    st.write("Thank you for using the Invoice Extractor app!")





# Add a footer
st.markdown(
    """
    <style>
    footer {
        visibility: hidden;
    }
    </style>
    """,
    unsafe_allow_html=True,
)
