# query/app.py

import streamlit as st
from rag_chain import load_vectorstore, build_rag_chain

# Load components
vectorstore = load_vectorstore()
rag_chain = build_rag_chain(vectorstore)

# UI
st.set_page_config(page_title="AutoLegal AI", page_icon="⚖️")
st.title("🤖 AutoLegal: NDA Chatbot")

query = st.text_input("Ask a question about your document:")
if query:
    with st.spinner("Thinking..."):
        answer = rag_chain.invoke(query)
        st.markdown("### 📄 Answer:")
        st.write(answer)
