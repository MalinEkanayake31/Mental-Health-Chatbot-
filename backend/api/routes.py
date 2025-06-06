from fastapi import APIRouter, Request
from backend.rag.llm_response import get_chat_response
from journal.save_journal import save_query

router = APIRouter()

@router.post("/ask")
async def ask_bot(req: Request):
    data = await req.json()
    query = data["query"]
    history = data.get("history", [])
    tone = data.get("tone", "Supportive")
    length = data.get("length", "Short")
    emotion = data.get("emotion", "😊")  # New field

    response = await get_chat_response(query, history, tone, length, emotion)
    save_query(query, response, emotion)
    return {"response": response}
