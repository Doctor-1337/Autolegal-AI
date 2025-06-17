# query/query_documents.py

from rag_chain import load_vectorstore, build_rag_chain

rag_chain = build_rag_chain(load_vectorstore())

while True:
    q = input("Ask: ")
    if q.lower() in ["exit", "quit"]:
        break
    print(rag_chain.invoke(q))
