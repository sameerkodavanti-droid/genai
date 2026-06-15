from dotenv import load_dotenv
import os
import streamlit as st
from langchain_groq import ChatGroq
load_dotenv()


groq_api = os.getenv("groq_api")

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    groq_api_key=groq_api
)

#User Interface
st.title("Q&A Chatbot")
st.markdown("Basic Q&A Chatbot using LangChain and Groq")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    role=message["role"]
    content=message["content"]
    st.chat_message(role).markdown(content)

user_input = st.chat_input("Ask a question")
if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.chat_message("user").markdown(user_input)
    response = llm.invoke(user_input)
    st.chat_message("assistant").markdown(response.content)
    st.session_state.messages.append({"role": "assistant", "content": response.content})