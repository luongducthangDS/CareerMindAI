import streamlit as st
from utils.jd_analyzer_llm import analyze_jd


def render():
    st.markdown("## 🎯 Phân tích tin tuyển dụng")
    st.markdown("Dán nội dung JD vào bên dưới — AI sẽ phân tích yêu cầu và so sánh với CV của bạn.")
    st.markdown("<div style='margin-top:1rem'></div>", unsafe_allow_html=True)

    # JD input
    st.markdown("#### Nội dung tin tuyển dụng")
    jd_text = st.text_area(
        "Dán nội dung JD",
        height=280,
        placeholder="Dán toàn bộ nội dung tin tuyển dụng vào đây...\n\nVí dụ: Yêu cầu 2 năm kinh nghiệm Python, biết FastAPI, Docker, có kiến thức về Machine Learning...",
        label_visibility="collapsed",
        key="jd_input",
    )

    # CV status
    has_cv = bool(st.session_state.get("cv_text", "").strip())

    if has_cv:
        st.success("✅ Đã có CV từ trang Phân tích CV — AI sẽ so sánh trực tiếp với CV của bạn.")
    else:
        st.info("💡 Chưa có CV. Bạn có thể tải CV lên ở trang **Phân tích CV** để nhận đánh giá chi tiết hơn. Hoặc tiếp tục để chỉ phân tích JD.")

    st.markdown("<div style='margin-top:0.5rem'></div>", unsafe_allow_html=True)

    if st.button("🔍  Phân tích ngay", use_container_width=True, disabled=not jd_text.strip()):
        if not jd_text.strip():
            st.warning("Vui lòng dán nội dung tin tuyển dụng trước.")
        else:
            with st.spinner("AI đang phân tích tin tuyển dụng..."):
                try:
                    cv_text = st.session_state.get("cv_text", "")
                    result = analyze_jd(jd_text=jd_text, cv_text=cv_text)
                    st.session_state.jd_result = result
                    st.session_state.jd_text_saved = jd_text
                except Exception:
                    st.error("Phân tích thất bại. Vui lòng thử lại.")

    if "jd_result" in st.session_state:
        st.markdown("---")
        st.markdown(st.session_state.jd_result)
        st.markdown("---")

        col_a, col_b = st.columns(2)
        with col_a:
            st.download_button(
                label="📥  Tải kết quả về máy",
                data=st.session_state.jd_result,
                file_name="phan_tich_jd.txt",
                mime="text/plain",
                use_container_width=True,
            )
        with col_b:
            if st.button("🔄  Phân tích lại", use_container_width=True):
                del st.session_state["jd_result"]
                st.rerun()
