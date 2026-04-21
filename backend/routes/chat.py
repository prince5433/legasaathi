import logging
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Request
from slowapi import Limiter
from slowapi.util import get_remote_address

from database import get_chats_col
from middleware.auth import verify_clerk
from models.chat import ChatRequest, ChatResponse
from services.rag_service import answer_query

log = logging.getLogger("legalsaathi.chat")
router = APIRouter()
limiter = Limiter(key_func=get_remote_address)


@router.post("/ask", response_model=ChatResponse)
@limiter.limit("20/minute")
async def ask_question(
    request: Request,
    body: ChatRequest,
    user_id: str = Depends(verify_clerk),
):
    question = body.question.strip()
    if not question:
        raise HTTPException(400, "Question cannot be empty")

    try:
        answer = await answer_query(
            question=question,
            user_id=user_id,
            doc_id=body.documentId,
            language=body.language,
        )
    except Exception as e:
        log.exception("answer_query failed")
        raise HTTPException(500, f"Chat backend failed: {type(e).__name__}: {e}")

    now = datetime.utcnow()
    await get_chats_col().update_one(
        {"userId": user_id, "documentId": body.documentId},
        {"$push": {"messages": {"$each": [
            {"role": "user", "content": question, "ts": now},
            {"role": "assistant", "content": answer, "ts": now},
        ]}}},
        upsert=True,
    )

    return ChatResponse(answer=answer, language=body.language)


@router.get("/history/{document_id}")
async def get_chat_history(
    document_id: str,
    user_id: str = Depends(verify_clerk),
):
    chat = await get_chats_col().find_one(
        {"userId": user_id, "documentId": document_id},
    )
    return {"messages": (chat or {}).get("messages", [])}
