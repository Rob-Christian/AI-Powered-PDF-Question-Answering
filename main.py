# Import necessary libraries
import streamlit as st
import langchain
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.openai.embeddings import OpenAIEmbeddings
from langchain.openai.chat_models import ChatOpenAI
