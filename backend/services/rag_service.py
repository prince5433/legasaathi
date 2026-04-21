"""Answer a user question using Mem0 + Qdrant + Neo4j + LLM."""

from __future__ import annotations

import logging

from services.llm_service import ainvoke_with_fallback
from services.qdrant_service import search_similar
from services.neo4j_service import get_related_context
from services.memory_service import get_memory, save_memory

log = logging.getLogger("legalsaathi.rag")


async def answer_query(
    question: str,
    user_id: str,
    doc_id: str | None = None,
    language: str = "hindi",
) -> str:
    past = get_memory(user_id, question)

    try:
        docs = await search_similar(question, doc_id=doc_id, k=4)
        qdrant_ctx = "\n\n".join(d.page_content for d in docs)
    except Exception:
        log.exception("Qdrant search failed; continuing without doc context")
        qdrant_ctx = ""

    neo4j_ctx = ""
    if doc_id:
        try:
            neo4j_ctx = await get_related_context(doc_id)
        except Exception:
            log.exception("Neo4j graph read failed; continuing")

    lang = (
        "Jawab simple Hindi (Devanagari ya Roman dono theek hai) mein do."
        if language == "hindi"
        else "Answer in clear English."
    )

    prompt = (
        "You are LegalSaathi, a legal assistant for Indian citizens. "
        f"{lang}\n"
        "If the context is insufficient, say so honestly.\n\n"
        f"=== User History ===\n{past or '(none)'}\n\n"
        f"=== Document Context ===\n{qdrant_ctx or '(none)'}\n\n"
        f"=== Graph Context ===\n{neo4j_ctx or '(none)'}\n\n"
        f"=== Question ===\n{question}"
    )

    resp = await ainvoke_with_fallback(prompt)
    answer = resp.content if hasattr(resp, "content") else str(resp)

    save_memory(
        user_id,
        [
            {"role": "user", "content": question},
            {"role": "assistant", "content": answer},
        ],
    )
    return answer
