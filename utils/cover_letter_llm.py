from utils.llm_client import chat

SYSTEM = """Bạn là chuyên gia viết thư xin việc (cover letter) cho ngành IT tại Việt Nam.
Viết thư chuyên nghiệp, cá nhân hóa, thể hiện đúng con người ứng viên — không sáo rỗng, không copy-paste mẫu."""

PROMPT = """Viết thư xin việc dựa trên thông tin sau:

VỊ TRÍ ỨNG TUYỂN: {vi_tri}
TÊN CÔNG TY: {cong_ty}
NGƯỜI NHẬN: {nguoi_nhan}

THÔNG TIN CV ỨNG VIÊN:
{cv_text}

NỘI DUNG TIN TUYỂN DỤNG (nếu có):
{jd_text}

Yêu cầu:
- Độ dài: 3–4 đoạn, khoảng 250–350 từ
- Đoạn 1: Giới thiệu bản thân + lý do ứng tuyển vị trí này tại công ty này
- Đoạn 2–3: Highlight 2–3 thành tích/kỹ năng cụ thể phù hợp với JD
- Đoạn 4: Lời kết, mong muốn phỏng vấn, cảm ơn
- Ngôn ngữ: tự nhiên, tự tin, không sáo rỗng
- Viết bằng tiếng Việt (hoặc tiếng Anh nếu JD bằng tiếng Anh)
- Bắt đầu bằng "Kính gửi [Người nhận]," hoặc "Dear [Recruiter],"
- Kết thúc bằng chữ ký phù hợp"""


def generate_cover_letter(vi_tri: str, cong_ty: str, nguoi_nhan: str, cv_text: str, jd_text: str = "") -> str:
    prompt = PROMPT.format(
        vi_tri=vi_tri,
        cong_ty=cong_ty,
        nguoi_nhan=nguoi_nhan if nguoi_nhan else "Phòng Nhân sự",
        cv_text=cv_text if cv_text else "(Chưa có thông tin CV)",
        jd_text=jd_text if jd_text else "(Không có)",
    )
    return chat(prompt=prompt, system=SYSTEM, provider="groq")
