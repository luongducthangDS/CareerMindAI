import streamlit as st
import io
from docx import Document
from utils.cover_letter_llm import generate_cover_letter


def _to_docx(text: str) -> bytes:
    doc = Document()
    for para in text.split("\n"):
        doc.add_paragraph(para)
    buf = io.BytesIO()
    doc.save(buf)
    return buf.getvalue()


def render():
    st.markdown("## 💼 Viết thư xin việc")
    st.markdown("Điền thông tin bên dưới — AI sẽ viết thư xin việc cá nhân hóa cho bạn trong vài giây.")
    st.markdown("<div style='margin-top:1rem'></div>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        vi_tri = st.text_input("Vị trí ứng tuyển *", placeholder="AI Engineer")
        cong_ty = st.text_input("Tên công ty *", placeholder="FPT Software, VNG, Grab...")
    with col2:
        nguoi_nhan = st.text_input("Người nhận (không bắt buộc)", placeholder="Anh/Chị Nguyễn Thị B")

    # CV source
    st.markdown("#### Thông tin CV")
    has_cv = bool(st.session_state.get("cv_text", "").strip())

    if has_cv:
        st.success("✅ Sử dụng CV đã tải lên ở trang Phân tích CV.")
        cv_text = st.session_state["cv_text"]
    else:
        st.info("Chưa có CV. Bạn có thể dán tóm tắt thông tin bản thân bên dưới.")
        cv_text = st.text_area(
            "Tóm tắt thông tin bản thân",
            height=150,
            placeholder="Ví dụ:\n- 2 năm kinh nghiệm Python, FastAPI\n- Tốt nghiệp HUST ngành CNTT 2024\n- Có kinh nghiệm deploy ML model lên production\n- GitHub: github.com/username",
            label_visibility="collapsed",
        )

    # JD (optional)
    st.markdown("#### Nội dung tin tuyển dụng (không bắt buộc)")
    jd_saved = st.session_state.get("jd_text_saved", "")
    if jd_saved:
        st.caption("✅ Sẵn có JD từ trang Phân tích tin tuyển dụng.")
    jd_text = st.text_area(
        "Dán JD để thư được cá nhân hóa hơn",
        value=jd_saved,
        height=120,
        placeholder="(Tùy chọn) Dán nội dung tin tuyển dụng vào đây...",
        label_visibility="collapsed",
    )

    st.markdown("<div style='margin-top:0.5rem'></div>", unsafe_allow_html=True)

    can_generate = bool(vi_tri.strip() and cong_ty.strip() and cv_text.strip())

    if st.button("✍️  Viết thư xin việc", use_container_width=True, disabled=not can_generate):
        with st.spinner("AI đang viết thư cho bạn..."):
            try:
                letter = generate_cover_letter(
                    vi_tri=vi_tri,
                    cong_ty=cong_ty,
                    nguoi_nhan=nguoi_nhan,
                    cv_text=cv_text,
                    jd_text=jd_text,
                )
                st.session_state.cover_letter = letter
                st.session_state.cover_letter_meta = {"vi_tri": vi_tri, "cong_ty": cong_ty}
            except Exception:
                st.error("Tạo thư thất bại. Vui lòng thử lại.")

    if not can_generate and not vi_tri.strip():
        st.caption("* Vui lòng điền Vị trí ứng tuyển, Tên công ty và thông tin CV.")

    # Result
    if "cover_letter" in st.session_state:
        st.markdown("---")
        meta = st.session_state.get("cover_letter_meta", {})
        st.markdown(f"### Thư xin việc — *{meta.get('vi_tri', '')}* tại *{meta.get('cong_ty', '')}*")

        edited = st.text_area(
            "Bạn có thể chỉnh sửa trực tiếp bên dưới",
            value=st.session_state.cover_letter,
            height=400,
            label_visibility="collapsed",
            key="letter_edit",
        )
        st.session_state.cover_letter = edited

        st.markdown("---")
        col_a, col_b, col_c = st.columns(3)
        with col_a:
            st.download_button(
                label="📥  Tải về Word (.docx)",
                data=_to_docx(edited),
                file_name=f"Thu_xin_viec_{cong_ty.replace(' ','_')}.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                use_container_width=True,
            )
        with col_b:
            st.download_button(
                label="📄  Tải về TXT",
                data=edited,
                file_name=f"Thu_xin_viec_{cong_ty.replace(' ','_')}.txt",
                mime="text/plain",
                use_container_width=True,
            )
        with col_c:
            if st.button("🔄  Viết lại", use_container_width=True):
                del st.session_state["cover_letter"]
                st.rerun()
