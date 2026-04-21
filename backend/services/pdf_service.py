"""Extract raw text from a PDF buffer. No disk writes."""

import io
import pdfplumber


def extract_text(file_bytes: bytes) -> str:
    text_parts: list[str] = []
    with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text() or ""
            if page_text:
                text_parts.append(page_text)
    return "\n\n".join(text_parts).strip()
