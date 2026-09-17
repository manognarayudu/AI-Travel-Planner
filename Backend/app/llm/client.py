import os

from langchain_openai import ChatOpenAI


OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

if not OPENROUTER_API_KEY:
    raise RuntimeError("OPENROUTER_API_KEY environment variable is not set")


llm = ChatOpenAI(
    model="nex-agi/nex-n2.5-pro:free",
    temperature=0,
    api_key=OPENROUTER_API_KEY,
    base_url="https://openrouter.ai/api/v1",
    default_headers={
        "HTTP-Referer": "https://ai-travel-planner-i57s5rne7-manognya.vercel.app",
        "X-Title": "AI Travel Planner",
    },
)