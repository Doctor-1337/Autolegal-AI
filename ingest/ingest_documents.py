import os
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_ollama.embeddings import OllamaEmbeddings
from langchain_chroma import Chroma
from dotenv import load_dotenv


def load_pdf(file_path):
    loader = PyPDFLoader(file_path)
    return loader.load()

def split_document(documents):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=150
    )
    return splitter.split_documents(documents)

def embed_and_store(docs, persist_directory="db"):
    embedding = OllamaEmbeddings(model="llama3.2")
    vectordb = Chroma.from_documents(documents=docs,embedding=embedding,persist_directory=persist_directory)

if __name__ == "__main__":
    file_path = "doc_source/nda_doc.pdf"
    docs = load_pdf(file_path)
    chunks = split_document(docs)
    embed_and_store(chunks)
    print(f"Ingestion complete : {len(chunks)} chunks stored.")