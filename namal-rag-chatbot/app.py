import streamlit as st
import os
from utils.data_loader import load_namal_data
from utils.vector_store import create_vector_store
from utils.rag_chain import create_rag_response


st.set_page_config(
    page_title="Namal University AI Chatbot",
    page_icon="🎓",
    layout="centered"
)

st.title("🎓 Namal University AI Chatbot")

st.write("Ask anything about Namal University")


@st.cache_resource
def setup_chatbot():

    docs = load_namal_data("data/namal_data.json")
    
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    DATA_PATH = os.path.join(BASE_DIR, "data", "namal_data.json")

    docs = load_namal_data(DATA_PATH)

    vector_store = create_vector_store(docs)

    retriever = vector_store.as_retriever(
        search_kwargs={"k": 8}
    )

    return retriever


retriever = setup_chatbot()


if "messages" not in st.session_state:
    st.session_state.messages = []


# Display chat history
for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# User input
user_query = st.chat_input("Ask your question...")


if user_query:

    # Save user message
    st.session_state.messages.append({
        "role": "user",
        "content": user_query
    })

    # Show user message
    with st.chat_message("user"):
        st.markdown(user_query)

    # Retrieve docs
    retrieved_docs = retriever.invoke(user_query)

    # Generate AI response
    response = create_rag_response(
        user_query,
        retrieved_docs
    )

    # Show assistant response
    with st.chat_message("assistant"):
        st.markdown(response)

    # Save assistant response
    st.session_state.messages.append({
        "role": "assistant",
        "content": response
    })
