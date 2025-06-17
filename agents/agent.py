# agent/agent.py

from langchain.agents import initialize_agent, AgentType
from langchain_ollama import OllamaLLM
from query.tool import PDFIngestTool
from tools.live_legal_data.tool import LegalDatasetTool

def create_legal_agent(model_name="llama3.2"):
    tools = [PDFIngestTool, LegalDatasetTool]
    llm = OllamaLLM(model=model_name)

    agent = initialize_agent(
        tools=tools,
        llm=llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True,
    )
    return agent
