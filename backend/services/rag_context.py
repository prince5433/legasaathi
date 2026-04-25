"""Shared context loading and prompt building for document chat."""

from __future__ import annotations

from bson import ObjectId

from database import get_documents_col


OUT_OF_CONTEXT = {
    "hindi": "Yeh sawaal is document ke context se bahar hai.",
    "english": "This question is out of context for the selected document.",
}


async def load_document_context(doc_id: str | None, user_id: str) -> tuple[dict | None, str]:
    """Load the selected document's raw text for grounded answers.

    Qdrant is still used for focused snippets, but the raw text fallback keeps
    typo-heavy or broad document questions from failing as "unclear".
    """
    if not doc_id:
        return None, ""

    try:
        oid = ObjectId(doc_id)
    except Exception:
        return None, ""

    doc = await get_documents_col().find_one(
        {"_id": oid, "userId": user_id},
        {"fileName": 1, "docType": 1, "summary": 1, "rawText": 1},
    )
    if not doc:
        return None, ""

    return doc, (doc.get("rawText") or "").strip()


def build_document_prompt(
    *,
    question: str,
    language: str,
    past: str,
    qdrant_ctx: str,
    neo4j_ctx: str,
    jurisdiction_ctx: str,
    state: str | None,
    doc: dict | None,
    raw_text: str,
) -> str:
    lang = (
        "Reply in simple Hindi/Hinglish. Use Roman Hindi when the user writes in Roman Hindi."
        if language == "hindi"
        else "Reply in clear English."
    )
    out_of_context = OUT_OF_CONTEXT.get(language, OUT_OF_CONTEXT["hindi"])

    doc_meta = "(none)"
    if doc:
        doc_meta = (
            f"File name: {doc.get('fileName', '(unknown)')}\n"
            f"Document type: {doc.get('docType', '(unknown)')}\n"
            f"Existing summary: {doc.get('summary', '') or '(none)'}"
        )

    prompt = (
        "You are LegalSaathi, a document-grounded legal assistant for Indian citizens.\n"
        f"{lang}\n\n"
        "Rules:\n"
        "- Answer questions about the selected document even if the user's spelling or grammar is imperfect.\n"
        "- Use only the selected document text, retrieved chunks, graph context, and state-law context when relevant.\n"
        "- If the question is about document parties, clauses, payments, obligations, rights, dates, risks, summary, "
        "termination, retention, or any information present in the document, answer directly from the document.\n"
        f"- If the question cannot be answered from the selected document, reply exactly: {out_of_context}\n"
        "- Do not ask for clarification just because the wording is short or contains typos; infer the closest document-related intent.\n"
        "- Do not invent facts that are not in the selected document.\n\n"
        f"=== User History ===\n{past or '(none)'}\n\n"
        f"=== Selected Document ===\n{doc_meta}\n\n"
        f"=== Retrieved Document Chunks ===\n{qdrant_ctx or '(none)'}\n\n"
        f"=== Full Document Text ===\n{raw_text[:12000] or '(none)'}\n\n"
        f"=== Graph Context ===\n{neo4j_ctx or '(none)'}\n\n"
    )

    if jurisdiction_ctx:
        state_label = f" ({state})" if state else ""
        prompt += f"=== State Law Context{state_label} ===\n{jurisdiction_ctx}\n\n"

    return prompt + f"=== Question ===\n{question}"
