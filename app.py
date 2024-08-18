import streamlit as st

from pdf_to_image import pdf_to_image
from image_to_text import image_to_text
from mirascope_extractor import extractor

import google.generativeai as genai
import pandas as pd

import glob
import os
from dotenv import load_dotenv
import streamlit as st
# import subprocess

# Example installation command (adjust based on your environment)
# subprocess.run(['apt-get', 'install', 'tesseract-ocr'])


load_dotenv()

global empty_df
openai_api_key = os.getenv('OPENAI_API_KEY')
genai.configure(api_key=openai_api_key)


# Verify that Poppler is installed and in PATH

# folder_name = "/project/workspace/pdfs"
# invoice_pdfs = glob.glob(os.path.join(folder_name, '*.pdf')) + glob.glob(os.path.join(folder_name, '*.PDF'))
# print(f'Invoices_pdfs: {invoice_pdfs}')

st.set_page_config(page_title="Invoice Extractor")
st.title("Gen AI Invoice Extraction")
uploaded_files = st.file_uploader("Choose PDF files", accept_multiple_files=True, type="pdf")
if uploaded_files:
    # st.write(f'This is {uploaded_files}')
    if st.button('Extract'):
        image_bytes = pdf_to_image(uploaded_files)
        
        all_texts = []
        for image_byte in image_bytes:
          text = image_to_text(image_byte)
          all_texts.append(text)
          print('one text appended')
        
        empty_df = pd.DataFrame()
        
        for text in all_texts:
            extracted_text = extractor(text)
            task_details_dict = extracted_text.dict()
            df = pd.DataFrame([task_details_dict])
            empty_df = pd.concat([empty_df, df])

        st.write(empty_df)
        csv = empty_df.to_csv(index=False)
        st.download_button(
            label = 'Click to Download CSV',
            data = csv,
            file_name = 'Extracted_data.csv',
            mime='text/csv',
        )
        
