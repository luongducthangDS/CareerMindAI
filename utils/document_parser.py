import pdfplumber
import docx
import io


def extract_text_from_pdf(file_bytes: bytes) -> str:
    text_parts = []
    with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                text_parts.append(text)
    return "\n".join(text_parts)


def extract_text_from_docx(file_bytes: bytes) -> str:
    doc = docx.Document(io.BytesIO(file_bytes))
    paragraphs = [p.text for p in doc.paragraphs if p.text.strip()]
    return "\n".join(paragraphs)


def parse_uploaded_file(uploaded_file) -> tuple[str, str]:
    """Returns (extracted_text, file_type)."""
    file_bytes = uploaded_file.read()
    name = uploaded_file.name.lower()

    if name.endswith(".pdf"):
        return extract_text_from_pdf(file_bytes), "pdf"
    elif name.endswith(".docx"):
        return extract_text_from_docx(file_bytes), "docx"
    else:
        raise ValueError(f"Unsupported file type: {uploaded_file.name}")
