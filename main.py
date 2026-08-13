import streamlit as st
import os
import requests

from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_ollama import ChatOllama

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser


# =========================================================
# LOAD ENVIRONMENT VARIABLES
# =========================================================

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
LANGCHAIN_API_KEY = os.getenv("LANGCHAIN_API_KEY")
LANGCHAIN_PROJECT = os.getenv(
    "LANGCHAIN_PROJECT",
    "QA_Chatbot"
)


# =========================================================
# LANGSMITH
# =========================================================

if LANGCHAIN_API_KEY:

    os.environ["LANGCHAIN_API_KEY"] = LANGCHAIN_API_KEY
    os.environ["LANGCHAIN_TRACING_V2"] = "true"
    os.environ["LANGCHAIN_PROJECT"] = LANGCHAIN_PROJECT


# =========================================================
# STREAMLIT CONFIG
# =========================================================

st.set_page_config(
    page_title="QA Chatbot",
    page_icon="🤖",
    layout="centered"
)


# =========================================================
# CHECK OLLAMA SERVER
# =========================================================

def check_ollama():

    try:

        response = requests.get(
            "http://localhost:11434/api/tags",
            timeout=2
        )

        if response.status_code == 200:
            return True

        return False

    except requests.exceptions.RequestException:

        return False


ollama_available = check_ollama()


# =========================================================
# TITLE
# =========================================================

st.title("🤖 QA Chatbot")

st.write(
    "Ask questions using OpenAI or a locally hosted Ollama model."
)


# =========================================================
# MODEL SELECTION
# =========================================================

model_choice = st.selectbox(
    "Choose your LLM:",
    [
        "OpenAI",
        "Ollama"
    ]
)


# =========================================================
# OLLAMA STATUS
# =========================================================

if model_choice == "Ollama":

    if ollama_available:

        st.success(
            "🦙 Ollama is available."
        )

    else:

        st.warning(
            "⚠️ Ollama is not available in this environment."
        )

        st.info(
            "Ollama is only available when an Ollama "
            "server is accessible. It cannot connect "
            "to your local PC from Streamlit Cloud."
        )

        st.stop()


# =========================================================
# PROMPT
# =========================================================

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
            You are a helpful AI assistant.

            Answer the user's questions clearly,
            accurately, and concisely.
            """
        ),

        (
            "user",
            "{question}"
        )
    ]
)


# =========================================================
# SELECT LLM
# =========================================================

if model_choice == "OpenAI":

    if not OPENAI_API_KEY:

        st.error(
            "OPENAI_API_KEY is not configured."
        )

        st.stop()

    llm = ChatOpenAI(
        model="gpt-3.5-turbo",
        temperature=0
    )


elif model_choice == "Ollama":

    llm = ChatOllama(
        model="llama3.2",
        temperature=0
    )


# =========================================================
# OUTPUT PARSER
# =========================================================

output_parser = StrOutputParser()


# =========================================================
# CHAIN
# =========================================================

chain = prompt | llm | output_parser


# =========================================================
# USER QUESTION
# =========================================================

input_text = st.text_input(
    "Enter your question:"
)


# =========================================================
# GENERATE RESPONSE
# =========================================================

if input_text:

    try:

        with st.spinner(
            f"Generating response using {model_choice}..."
        ):

            response = chain.invoke(
                {
                    "question": input_text
                }
            )

        st.subheader("Answer")

        st.write(response)

    except Exception as e:

        st.error(
            f"Error: {str(e)}"
        )