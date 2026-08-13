#from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_ollama import OllamaLLM
import streamlit as st
import os
from dotenv import load_dotenv

load_dotenv()


# langsmith Tacking
langchain_api_key = os.getenv("LANGCHAIN_API_KEY")

if langchain_api_key:
    os.environ["LANGCHAIN_API_KEY"] = langchain_api_key
    os.environ["LANGCHAIN_TRACING_V2"] = "true"
    os.environ["LANGCHAIN_PROJECT"] = "llama2-streamlit-chatbot"

# Creating Chatbot

prompt=ChatPromptTemplate.from_messages(
    [
        ("system","You are a helpful assistant. Please respond to the user queries"),
        ("user","Question:{question}")
    ]
)

# Streamlit Framework
 
st.title("LangChain Chatbot with Llama 2")
st.write("Ask anything to your local Llama 2 model.")


input_text = st.text_input("Enter your question here:")

# Open AI LLM call
llm = OllamaLLM(model="llama2")
output_parser=StrOutputParser()

# Chain Creation
chain=prompt|llm|output_parser

if input_text:
    st.write(chain.invoke({'question':input_text}))