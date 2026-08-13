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
LANGCHAIN_PROJECT = os.getenv("LANGCHAIN_PROJECT", "QA_Chatbot")


# =========================================================
# LANGSMITH CONFIGURATION
# =========================================================

if LANGCHAIN_API_KEY:
    os.environ["LANGCHAIN_API_KEY"] = LANGCHAIN_API_KEY
    os.environ["LANGCHAIN_TRACING_V2"] = "true"
    os.environ["LANGCHAIN_PROJECT"] = LANGCHAIN_PROJECT


# =========================================================
# STREAMLIT CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="QA Chatbot",
    page_icon="🤖",
    layout="centered"
)


# =========================================================
# CHECK OLLAMA
# =========================================================

def is_ollama_available():

    try:
        response = requests.get(
            "http://localhost:11434/api/tags",
            timeout=2
        )

        return response.status_code == 200

    except Exception:
        return False


ollama_available = is_ollama_available()


# =========================================================
# TITLE
# =========================================================

st.title("🤖 QA Chatbot")

st.write(
    "Ask questions using OpenAI or a locally hosted Ollama model."
)


# =========================================================
# MODEL OPTIONS
# =========================================================

model_options = ["OpenAI"]

if ollama_available:
    model_options.append("Ollama")


model_choice = st.selectbox(
    "Choose your LLM:",
    model_options
)


# =========================================================
# SHOW OLLAMA STATUS
# =========================================================

if ollama_available:

    st.success(
        "🦙 Ollama is available. "
        "You can use a local Ollama model."
    )

else:

    st.info(
        "🦙 Ollama is not available. "
        "Running in cloud mode or Ollama is not running locally."
    )


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
# INITIALIZE LLM
# =========================================================

llm = None


if model_choice == "OpenAI":

    if not OPENAI_API_KEY:

        st.error(
            "OPENAI_API_KEY is not configured."
        )

        st.info(
            "Add OPENAI_API_KEY to your .env file "
            "when running locally or Streamlit Secrets "
            "when deployed."
        )

        st.stop()

    llm = ChatOpenAI(
        model="gpt-3.5-turbo",
        temperature=0
    )


elif model_choice == "Ollama":

    if not ollama_available:

        st.error(
            "Ollama is not available."
        )

        st.stop()

    llm = ChatOllama(
        model="llama3.2",
        temperature=0
    )


# =========================================================
# OUTPUT PARSER
# =========================================================

output_parser = StrOutputParser()


# =========================================================
# CREATE CHAIN
# =========================================================

chain = prompt | llm | output_parser


# =========================================================
# USER INPUT
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