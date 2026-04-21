"""5-point Hindi summary of a legal document."""

from services.llm_service import ainvoke_with_fallback


async def summarize_document(raw_text: str) -> str:
    prompt = (
        "Yeh Indian legal document ka simple Hindi summary do — exactly 5 bullet "
        "points, har point 1-2 line. Aam aadmi samajh sake aisi bhasha. "
        "Tough legal jargon avoid karo.\n\n"
        f"Document:\n{raw_text[:4000]}"
    )
    resp = await ainvoke_with_fallback(prompt)
    return resp.content.strip() if hasattr(resp, "content") else str(resp)
