import streamlit as st
from utils.cv_generator_llm import enhance_cv
from utils.docx_exporter import export_cv_docx


def _init_state():
    if "cv_gen" not in st.session_state:
        st.session_state.cv_gen = {
            "ho_ten": "", "chuc_danh": "", "email": "", "phone": "",
            "linkedin": "", "github": "", "dia_chi": "",
            "tom_tat": "",
            "kinh_nghiem": [{"cong_ty": "", "vi_tri": "", "thoi_gian": "", "mo_ta": ""}],
            "hoc_van": [{"truong": "", "nganh": "", "thoi_gian": "", "gpa": ""}],
            "ky_nang": "",
            "du_an": [{"ten": "", "cong_nghe": "", "mo_ta": "", "link": ""}],
            "chung_chi": "",
        }


def render():
    _init_state()
    d = st.session_state.cv_gen

    st.markdown("## ✍️ Tạo CV mới")
    st.markdown("Điền thông tin bên dưới — AI sẽ giúp cải thiện ngôn từ và tạo file Word chuyên nghiệp.")
    st.markdown("<div style='margin-top:1rem'></div>", unsafe_allow_html=True)

    tab1, tab2, tab3, tab4 = st.tabs(["👤 Cá nhân", "💼 Kinh nghiệm", "🎓 Học vấn", "🛠️ Kỹ năng & Dự án"])

    # ── Tab 1: Thông tin cá nhân ─────────────────────────────────────────────
    with tab1:
        st.markdown("#### Thông tin cơ bản")
        c1, c2 = st.columns(2)
        with c1:
            d["ho_ten"] = st.text_input("Họ và tên *", value=d["ho_ten"], placeholder="Nguyễn Văn A")
            d["email"] = st.text_input("Email *", value=d["email"], placeholder="email@gmail.com")
            d["phone"] = st.text_input("Số điện thoại", value=d["phone"], placeholder="0901 234 567")
            d["dia_chi"] = st.text_input("Địa chỉ", value=d["dia_chi"], placeholder="Hà Nội, Việt Nam")
        with c2:
            d["chuc_danh"] = st.text_input("Vị trí ứng tuyển *", value=d["chuc_danh"], placeholder="AI Engineer")
            d["linkedin"] = st.text_input("LinkedIn", value=d["linkedin"], placeholder="linkedin.com/in/username")
            d["github"] = st.text_input("GitHub", value=d["github"], placeholder="github.com/username")

        st.markdown("#### Tóm tắt bản thân")
        d["tom_tat"] = st.text_area(
            "Viết 2–4 câu giới thiệu bản thân. AI sẽ giúp cải thiện.",
            value=d["tom_tat"],
            height=120,
            placeholder="Ví dụ: Sinh viên năm 4 ngành CNTT, có 1 năm kinh nghiệm thực tập tại...",
            label_visibility="collapsed",
        )

    # ── Tab 2: Kinh nghiệm ──────────────────────────────────────────────────
    with tab2:
        st.markdown("#### Kinh nghiệm làm việc")
        st.caption("Thêm từng vị trí đã làm — từ gần nhất đến cũ nhất.")

        for i, exp in enumerate(d["kinh_nghiem"]):
            with st.container():
                st.markdown(f"**Vị trí {i + 1}**")
                c1, c2 = st.columns(2)
                with c1:
                    exp["cong_ty"] = st.text_input("Tên công ty", value=exp["cong_ty"],
                                                    key=f"exp_cty_{i}", placeholder="Google, FPT, Startup XYZ...")
                    exp["vi_tri"] = st.text_input("Chức danh", value=exp["vi_tri"],
                                                   key=f"exp_vt_{i}", placeholder="Software Engineer Intern")
                with c2:
                    exp["thoi_gian"] = st.text_input("Thời gian", value=exp["thoi_gian"],
                                                      key=f"exp_tg_{i}", placeholder="06/2024 – 12/2024")
                exp["mo_ta"] = st.text_area(
                    "Mô tả công việc (mỗi dòng một ý)",
                    value=exp["mo_ta"], key=f"exp_mt_{i}", height=120,
                    placeholder="- Xây dựng API REST bằng FastAPI phục vụ 10,000 requests/ngày\n- Tối ưu query database giảm 40% thời gian phản hồi",
                    label_visibility="collapsed",
                )
                if len(d["kinh_nghiem"]) > 1:
                    if st.button("🗑️ Xóa vị trí này", key=f"del_exp_{i}"):
                        d["kinh_nghiem"].pop(i)
                        st.rerun()
                st.markdown("---")

        if st.button("➕ Thêm vị trí làm việc"):
            d["kinh_nghiem"].append({"cong_ty": "", "vi_tri": "", "thoi_gian": "", "mo_ta": ""})
            st.rerun()

    # ── Tab 3: Học vấn ──────────────────────────────────────────────────────
    with tab3:
        st.markdown("#### Học vấn")

        for i, edu in enumerate(d["hoc_van"]):
            with st.container():
                st.markdown(f"**Trường {i + 1}**")
                c1, c2 = st.columns(2)
                with c1:
                    edu["truong"] = st.text_input("Tên trường", value=edu["truong"],
                                                   key=f"edu_tr_{i}", placeholder="Đại học Bách Khoa Hà Nội")
                    edu["nganh"] = st.text_input("Ngành học", value=edu["nganh"],
                                                  key=f"edu_ng_{i}", placeholder="Khoa học Máy tính")
                with c2:
                    edu["thoi_gian"] = st.text_input("Thời gian", value=edu["thoi_gian"],
                                                      key=f"edu_tg_{i}", placeholder="2021 – 2025")
                    edu["gpa"] = st.text_input("GPA (nếu có)", value=edu["gpa"],
                                               key=f"edu_gpa_{i}", placeholder="3.5 / 4.0")
                if len(d["hoc_van"]) > 1:
                    if st.button("🗑️ Xóa trường này", key=f"del_edu_{i}"):
                        d["hoc_van"].pop(i)
                        st.rerun()
                st.markdown("---")

        if st.button("➕ Thêm trường học"):
            d["hoc_van"].append({"truong": "", "nganh": "", "thoi_gian": "", "gpa": ""})
            st.rerun()

    # ── Tab 4: Kỹ năng & Dự án ──────────────────────────────────────────────
    with tab4:
        st.markdown("#### Kỹ năng")
        d["ky_nang"] = st.text_area(
            "Liệt kê kỹ năng",
            value=d["ky_nang"], height=100,
            placeholder="Python, FastAPI, React, Docker, Git, SQL, Machine Learning, LLM, ...",
            label_visibility="collapsed",
        )

        st.markdown("#### Dự án cá nhân")
        for i, proj in enumerate(d["du_an"]):
            with st.container():
                st.markdown(f"**Dự án {i + 1}**")
                c1, c2 = st.columns(2)
                with c1:
                    proj["ten"] = st.text_input("Tên dự án", value=proj["ten"],
                                                 key=f"proj_ten_{i}", placeholder="CareerMind AI")
                    proj["cong_nghe"] = st.text_input("Công nghệ sử dụng", value=proj["cong_nghe"],
                                                       key=f"proj_cn_{i}", placeholder="Python, Streamlit, Groq API")
                with c2:
                    proj["link"] = st.text_input("Link (GitHub/Demo)", value=proj["link"],
                                                  key=f"proj_link_{i}", placeholder="github.com/username/project")
                proj["mo_ta"] = st.text_area(
                    "Mô tả dự án",
                    value=proj["mo_ta"], key=f"proj_mt_{i}", height=100,
                    placeholder="- Xây dựng ứng dụng phân tích CV bằng AI\n- Tích hợp Groq LLaMA 3 để phân tích và gợi ý cải thiện",
                    label_visibility="collapsed",
                )
                if len(d["du_an"]) > 1:
                    if st.button("🗑️ Xóa dự án này", key=f"del_proj_{i}"):
                        d["du_an"].pop(i)
                        st.rerun()
                st.markdown("---")

        if st.button("➕ Thêm dự án"):
            d["du_an"].append({"ten": "", "cong_nghe": "", "mo_ta": "", "link": ""})
            st.rerun()

        st.markdown("#### Chứng chỉ & Giải thưởng")
        d["chung_chi"] = st.text_area(
            "Chứng chỉ",
            value=d["chung_chi"], height=80,
            placeholder="AWS Certified Cloud Practitioner (2024)\nTOEIC 850 (2023)",
            label_visibility="collapsed",
        )

    # ── Export section ───────────────────────────────────────────────────────
    st.markdown("---")
    st.markdown("### Tạo CV")

    col_ai, col_dl = st.columns(2)

    with col_ai:
        if st.button("✨  AI cải thiện nội dung", use_container_width=True, help="AI sẽ viết lại summary và bullet points chuyên nghiệp hơn"):
            if not d["ho_ten"] or not d["chuc_danh"]:
                st.warning("Vui lòng điền ít nhất Họ tên và Vị trí ứng tuyển.")
            else:
                with st.spinner("AI đang cải thiện ngôn từ CV..."):
                    try:
                        enhanced = enhance_cv(d, d["chuc_danh"])
                        st.session_state.cv_gen.update(enhanced)
                        st.success("✅ Đã cải thiện! Kiểm tra lại các tab rồi tải về.")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Lỗi: {e}")

    with col_dl:
        if not d["ho_ten"]:
            st.button("📥  Tải về Word (.docx)", disabled=True, use_container_width=True,
                      help="Điền họ tên trước")
        else:
            docx_bytes = export_cv_docx(d)
            filename = f"CV_{d['ho_ten'].replace(' ', '_')}.docx"
            st.download_button(
                label="📥  Tải về Word (.docx)",
                data=docx_bytes,
                file_name=filename,
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                use_container_width=True,
            )
