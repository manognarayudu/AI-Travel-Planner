from app.llm.client import llm


response = llm.invoke(
    "Say hello and explain in one sentence what a travel planning AI does."
)


print(response.content)