# agent/agent.py

from langchain.agents import initialize_agent, AgentType
from langchain_ollama import OllamaLLM
from query.tool import PDFIngestTool
from tools.live_legal_data.tool import LegalDatasetTool
from langchain.memory import ConversationBufferMemory


def create_legal_agent(model_name="llama3.2"):
    tools = [PDFIngestTool(), LegalDatasetTool]
    llm = OllamaLLM(model=model_name)

    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    agent_kwargs = {
        "prefix": """You are a legal assistant agent.
You can use the following tools:
- PDFIngestTool: Ask questions from uploaded PDFs.
- LegalDatasetTool: Ask about legal concepts or cases.

When using a tool, only pass a plain string as input.
❗Do NOT use function-like syntax such as Tool(query="...").
Just do:
Action: LegalDatasetTool
Action Input: "breach of contract"
"""
    }

    agent = initialize_agent(
        tools=tools,
        llm=llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True,
        handle_parsing_errors=True,
        max_iterations=12,
        memory=memory,
        agent_kwargs=agent_kwargs
    )
    
    return agent
