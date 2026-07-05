import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain.agents import create_agent
from langchain.tools import tool
from langchain_community.utilities import GoogleSerperAPIWrapper
from langgraph.checkpoint.memory import InMemorySaver 
import streamlit as st

load_dotenv()


search = GoogleSerperAPIWrapper()
tools = [search.run]
if "memory" not in st.session_state:
    st.session_state["memory"] = InMemorySaver()
    st.session_state.history = []

model = ChatGroq(
    groq_api_key=os.getenv("groq_api"),
    model="openai/gpt-oss-20b",
)

agent = create_agent(
    model=model,
    tools=tools,
    checkpointer=st.session_state.memory,
    system_prompt="You are a helpful assistant and can search google as well.",
    
)


st.title("Q&A Agent")
st.subheader("Ask a question")

query = st.chat_input("Ask your question here...")

for message in st.session_state.history:
    role = message["role"]
    content = message["content"]
    st.chat_message(role).markdown(content)

if query:
    st.chat_message("user").markdown(query)
    st.session_state.history.append({"role":"user","content":query})
    
    response = agent.stream(
        {"messages":[{"role":"user","content":query}]},
        {"configurable":{"thread_id":1}},
        stream_mode = "messages")

    ai_cont = st.chat_message("ai")

    with ai_cont:
        space = st.empty()
        message = ""
        for chunk in response:
            message = message + chunk[0].content
            space.write(message)
        st.session_state.history.append({"role":"assistant","content":message})
    
