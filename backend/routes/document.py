"""Document upload + retrieval routes.

The upload flow fixes the v5 `doc_id='temp'` bug by inserting into MongoDB
BEFORE running the LangGraph pipeline, so the pipeline receives the real
ObjectId string and every Qdrant chunk / Neo4j node is tagged correctly.
"""

import asyncio
import logging
from datetime import datetime

from bson import ObjectId
from fastapi import APIRouter, Depends, File, HTTPException, Request, UploadFile
from slowapi import Limiter
from slowapi.util import get_remote_address

log = logging.getLogger("legalsaathi.document")

from database import get_documents_col
from middleware.auth import verify_clerk
from services.pdf_service import extract_text
from services.s3_service import upload_pdf
from services.summarizer_service import summarize_document
from services.risk_service import detect_risks
from services.classifier_service import classify_document
from services.langgraph_pipeline import pipeline

router = APIRouter()
limiter = Limiter(key_func=get_remote_address)


def _serialise(doc: dict) -> dict:
    doc["_id"] = str(doc["_id"])
    # rawText is big — trim on the way out
    doc.pop("rawText", None)
    return doc


@router.post("/upload")
@limiter.limit("10/hour")
async def upload_document(
    request: Request,
    pdf: UploadFile = File(...),
    user_id: str = Depends(verify_clerk),
):
    if pdf.content_type not in {"application/pdf", "application/x-pdf"}:
        raise HTTPException(400, "Only PDF files are accepted")

    contents = await pdf.read()
    if not contents:
        raise HTTPException(400, "Empty file")

    file_url = await upload_pdf(contents, pdf.filename, user_id)
    raw_text = extract_text(contents)
    if not raw_text:
        raise HTTPException(422, "Could not extract text from this PDF")

    # Insert first to get a real ObjectId — avoids the v5 doc_id='temp' bug
    col = get_documents_col()
    insert_result = await col.insert_one({
        "userId": user_id,
        "fileName": pdf.filename,
        "fileUrl": file_url,
        "rawText": raw_text,
        "status": "processing",
        "createdAt": datetime.utcnow(),
    })
    doc_id = str(insert_result.inserted_id)

    # LangGraph ingestion (chunk+embed to Qdrant, entities to Neo4j)
    try:
        await pipeline.ainvoke({
            "file_bytes": contents,
            "doc_id": doc_id,
            "raw_text": raw_text,
        })
    except Exception:
        log.exception("LangGraph pipeline failed for doc %s", doc_id)

    # Parallel analysis — each wrapped so one failure doesn't nuke the others
    async def _safe(coro, default, label):
        try:
            return await coro
        except Exception:
            log.exception("analysis step '%s' failed for doc %s", label, doc_id)
            return default

    summary, risks, doc_type = await asyncio.gather(
        _safe(summarize_document(raw_text), "", "summary"),
        _safe(detect_risks(raw_text), [], "risks"),
        _safe(classify_document(raw_text), "other", "classify"),
    )

    await col.update_one(
        {"_id": insert_result.inserted_id},
        {"$set": {
            "summary": summary,
            "risks": risks,
            "docType": doc_type,
            "status": "done",
        }},
    )

    return {
        "docId": doc_id,
        "fileName": pdf.filename,
        "fileUrl": file_url,
        "summary": summary,
        "risks": risks,
        "docType": doc_type,
        "status": "done",
    }


@router.get("/list")
async def list_documents(user_id: str = Depends(verify_clerk)):
    cursor = get_documents_col().find(
        {"userId": user_id},
        {"rawText": 0},
    ).sort("createdAt", -1).limit(50)
    return [_serialise(d) async for d in cursor]


@router.get("/{doc_id}")
async def get_document(doc_id: str, user_id: str = Depends(verify_clerk)):
    try:
        oid = ObjectId(doc_id)
    except Exception:
        raise HTTPException(400, "Invalid document id")

    doc = await get_documents_col().find_one(
        {"_id": oid, "userId": user_id},
        {"rawText": 0},
    )
    if not doc:
        raise HTTPException(404, "Document not found")
    return _serialise(doc)
