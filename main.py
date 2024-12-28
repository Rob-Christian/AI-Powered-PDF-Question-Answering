# Import necessary libraries
import streamlit as st
import langchain
import os
import PyPDF2
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain import OpenAI
from langchain.chains import RetrievalQA

# Retrieve OpenAI key
OPENAI_API_KEY = st.secrets["key"]
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

# Function to extract text from PDF
def pdf_to_text(files):
  text = []
  for file in files:
    pdf_reader = PyPDF2.PdfReader(file)
    for i in pdf_reader.pages:
      text.append(pdf_reader.pages[i].extract_text)
  return text

# Customize PDF Question Answering
st.set_page_config(layout = "centered", page_title = "Retrieval-based QA")
st.header("AI-PoweredPDF Question Answering")
st.write("---")

# File to upload
upload_files = st.file_uploader("Upload up to 3 PDF Documents", accept_multiple_files = True, type = ['pdf'])

# Check file upload status
if upload_files:
  if len(upload_files) > 3:
    st.warning("You can only upload up to 3 files")
    upload_files = upload_files[:3]
  else:
    st.success(f"{len(upload_files)} document(s) ready for processing")


sample = pdf_to_text(upload_files)
st.write(sample)







