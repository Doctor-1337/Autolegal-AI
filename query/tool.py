from langchain.tools import Tool
from query.rag_chain import load_vectorstore, build_rag_chain

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
    description="Use this to ask questions from the ingested PDF documents using semantic search. Example: 'What are the clauses in the Hindu Marriage Act?'"
)
