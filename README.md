# AI-Powered PDF Question Answering

This project is a Streamlit-based application that enables users to upload up to three PDF documents and ask retrieval-based questions about their content. The application uses the LangChain framework and OpenAI embeddings and Retrieval to process the PDF files and provide accurate answers with sources.

---

## Features

- **PDF Upload:** Upload up to three PDF documents for review and analysis.
- **Text Extraction:** Extracts text from the uploaded PDF files.
- **Embeddings Generation:** Converts text into embeddings using OpenAI's text-embedding-ada-002 model.
- **Vector Store:** Stores text with associated metadata in a Chroma vector database.
- **Question Answering:** Uses OpenAI's GPT-3.5-turbo model for generating and answering questions based on the content of the uploaded PDFs.

---

## Requirements

- Python 3.8 or higher
- Streamlit
- LangChain
- PyPDF2
- OpenAI version 0.28
- chromadb version 0.3.29
- OpenAI API Key

---

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/Rob-Christian/AI-Powered-PDF-Question-Answering.git
   cd pdf-reviewer-qa

2. Install packages
   ```bash
   pip install -r requirements.txt

3. Add your OpenAI API key
