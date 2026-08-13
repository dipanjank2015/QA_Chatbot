import streamlit as st
import os

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


# =========================================================
# LANGSMITH CONFIGURATION
# =========================================================

if LANGCHAIN_API_KEY:
    os.environ["LANGCHAIN_API_KEY"] = LANGCHAIN_API_KEY
    os.environ["LANGCHAIN_TRACING_V2"] = "true"
    os.environ["LANGCHAIN_PROJECT"] = "OpenAI-Ollama-Chatbot"


# =========================================================
# STREAMLIT PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="OpenAI + Ollama Chatbot",
    page_icon="🤖",
    layout="centered"
)


# =========================================================
# TITLE
# =========================================================

st.title("🤖 OpenAI + Ollama Chatbot")

st.write(
    "Select a model and ask your question."
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
# PROMPT
# =========================================================

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a helpful AI assistant. "
            "Answer the user's questions clearly and accurately."
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
            "OPENAI_API_KEY is not found in your .env file."
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

        st.subheader("Response")

        st.write(response)

    except Exception as e:

        st.error(
            f"Error: {str(e)}"
        )