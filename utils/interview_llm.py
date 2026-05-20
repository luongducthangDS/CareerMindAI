from utils.llm_client import chat

GEN_SYSTEM = """Bạn là interviewer kỳ cựu tại các công ty công nghệ lớn.
Tạo câu hỏi phỏng vấn thực tế, sát với vị trí và level của ứng viên.
Trả lời bằng tiếng Việt."""

GEN_PROMPT = """Tạo {so_cau} câu hỏi phỏng vấn cho vị trí: {vi_tri} — Level: {level}
Loại phỏng vấn: {loai}

Định dạng — mỗi câu hỏi trên một dòng, bắt đầu bằng số thứ tự:
1. [Câu hỏi]
2. [Câu hỏi]
...

Chỉ trả về danh sách câu hỏi, không giải thích thêm."""

EVAL_SYSTEM = """Bạn là interviewer đang chấm điểm câu trả lời phỏng vấn.
Cho phản hồi cụ thể, xây dựng và thực tế. Trả lời bằng tiếng Việt."""

EVAL_PROMPT = """Đánh giá câu trả lời phỏng vấn sau:

VỊ TRÍ: {vi_tri}
CÂU HỎI: {cau_hoi}
CÂU TRẢ LỜI CỦA ỨNG VIÊN: {tra_loi}

Trả lời theo format:
**Điểm: [X/10]**

**Điểm tốt:** [1–2 điểm tích cực cụ thể]

**Cần cải thiện:** [1–2 điểm cần làm tốt hơn]

**Gợi ý câu trả lời tốt hơn:** [1–2 câu gợi ý ngắn gọn]"""


def generate_questions(vi_tri: str, level: str, loai: str, so_cau: int = 5) -> list[str]:
    raw = chat(
        prompt=GEN_PROMPT.format(vi_tri=vi_tri, level=level, loai=loai, so_cau=so_cau),
        system=GEN_SYSTEM,
        provider="groq",
    )
    questions = []
    for line in raw.strip().split("\n"):
        line = line.strip()
        if line and line[0].isdigit() and "." in line:
            q = line.split(".", 1)[1].strip()
            if q:
                questions.append(q)
    return questions if questions else [raw]


def evaluate_answer(vi_tri: str, cau_hoi: str, tra_loi: str) -> str:
    return chat(
        prompt=EVAL_PROMPT.format(vi_tri=vi_tri, cau_hoi=cau_hoi, tra_loi=tra_loi),
        system=EVAL_SYSTEM,
        provider="groq",
    )
