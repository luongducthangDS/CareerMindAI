import json
from utils.llm_client import chat

SYSTEM = """Bạn là chuyên gia viết CV cho ngành IT tại Việt Nam.
Nhiệm vụ: cải thiện ngôn từ CV để nghe chuyên nghiệp, mạnh mẽ và thu hút nhà tuyển dụng.
Quy tắc bắt buộc:
- KHÔNG thay đổi thông tin thực tế (tên, công ty, trường, thời gian, số liệu)
- Bullet points theo cấu trúc: Động từ mạnh + Hành động cụ thể + Kết quả/Tác động
- Summary: 3-4 câu, highlight điểm mạnh nhất, phù hợp vị trí target
- Trả về JSON thuần túy, không bọc trong markdown code block"""

PROMPT = """Cải thiện nội dung CV sau cho vị trí: {target_role}

Dữ liệu CV (JSON):
{cv_json}

Chỉ cải thiện: tom_tat, kinh_nghiem[].mo_ta, du_an[].mo_ta
Giữ nguyên tất cả trường còn lại.
Trả về JSON đầy đủ đã được cải thiện."""


def enhance_cv(cv_data: dict, target_role: str) -> dict:
    raw = chat(
        prompt=PROMPT.format(target_role=target_role, cv_json=json.dumps(cv_data, ensure_ascii=False, indent=2)),
        system=SYSTEM,
        provider="groq",
    )
    raw = raw.strip().lstrip("```json").lstrip("```").rstrip("```").strip()
    try:
        return json.loads(raw)
    except Exception:
        return cv_data
