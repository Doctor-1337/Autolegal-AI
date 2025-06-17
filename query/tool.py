from langchain.tools import Tool
from query.rag_chain import load_vectorstore, build_rag_chain
from langchain_core.tools import BaseTool
from typing import Optional

def pdf_ingest_tool_fn(query: str) -> str:
    try:
        vectorstore = load_vectorstore()
        rag_chain = build_rag_chain(vectorstore)
        return rag_chain.invoke(query)
    except Exception as e:
        return f"Error querying PDF: {str(e)}"

PDFIngestTool = Tool(
    name="PDFIngestTool",
    func=pdf_ingest_tool_fn,
    description="Use this to ask questions from the ingested PDF documents. Example: 'What is the termination clause in the agreement?'"
)

# query/tool.py

pdf_memory = {}  # simple global store; in production use a better cache

def store_pdf_text_for_agent(pdf_path):
    from langchain_community.document_loaders import PyPDFLoader
    from langchain.text_splitter import RecursiveCharacterTextSplitter

    loader = PyPDFLoader(pdf_path)
    documents = loader.load()
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150)
    chunks = splitter.split_documents(documents)
    all_text = "\n".join([chunk.page_content for chunk in chunks])
    
    pdf_memory["content"] = all_text

class PDFIngestTool(BaseTool):
    name: str = "PDFIngestTool"
    description: str = "Useful for answering questions from the uploaded PDF"

    def _run(self, query: str) -> str:
        if "content" not in pdf_memory:
            return "No PDF content available."
        content = pdf_memory["content"]
        if query.lower() in content.lower():
            return f"Found relevant content: {query}"
        return "Couldn't find relevant content in the PDF."
