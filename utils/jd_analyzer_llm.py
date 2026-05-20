from utils.llm_client import chat

ANALYZE_SYSTEM = """Bạn là chuyên gia tuyển dụng IT. Phân tích tin tuyển dụng và đánh giá mức độ phù hợp với CV ứng viên.
Luôn trả lời bằng tiếng Việt, cụ thể và thực tế."""

ANALYZE_PROMPT = """Phân tích tin tuyển dụng sau và so sánh với CV của ứng viên.

TIN TUYỂN DỤNG:
{jd_text}

CV ỨNG VIÊN:
{cv_text}

Trả lời theo cấu trúc markdown sau:

## 🎯 Mức độ phù hợp: [X%]
Giải thích ngắn gọn lý do điểm số này.

## ✅ Điểm mạnh phù hợp
Liệt kê 3–5 điểm ứng viên đáp ứng tốt yêu cầu JD.

## ⚠️ Kỹ năng còn thiếu
Liệt kê kỹ năng/kinh nghiệm JD yêu cầu nhưng CV chưa thể hiện rõ.

## 📝 Gợi ý tùy chỉnh CV
3–5 gợi ý cụ thể để CV phù hợp hơn với JD này (thêm từ khóa, viết lại bullet nào, v.v.)

## 🔑 Từ khóa quan trọng trong JD
Liệt kê các từ khóa/kỹ năng nên có trong CV để qua ATS."""

ANALYZE_NO_CV_PROMPT = """Phân tích tin tuyển dụng sau:

TIN TUYỂN DỤNG:
{jd_text}

Trả lời theo cấu trúc markdown sau:

## 📋 Tóm tắt vị trí
Tên vị trí, công ty (nếu có), mức kinh nghiệm yêu cầu.

## 🛠️ Kỹ năng bắt buộc
Liệt kê các kỹ năng/công nghệ bắt buộc phải có.

## ⭐ Kỹ năng ưu tiên (nice-to-have)
Liệt kê kỹ năng được ưu tiên nhưng không bắt buộc.

## 📌 Trách nhiệm chính
3–5 nhiệm vụ chính của vị trí này.

## 💡 Lời khuyên ứng tuyển
2–3 gợi ý để nổi bật khi ứng tuyển vị trí này."""


def analyze_jd(jd_text: str, cv_text: str = "") -> str:
    if cv_text.strip():
        prompt = ANALYZE_PROMPT.format(jd_text=jd_text, cv_text=cv_text)
    else:
        prompt = ANALYZE_NO_CV_PROMPT.format(jd_text=jd_text)
    return chat(prompt=prompt, system=ANALYZE_SYSTEM, provider="groq")
