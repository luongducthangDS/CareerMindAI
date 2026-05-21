import pdfplumber
import docx
import io

MAX_FILE_SIZE_MB = 5
MAX_FILE_SIZE_BYTES = MAX_FILE_SIZE_MB * 1024 * 1024
MAX_CV_TEXT_CHARS = 15_000  # ~3750 tokens, đủ cho một CV đầy đủ

# Magic bytes để xác nhận định dạng file thật sự (không chỉ dựa vào đuôi file)
PDF_MAGIC = b"%PDF"
DOCX_MAGIC = b"PK\x03\x04"  # DOCX là ZIP archive


def _validate_file(file_bytes: bytes, declared_ext: str) -> None:
    """Kiểm tra kích thước và magic bytes của file."""
    if len(file_bytes) > MAX_FILE_SIZE_BYTES:
        raise ValueError(f"File quá lớn. Giới hạn {MAX_FILE_SIZE_MB}MB.")

    if declared_ext == "pdf":
        if not file_bytes.startswith(PDF_MAGIC):
            raise ValueError("File không phải PDF hợp lệ.")
    elif declared_ext == "docx":
        if not file_bytes.startswith(DOCX_MAGIC):
            raise ValueError("File không phải DOCX hợp lệ.")


def extract_text_from_pdf(file_bytes: bytes) -> str:
    text_parts = []
    with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
        if len(pdf.pages) > 10:
            raise ValueError("CV quá dài (hơn 10 trang). Vui lòng rút gọn.")
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
    """Trả về (extracted_text, file_type). Raise ValueError nếu file không hợp lệ."""
    file_bytes = uploaded_file.read()
    name = uploaded_file.name.lower()

    if name.endswith(".pdf"):
        ext = "pdf"
    elif name.endswith(".docx"):
        ext = "docx"
    else:
        raise ValueError(f"Định dạng không được hỗ trợ: {uploaded_file.name}")

    _validate_file(file_bytes, ext)

    if ext == "pdf":
        text = extract_text_from_pdf(file_bytes)
    else:
        text = extract_text_from_docx(file_bytes)

    if not text.strip():
        raise ValueError("Không đọc được nội dung từ file. CV có thể bị scan dạng ảnh.")

    # Truncate nếu quá dài, tránh vượt token limit LLM
    if len(text) > MAX_CV_TEXT_CHARS:
        text = text[:MAX_CV_TEXT_CHARS] + "\n\n[... Nội dung bị cắt bớt do quá dài]"

    return text, ext
