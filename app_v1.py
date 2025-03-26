import os
from dotenv import load_dotenv
from langchain.schema import HumanMessage, AIMessage
import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro-latest", google_api_key="AIzaSyCC-B1PFwUKg6c4ryvQh_QhjCex3bYxSsA")

st.set_page_config(page_title="Chatbot", page_icon="💬")

st.title("Langchain")
st.subheader("A simple language model for conversational AI")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

for message in st.session_state.chat_history:
    if isinstance(message, HumanMessage):
        st.markdown(f"**🧑 You:** {message.content}")
    else:
        st.markdown(f"**🤖 Bot:** {message.content}")

user_input = st.text_input("Ask me anything", key="user_input")

def chatbot_response(user_input):
    st.session_state.chat_history.append(HumanMessage(content=user_input))
    response = llm.invoke(st.session_state.chat_history)
    st.session_state.chat_history.append(AIMessage(content=response.content))
    return response.content

if st.button("Send"):
    if user_input:
        response = chatbot_response(user_input)
        st.experimental_rerun()
