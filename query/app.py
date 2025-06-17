import streamlit as st
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_ollama.embeddings import OllamaEmbeddings
from langchain import hub
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from tempfile import NamedTemporaryFile
import os

import sys
# Add project root (autolegal-ai/) to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from query.tool import PDFIngestTool

import streamlit as st
from tempfile import NamedTemporaryFile
from query.tool import store_pdf_text_for_agent  # You need to create this helper

from agents.agent import create_legal_agent



MODEL_NAME = "llama3.2"

st.title("📚 Legal Assistant - Powered by Local Agent")

uploaded_file = st.file_uploader("Upload a PDF file", type="pdf")

agent = create_legal_agent(model_name=MODEL_NAME)

if uploaded_file:
    st.info("📑 Processing uploaded PDF...")
    with NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
        tmp_file.write(uploaded_file.read())
        tmp_pdf_path = tmp_file.name

    # You can implement a helper that stores the PDF content in a global state or vector DB
    # so that PDFIngestTool can access it later
    store_pdf_text_for_agent(tmp_pdf_path)

    st.success("✅ PDF content ingested successfully.")

elif not os.path.exists("../ingest/db"):
    st.warning("⚠️ Please upload a PDF to begin.")
    st.stop()

query = st.text_input("Ask a legal question (based on PDF or case law):")

if query:
    with st.spinner("🧠 Thinking..."):
        response = agent.invoke(query)
    st.markdown("**Answer:**")
    st.write(response)