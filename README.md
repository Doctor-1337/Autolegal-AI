📘 Overview

AutoLegal-AI is a Streamlit-based application that enables users to ask legal questions based on uploaded PDF documents (such as legal agreements or court decisions) and retrieves context-aware answers using Retrieval-Augmented Generation (RAG). It also allows searching through case law data using tools integrated into a LangChain agent.

🎯 Key Features

PDF Upload and Processing: Upload legal documents or use a preloaded one.

RAG-Based Retrieval: Query the document using semantic search with a vector store.

LangChain Agent: Uses tools like PDFIngestTool and LegalDatasetTool to determine the best path for query resolution.

Legal Dataset Search: Uses LexGLUE (ECHR case law) for real-world case references.

Memory Support: Maintains multi-turn conversations using LangChain memory.

📊 Architecture Diagram

                           +--------------------------+
                           |      Streamlit UI        |
                           | - Upload PDF             |
                           | - Input Question         |
                           +-----------+--------------+
                                       |
                                       v
                           +-----------+--------------+
                           |        LangChain Agent   |
                           | - ZeroShotReAct          |
                           | - Memory (Chat History)  |
                           +-----------+--------------+
                                       |
                   +-------------------+-------------------+
                   |                                       |
        +----------v---------+                 +-----------v------------+
        |   PDFIngestTool    |                 |   LegalDatasetTool     |
        | - RAG from Vector  |                 | - LexGLUE (ECHR cases) |
        +----------+---------+                 +-----------+------------+
                   |                                       |
        +----------v---------------------------------------v-----------+
        |                        Response Synthesizer                  |
        +--------------------------------------------------------------+
                                       |
                                       v
                           +-----------+--------------+
                           |         Final Answer     |
                           +--------------------------+

🧰 Tech Stack

LangChain: For agent, tools, memory

Ollama: Local LLM (e.g., LLaMA 3)

ChromaDB: Vector store for document embeddings

LexGLUE (ECHR): Case law search

Streamlit: UI layer

Pydantic: Tool and memory configurations

🚀 Usage Instructions

Install Dependencies

pip install -r requirements.txt

Run Ollama in Background

ollama run llama3

Start Streamlit App

streamlit run query/app.py

Use the App

Upload a PDF or rely on the preloaded one

Ask legal queries (e.g., "What is the termination clause?")

Agent will decide whether to use PDF or legal dataset tool

🧠 Agent Tools

PDFIngestTool: Queries vector DB generated from PDF chunks

LegalDatasetTool: Searches LexGLUE (subset) for legal precedent