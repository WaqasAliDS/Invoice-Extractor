from pdf_to_image import pdf_to_image
from image_to_text import image_to_text
from mirascope_extractor import extractor

import google.generativeai as genai
import pandas as pd

import glob
import os
from dotenv import load_dotenv
import streamlit as st
load_dotenv()









global empty_df
openai_api_key = os.getenv('OPENAI_API_KEY')
genai.configure(api_key=openai_api_key)

folder_name = "/project/workspace/pdfs"
invoice_pdfs = glob.glob(os.path.join(folder_name, '*.pdf')) + glob.glob(os.path.join(folder_name, '*.PDF'))
print(f'Invoices_pdfs: {invoice_pdfs}')

for pdf_path in invoice_pdfs:
  convert_image = pdf_to_image(pdf_path)
  convert_image.save_image(f'{pdf_path}image')
  print('one_pdf_converted')

all_images = glob.glob(os.path.join(folder_name, '*.jpg'))
all_texts = []
for image_path in all_images:
  text = image_to_text(image_path)
  all_texts.append(text)
  print('one text appended')

empty_df = pd.DataFrame()

for text in all_texts:
    extracted_text = extractor(text)
    task_details_dict = extracted_text.dict()
    df = pd.DataFrame([task_details_dict])
    empty_df = pd.concat([empty_df, df])


empty_df.to_csv('extracted_data.csv')









