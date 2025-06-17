# query/rag_chain.py

from langchain.vectorstores import Chroma
from langchain_ollama.embeddings import OllamaEmbeddings
from langchain import hub
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_community.llms import Ollama

# Load vector DB
def load_vectorstore(persist_directory="../ingest/db"):
    embedding = OllamaEmbeddings(model="llama3.2")
    return Chroma(persist_directory=persist_directory, embedding_function=embedding)

# Format retrieved docs
def format_docs(docs):
    return "\n\n".join(d.page_content for d in docs)

# Build RAG chain
def build_rag_chain(vectorstore, model_name="llama3.2"):
    llm = Ollama(model=model_name)
    prompt = hub.pull("rlm/rag-prompt")
    
    rag_chain = (
        {
            "context": vectorstore.as_retriever() | format_docs,
            "question": RunnablePassthrough(),
        }
        | prompt
        | llm
        | StrOutputParser()
    )
    return rag_chain
