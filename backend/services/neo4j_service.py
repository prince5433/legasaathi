"""Neo4j knowledge-graph writes + simple reads."""

from __future__ import annotations

import json
import re
from neo4j import AsyncGraphDatabase

from config import settings
from services.llm_service import ainvoke_with_fallback

_driver = None


def get_driver():
    global _driver
    if _driver is None:
        _driver = AsyncGraphDatabase.driver(
            settings.NEO4J_URI,
            auth=(settings.NEO4J_USER, settings.NEO4J_PASSWORD),
        )
    return _driver


async def close_driver() -> None:
    global _driver
    if _driver is not None:
        await _driver.close()
        _driver = None


def _strip_code_fence(text: str) -> str:
    text = text.strip()
    text = re.sub(r"^```(?:json)?", "", text).strip()
    text = re.sub(r"```$", "", text).strip()
    return text


async def extract_entities_llm(raw_text: str) -> dict:
    """Ask the LLM for persons / sections / dates / doc_type as JSON."""
    prompt = (
        "Extract entities from this Indian legal document. "
        "Respond with JSON only, no prose.\n"
        'Format: {"persons":[],"sections":[],"dates":[],"doc_type":""}\n'
        f"Document:\n{raw_text[:2500]}"
    )
    resp = await ainvoke_with_fallback(prompt)
    content = resp.content if hasattr(resp, "content") else str(resp)
    try:
        return json.loads(_strip_code_fence(content))
    except json.JSONDecodeError:
        return {"persons": [], "sections": [], "dates": [], "doc_type": ""}


async def store_entities(entities: dict, doc_id: str) -> None:
    driver = get_driver()
    doc_type = entities.get("doc_type", "") or ""
    async with driver.session() as session:
        await session.run(
            "MERGE (d:Document {id: $doc_id}) SET d.type = $doc_type",
            doc_id=doc_id,
            doc_type=doc_type,
        )
        for person in entities.get("persons") or []:
            await session.run(
                "MERGE (p:Person {name: $name}) "
                "WITH p MATCH (d:Document {id: $doc_id}) "
                "MERGE (d)-[:MENTIONS]->(p)",
                name=person,
                doc_id=doc_id,
            )
        for section in entities.get("sections") or []:
            await session.run(
                "MERGE (s:Section {name: $section}) "
                "WITH s MATCH (d:Document {id: $doc_id}) "
                "MERGE (d)-[:CITES]->(s)",
                section=section,
                doc_id=doc_id,
            )


async def get_related_context(doc_id: str, limit: int = 10) -> str:
    """Return a short text blob describing graph neighbours of this doc."""
    driver = get_driver()
    async with driver.session() as session:
        result = await session.run(
            "MATCH (d:Document {id: $doc_id})-[r]->(n) "
            "RETURN type(r) AS rel, labels(n)[0] AS label, "
            "       coalesce(n.name, n.id) AS name LIMIT $limit",
            doc_id=doc_id,
            limit=limit,
        )
        rows = [rec.data() async for rec in result]
    if not rows:
        return ""
    parts = [f"{r['label']} '{r['name']}' ({r['rel']})" for r in rows]
    return "Related entities: " + "; ".join(parts)
