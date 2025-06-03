import os
import httpx
from dotenv import load_dotenv
from .retriever import get_retriever

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = os.getenv("GROQ_MODEL")
retriever = get_retriever()


async def get_chat_response(user_query, history=None, tone="Supportive", length="Short"):
    docs = retriever.get_relevant_documents(user_query)
    context = "\n\n".join([doc.page_content for doc in docs])

    tone_instruction = f"Respond in a {tone.lower()} tone."
    length_instruction = "Keep the response brief." if length == "Short" else "Provide a detailed explanation."

    prompt = f"""You are a mental health assistant.
Use the following verified context to answer empathetically.

{tone_instruction} {length_instruction}

Context:
{context}

Question:
{user_query}

Answer:"""

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": GROQ_MODEL,
        "messages": [
            {"role": "system", "content": "You are a compassionate mental health support assistant."},
            {"role": "user", "content": prompt}
        ]
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers=headers,
            json=payload
        )

    result = response.json()
    return result["choices"][0]["message"]["content"]

