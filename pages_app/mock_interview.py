import streamlit as st
from utils.interview_llm import generate_questions, evaluate_answer

LEVELS = ["Junior (0–2 năm)", "Mid-level (2–4 năm)", "Senior (4+ năm)"]
TYPES = ["Kỹ thuật (Technical)", "Hành vi (Behavioral)", "Kết hợp (Mixed)"]
ROLES = [
    "AI / Machine Learning Engineer",
    "Software Engineer",
    "Backend Engineer",
    "Full-Stack Engineer",
    "Data Scientist / Data Engineer",
    "DevOps Engineer",
    "✏️  Vị trí khác...",
]


def render():
    st.markdown("## 🎤 Phỏng vấn thử")
    st.markdown("Luyện tập trả lời câu hỏi phỏng vấn với AI — nhận phản hồi ngay lập tức.")
    st.markdown("<div style='margin-top:1rem'></div>", unsafe_allow_html=True)

    # ── Setup ────────────────────────────────────────────────────────────────
    if "interview_questions" not in st.session_state:
        st.markdown("#### Cài đặt buổi phỏng vấn")
        c1, c2, c3 = st.columns(3)
        with c1:
            role_sel = st.selectbox("Vị trí", ROLES, label_visibility="visible")
            if role_sel == "✏️  Vị trí khác...":
                role = st.text_input("Nhập vị trí", placeholder="iOS Developer, Product Manager...", label_visibility="collapsed")
            else:
                role = role_sel
        with c2:
            level = st.selectbox("Level", LEVELS)
        with c3:
            interview_type = st.selectbox("Loại phỏng vấn", TYPES)

        so_cau = st.slider("Số câu hỏi", min_value=3, max_value=10, value=5)

        if st.button("🚀  Bắt đầu phỏng vấn", use_container_width=True, disabled=not role.strip()):
            with st.spinner("AI đang chuẩn bị câu hỏi..."):
                try:
                    questions = generate_questions(
                        vi_tri=role,
                        level=level,
                        loai=interview_type,
                        so_cau=so_cau,
                    )
                    st.session_state.interview_questions = questions
                    st.session_state.interview_role = role
                    st.session_state.interview_idx = 0
                    st.session_state.interview_answers = []
                    st.session_state.interview_evals = []
                    st.rerun()
                except Exception:
                    st.error("Không tạo được câu hỏi. Vui lòng thử lại.")
        return

    # ── In progress ──────────────────────────────────────────────────────────
    questions = st.session_state.interview_questions
    idx = st.session_state.interview_idx
    role = st.session_state.interview_role
    total = len(questions)

    # Finished
    if idx >= total:
        _show_summary(questions, st.session_state.interview_answers, st.session_state.interview_evals, role)
        return

    # Progress bar
    st.markdown(f"**Câu {idx + 1} / {total}** — {role}")
    st.progress((idx) / total)
    st.markdown("<div style='margin-top:1rem'></div>", unsafe_allow_html=True)

    # Question card
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg,#667eea12,#764ba212);
        border-left: 4px solid #667eea;
        border-radius: 8px;
        padding: 1.25rem 1.5rem;
        font-size: 1.1rem;
        font-weight: 600;
        color: #1f2937;
        margin-bottom: 1.5rem;
    ">
        {questions[idx]}
    </div>
    """, unsafe_allow_html=True)

    answer = st.text_area(
        "Câu trả lời của bạn",
        height=180,
        placeholder="Viết câu trả lời của bạn tại đây...",
        key=f"ans_{idx}",
        label_visibility="collapsed",
    )

    col_skip, col_submit = st.columns([1, 3])
    with col_skip:
        if st.button("⏭️  Bỏ qua", use_container_width=True):
            st.session_state.interview_answers.append("")
            st.session_state.interview_evals.append(None)
            st.session_state.interview_idx += 1
            st.rerun()
    with col_submit:
        if st.button("✅  Gửi câu trả lời", use_container_width=True, disabled=not answer.strip()):
            with st.spinner("AI đang chấm câu trả lời..."):
                evaluation = evaluate_answer(vi_tri=role, cau_hoi=questions[idx], tra_loi=answer)
            st.session_state.interview_answers.append(answer)
            st.session_state.interview_evals.append(evaluation)
            st.session_state.interview_idx += 1

            # Show feedback before moving on
            st.markdown("---")
            st.markdown("**Phản hồi:**")
            st.markdown(evaluation)
            st.markdown("---")
            if st.button("➡️  Câu tiếp theo", use_container_width=True):
                st.rerun()


def _show_summary(questions, answers, evals, role):
    st.markdown("## 🏁 Kết quả phỏng vấn")
    st.markdown(f"**Vị trí:** {role}")

    scores = []
    for ev in evals:
        if ev:
            for line in ev.split("\n"):
                if "Điểm:" in line:
                    try:
                        score = float(line.split(":")[1].strip().split("/")[0].strip())
                        scores.append(score)
                    except Exception:
                        pass

    if scores:
        avg = sum(scores) / len(scores)
        st.markdown(f"### Điểm trung bình: **{avg:.1f} / 10**")
        grade = "Xuất sắc 🏆" if avg >= 8.5 else "Tốt 👍" if avg >= 7 else "Khá 📈" if avg >= 5.5 else "Cần cải thiện 💪"
        st.markdown(f"**Xếp loại:** {grade}")
        st.progress(avg / 10)

    st.markdown("---")
    st.markdown("### Chi tiết từng câu")
    for i, (q, a, ev) in enumerate(zip(questions, answers, evals)):
        with st.expander(f"Câu {i+1}: {q[:80]}..."):
            if a:
                st.markdown(f"**Câu trả lời của bạn:** {a}")
            else:
                st.markdown("*Đã bỏ qua câu này*")
            if ev:
                st.markdown("---")
                st.markdown(ev)

    st.markdown("---")
    if st.button("🔄  Phỏng vấn lại từ đầu", use_container_width=True):
        for key in ["interview_questions", "interview_role", "interview_idx", "interview_answers", "interview_evals"]:
            if key in st.session_state:
                del st.session_state[key]
        st.rerun()
