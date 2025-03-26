import os
from dotenv import load_dotenv
from langchain.schema import HumanMessage, AIMessage
import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from PyPDF2 import PdfReader
from PIL import Image
import io

load_dotenv()

llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro-latest", google_api_key="AIzaSyCC-B1PFwUKg6c4ryvQh_QhjCex3bYxSsA")

st.set_page_config(page_title="Chatbot", page_icon="💬", layout="wide")

col1, col2 = st.columns([1, 3])

with col1:
    st.sidebar.title("Upload Files")
    uploaded_file = st.sidebar.file_uploader("Upload a document (PDF, TXT) or an image", type=["pdf", "txt", "png", "jpg", "jpeg"])
    
    if uploaded_file is not None:
        file_type = uploaded_file.type
        if "pdf" in file_type:
            pdf_reader = PdfReader(uploaded_file)
            text = "\n".join([page.extract_text() for page in pdf_reader.pages if page.extract_text()])
            st.session_state["uploaded_text"] = text
            st.sidebar.success("PDF uploaded and processed successfully!")
        elif "text" in file_type:
            text = uploaded_file.read().decode("utf-8")
            st.session_state["uploaded_text"] = text
            st.sidebar.success("Text file uploaded and processed successfully!")
        elif "image" in file_type:
            image = Image.open(uploaded_file)
            st.session_state["uploaded_image"] = image
            st.sidebar.image(image, caption="Uploaded Image", use_column_width=True)

with col2:
    st.title("Langchain Chatbot")
    st.subheader("Conversational AI with File Processing")
    
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    chat_container = st.container()
    with chat_container:
        for message in st.session_state.chat_history:
            if isinstance(message, HumanMessage): 
                st.markdown(f"**🧑 You:** {message.content}")
            else:
                st.markdown(f"**🤖 Bot:** {message.content}")

    user_input = st.text_input("Ask me anything", key="user_input")

    def chatbot_response(user_input):
        st.session_state.chat_history.append(HumanMessage(content=user_input))
        context = st.session_state.get("uploaded_text", "")
        response = llm.invoke([HumanMessage(content=context + "\n\n" + user_input)])
        st.session_state.chat_history.append(AIMessage(content=response.content))
        return response.content

    if st.button("Send"):
        st.session_state.text_input = ""
        if user_input:
            response = chatbot_response(user_input)
            st.experimental_rerun()
