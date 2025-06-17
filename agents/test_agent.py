# agent/test_agent.py

from agents.agent import create_legal_agent

if __name__ == "__main__":
    agent = create_legal_agent()
    
    query = "What does the PDF say about indemnity? Also, are there any cases about breach of contract?"
    print("\n🤖 Answer:\n")
    result = agent.invoke(query)
    print(result)
