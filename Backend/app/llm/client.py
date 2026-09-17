from langchain_ollama import ChatOllama


# Local Ollama LLM
llm = ChatOllama(
    model="llama3.2:3b",
    temperature=0,
)