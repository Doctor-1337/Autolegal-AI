import streamlit as st
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_ollama.embeddings import OllamaEmbeddings
from langchain import hub
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from tempfile import NamedTemporaryFile
from langchain_community.llms import Ollama
import os


# UI: Title
st.title("📄 Chat with your PDF - Local RAG with Ollama")

# UI: Upload file
uploaded_file = st.file_uploader("Upload a PDF file", type="pdf")

# Model configuration
MODEL_NAME = "llama3.2"  

# Helper: Format docs for prompt
def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

persist_directory = "../ingest/db"

def load_preloaded_vectorstore():
    if os.path.exists(persist_directory):
        embeddings = OllamaEmbeddings(model=MODEL_NAME)
        return Chroma(persist_directory=persist_directory, embedding_function=embeddings)
    return None

if uploaded_file:
    st.info("📑 Loading and processing the PDF...")
    with NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
        tmp_file.write(uploaded_file.read())
        tmp_pdf_path = tmp_file.name

    loader = PyPDFLoader(tmp_pdf_path)
    documents = loader.load()

    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150)
    chunks = splitter.split_documents(documents)

    embeddings = OllamaEmbeddings(model=MODEL_NAME)
    vectordb = Chroma.from_documents(documents=chunks, embedding=embeddings)

else:
    vectordb = load_preloaded_vectorstore()
    if vectordb:
        st.info("📂 Using preloaded PDF vectorstore.")
    else:
        st.warning("⚠️ Please upload a PDF file to begin.")
        st.stop()

# Setup RAG Chain (moved outside the condition)
retriever = vectordb.as_retriever()
prompt = hub.pull("rlm/rag-prompt")
llm = Ollama(model=MODEL_NAME)
llm_chain = (
    {
        "context": retriever | format_docs,
        "question": RunnablePassthrough()
    }
    | prompt
    | llm
    | StrOutputParser()
)

# UI: Question input (shown always if vectordb is ready)
query = st.text_input("Ask something about the document:")
if query:
    with st.spinner("🧠 Thinking..."):
        response = llm_chain.invoke(query)
    st.markdown("**Answer:**")
    st.write(response)