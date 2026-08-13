from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

import streamlit as st
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# OpenAI API Key
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

# LangSmith Tracking
if os.getenv("LANGCHAIN_API_KEY"):
    os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")
    os.environ["LANGCHAIN_TRACING_V2"] = "true"

# -----------------------------
# Creating Prompt
# -----------------------------

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a helpful assistant. Please respond to the user queries."
        ),
        (
            "user",
            "Question: {question}"
        )
    ]
)

# -----------------------------
# Streamlit UI
# -----------------------------

st.title("LangChain Chatbot")

input_text = st.text_input("Enter your question here")

# -----------------------------
# OpenAI LLM
# -----------------------------

llm = ChatOpenAI(
    model="gpt-3.5-turbo",
    temperature=0
)

# -----------------------------
# Output Parser
# -----------------------------

output_parser = StrOutputParser()

# -----------------------------
# Chain Creation
# -----------------------------

chain = prompt | llm | output_parser

# -----------------------------
# Generate Response
# -----------------------------

if input_text:
    response = chain.invoke(
        {
            "question": input_text
        }
    )

    st.write(response)