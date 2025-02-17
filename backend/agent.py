from langchain.tools import Tool
from langchain.memory import ConversationBufferMemory
from langchain.agents import initialize_agent, AgentType
import streamlit as st
from langchain_community.llms import Ollama
from metrics_operations import check_degraded_pgs, check_recent_osd_crashes, get_cluster_health, get_diskoccupation, get_high_latency_osds
from agno.storage.agent.postgres import PostgresAgentStorage


# Define Tools
tools = [
    Tool(name="Get disk occupation", func=get_diskoccupation, description="Fetches the disk occupation per node."),
    Tool(name="Check degraded PGs", func=check_degraded_pgs, description="Checks degraded PGs."),
    Tool(name="Check recent OSD crashes", func=check_recent_osd_crashes, description="Checks recent OSD crashes."),
    Tool(name="Check cluster health", func=get_cluster_health, description="Check cluster health"),
    Tool(name="Check high latency OSDs", func=get_high_latency_osds, description="Check high latency OSDs")
]

# Memory for Conversation
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

chat_history = memory.load_memory_variables({}).get("chat_history", [])
if not isinstance(chat_history, list):
    chat_history = []

# Language Model 
'''llm = InferenceClient(
    model="mistralai/Mistral-7B-Instruct-v0.1",
    token=HUGGINGFACEHUB_API_TOKEN
)'''
llm = Ollama(model="llama3")

def query_llm(prompt: str):
    return llm.text_generation(prompt, max_new_tokens=100)

db_url = 'postgresql://postgres:postgres@localhost:5432/postgres'

storage = PostgresAgentStorage(
    # store sessions in the ai.sessions table
    table_name="agent_sessions",
    # db_url: Postgres database URL
    db_url=db_url,
)

# Initialize AI Agent
agent = initialize_agent(
    storage=storage,
    tools=tools,
    llm=llm,
    agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION,
    memory=memory,
    verbose=True,
    handle_parsing_errors=True
)

def process_query(query: str):
    return agent.run(query)

def main_agentic_streamlit():
    # Streamlit UI Configuration
    st.set_page_config(page_title="CICD Chatbot (Agentic)", page_icon="🤖")
    st.markdown("<h1 style='text-align: center;'>🤖 Welcome to CICD Chatbot!</h1>", unsafe_allow_html=True)

    # User input
    prompt = st.chat_input("Type your command (e.g., trigger job, last build summary)...")

    if prompt:
        with st.spinner("Thinking..."):
            response = process_query(prompt)
            st.write(response)

def main_agentic():
    while True:
        query = input("\n💬 Enter command: ").strip()
        if query.lower() == "exit":
            print("👋 Exiting agent...")
            break
        
        response = process_query(query)
        print(response)


if __name__ == "__main__":
    # main_agentic_streamlit()
    main_agentic()

