# 🤖 QA Chatbot — OpenAI & Ollama

An LLM-powered Question & Answer chatbot built using **LangChain and Streamlit**, supporting both **OpenAI API models** and **locally hosted Ollama models**.

The application allows users to select their preferred LLM and ask questions through a simple Streamlit interface.

---

## 🚀 Features

- 💬 Interactive Question & Answer chatbot
- 🤖 Support for OpenAI models
- 🦙 Support for locally hosted Ollama models
- 🔗 LangChain LCEL-based architecture
- 🧩 PromptTemplate / ChatPromptTemplate integration
- 📝 StrOutputParser for clean responses
- 🖥️ Streamlit web interface
- 🔐 Environment variable support for API keys
- 📊 Optional LangSmith tracing
- 🔄 Switch between OpenAI and Ollama from the same application

---

## 🏗️ Project Architecture

```text
                         User
                           │
                           ▼
                  ┌─────────────────┐
                  │    Streamlit    │
                  │   Web Interface │
                  └────────┬────────┘
                           │
                           ▼
                  ┌─────────────────┐
                  │  Model Selector │
                  └────────┬────────┘
                           │
                ┌──────────┴──────────┐
                │                     │
                ▼                     ▼
        ┌───────────────┐     ┌───────────────┐
        │    OpenAI     │     │    Ollama     │
        │  ChatOpenAI   │     │  ChatOllama   │
        └───────┬───────┘     └───────┬───────┘
                │                     │
                └──────────┬──────────┘
                           │
                           ▼
                  ┌─────────────────┐
                  │ ChatPromptTemplate│
                  └────────┬────────┘
                           │
                           ▼
                  ┌─────────────────┐
                  │      LLM        │
                  └────────┬────────┘
                           │
                           ▼
                  ┌─────────────────┐
                  │ StrOutputParser │
                  └────────┬────────┘
                           │
                           ▼
                       Response