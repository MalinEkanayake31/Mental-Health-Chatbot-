import os
import httpx
from dotenv import load_dotenv
from .retriever import get_retriever

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = os.getenv("GROQ_MODEL")
retriever = get_retriever()


async def get_chat_response(user_query, chat_history):
    docs = retriever.get_relevant_documents(user_query)
    context = "\n\n".join([doc.page_content for doc in docs])

    messages = [{"role": "system", "content": "You are a compassionate mental health support assistant."}]

    for pair in chat_history:
        messages.append({"role": "user", "content": pair["user"]})
        messages.append({"role": "assistant", "content": pair["bot"]})

    messages.append({"role": "user", "content": f"Context:\n{context}\n\nQuestion:\n{user_query}"})

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": GROQ_MODEL,
        "messages": messages
    }

    async with httpx.AsyncClient() as client:
        response = await client.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=payload)

    result = response.json()
    return result["choices"][0]["message"]["content"]
