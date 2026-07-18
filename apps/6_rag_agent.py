import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.agents import create_agent
from langchain.tools import tool
from langgraph.checkpoint.memory import InMemorySaver
load_dotenv()

llm = ChatGroq(
    groq_api_key=os.getenv("groq_api"), 
    model="openai/gpt-oss-20b"
)

loader = PyPDFLoader("../data/support_manual.pdf")
documents = loader.load()

splitter = RecursiveCharacterTextSplitter(chunk_size=1000,chunk_overlap=200)
splitted_docs = splitter.split_documents(documents)

embedding = HuggingFaceEmbeddings(
    model_name="BAAI/bge-base-en-v1.5"
)

vector_store = Chroma.from_documents(documents=splitted_docs,embedding=embedding)


@tool
def retriver_tool(query:str):
    """ 
        This tool can help you to retrieve the relevant data of pdf documents, and these documents have
        details about support manual.
    """
    docs = vector_store.similarity_search(query=query,k=4)
    print("tool called",query)

    context = "\n\n".join(doc.page_content for doc in docs)
    return context

system_prompt = """
    You are a helpful assistant that answers questions using retrived context.
    ALWAYS use the `retriever_tool` tool for questions requiring external knowledge. 
"""

agent = create_agent(
    model=llm,
    system_prompt=system_prompt,
    tools=[retriver_tool],
    checkpointer=InMemorySaver(),
)

while True:
    query = input("You: ")
    if query.lower() == "exit":
        break
    response = agent.invoke({"messages": [{"role": "user", "content": query}]},{"configurable":{"thread_id":"1"}})
    print("Agent: ", response["messages"][-1].content)