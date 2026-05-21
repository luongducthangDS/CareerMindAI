import streamlit as st
import uuid
from utils.document_parser import parse_uploaded_file
from utils.cv_analyzer import analyze_cv
from utils.vector_store import save_cv
from utils.rate_limiter import guard, consume

ROLE_OPTIONS = [
    "Kỹ sư AI / Machine Learning",
    "Kỹ sư phần mềm",
    "Kỹ sư Backend",
    "Kỹ sư Full-Stack",
    "Kỹ sư Data / Data Scientist",
    "Thực tập sinh IT",
    "✏️  Nhập vị trí khác...",
]

ROLE_MAP = {
    "Kỹ sư AI / Machine Learning": "AI Engineer / Machine Learning Engineer",
    "Kỹ sư phần mềm": "Software Engineer",
    "Kỹ sư Backend": "Backend Engineer",
    "Kỹ sư Full-Stack": "Full-Stack Engineer",
    "Kỹ sư Data / Data Scientist": "Data Engineer / Data Scientist",
    "Thực tập sinh IT": "IT Intern / Junior Developer",
}


def render():
    st.markdown("## 📄 Phân tích CV")
    st.markdown(
        "Tải CV lên để nhận nhận xét chi tiết: điểm mạnh, điểm yếu và gợi ý cải thiện ngay lập tức."
    )
    st.markdown("<div style='margin-top:1.5rem'></div>", unsafe_allow_html=True)

    # ── Step 1: Upload ──────────────────────────────────────────────────────────
    st.markdown("#### Bước 1 — Tải CV của bạn lên")
    uploaded_file = st.file_uploader(
        "Chấp nhận định dạng PDF và Word (.docx)",
        type=["pdf", "docx"],
        label_visibility="visible",
    )

    if uploaded_file is not None:
        # Parse silently — no raw text shown to user
        if "cv_text" not in st.session_state or st.session_state.get("last_file") != uploaded_file.name:
            with st.spinner("Đang đọc CV của bạn..."):
                try:
                    cv_text, _ = parse_uploaded_file(uploaded_file)
                    st.session_state.cv_text = cv_text
                    st.session_state.last_file = uploaded_file.name
                    if "cv_analysis" in st.session_state:
                        del st.session_state["cv_analysis"]
                except Exception:
                    st.error("Không đọc được file. Vui lòng kiểm tra lại định dạng PDF hoặc Word và thử lại.")
                    return

        st.success(f"✅ Đã tải lên: **{uploaded_file.name}**")
        st.markdown("<div style='margin-top:1.5rem'></div>", unsafe_allow_html=True)

        # ── Step 2: Choose role ─────────────────────────────────────────────────
        st.markdown("#### Bước 2 — Bạn đang ứng tuyển vị trí nào?")
        selected = st.selectbox(
            "Chọn vị trí ứng tuyển",
            ROLE_OPTIONS,
            label_visibility="collapsed",
        )

        if selected == "✏️  Nhập vị trí khác...":
            custom_role = st.text_input(
                "Nhập vị trí của bạn",
                placeholder="Ví dụ: Junior React Developer, DevOps Engineer, Product Manager...",
                label_visibility="collapsed",
            )
            target_role_vn = custom_role.strip() if custom_role.strip() else "Vị trí khác"
            target_role_en = target_role_vn  # Gửi thẳng cho LLM, đủ rõ
        else:
            target_role_vn = selected
            target_role_en = ROLE_MAP[selected]

        st.markdown("<div style='margin-top:1.5rem'></div>", unsafe_allow_html=True)

        # ── Step 3: Analyze ─────────────────────────────────────────────────────
        st.markdown("#### Bước 3 — Nhận phân tích từ AI")

        if st.button("🔍  Phân tích CV ngay", use_container_width=True):
            if not guard("cv_analyze"):
                return
            with st.spinner("AI đang phân tích CV của bạn... Thường mất 15–30 giây."):
                try:
                    analysis = analyze_cv(
                        cv_text=st.session_state.cv_text,
                        target_role=target_role_en,
                        provider="groq",
                    )
                    st.session_state.cv_analysis = analysis
                    st.session_state.analysis_role = target_role_vn

                    consume("cv_analyze")
                    save_cv(
                        session_id=str(uuid.uuid4()),
                        cv_text=st.session_state.cv_text,
                        analysis=analysis,
                        metadata={"role": target_role_en, "file": uploaded_file.name},
                    )
                except Exception:
                    st.error("Phân tích thất bại. Vui lòng thử lại sau ít phút.")
                    return

    # ── Results ─────────────────────────────────────────────────────────────────
    if "cv_analysis" in st.session_state:
        st.markdown("---")
        st.markdown(
            f"### Kết quả phân tích — *{st.session_state.get('analysis_role', '')}*"
        )
        st.markdown(st.session_state.cv_analysis)

        st.markdown("---")
        col_a, col_b = st.columns(2)
        with col_a:
            st.download_button(
                label="📥  Tải kết quả về máy",
                data=st.session_state.cv_analysis,
                file_name="phan_tich_cv.txt",
                mime="text/plain",
                use_container_width=True,
            )
        with col_b:
            if st.button("🔄  Phân tích lại", use_container_width=True):
                del st.session_state["cv_analysis"]
                st.rerun()

    elif uploaded_file is None:
        # Empty state
        st.markdown("""
        <div style="
            text-align: center;
            padding: 4rem 2rem;
            color: #d1d5db;
            border: 2px dashed #e5e7eb;
            border-radius: 16px;
            margin-top: 1rem;
        ">
            <div style="font-size:3rem; margin-bottom:0.75rem">📂</div>
            <p style="font-size:1rem; color:#9ca3af; margin:0">
                Tải CV lên để bắt đầu — hỗ trợ PDF và Word
            </p>
        </div>
        """, unsafe_allow_html=True)
