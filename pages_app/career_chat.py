import streamlit as st
from utils.llm_client import chat

SYSTEM = """Bạn là chuyên gia tư vấn nghề nghiệp IT tại Việt Nam với 10 năm kinh nghiệm.
Bạn am hiểu thị trường tuyển dụng IT Việt Nam, mức lương, lộ trình sự nghiệp, kỹ năng cần có.
Phong cách: thân thiện, thẳng thắn, thực tế — như người anh/chị trong ngành đang tư vấn cho em.
Trả lời bằng tiếng Việt, ngắn gọn và có ích. Dùng bullet points khi liệt kê."""

SUGGESTED_QUESTIONS = [
    "Lộ trình trở thành AI Engineer từ sinh viên mới ra trường?",
    "Mức lương Software Engineer tại Việt Nam hiện tại?",
    "Nên học thêm kỹ năng gì để tăng lương nhanh?",
    "Sự khác nhau giữa Backend Engineer và Full-Stack Engineer?",
    "Làm thế nào để chuyển ngành sang IT khi đã đi làm?",
    "Khi nào nên nghĩ đến việc đổi công ty?",
]


def render():
    st.markdown("## 💬 Tư vấn nghề nghiệp")
    st.markdown("Hỏi bất cứ điều gì về sự nghiệp IT — lộ trình, lương, kỹ năng, chiến lược tìm việc.")
    st.markdown("<div style='margin-top:0.5rem'></div>", unsafe_allow_html=True)

    # Init history
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # Suggested questions (only when empty)
    if not st.session_state.chat_history:
        st.markdown("#### Câu hỏi gợi ý")
        cols = st.columns(2)
        for i, q in enumerate(SUGGESTED_QUESTIONS):
            with cols[i % 2]:
                if st.button(q, key=f"suggest_{i}", use_container_width=True):
                    st.session_state.chat_history.append({"role": "user", "content": q})
                    with st.spinner("Đang trả lời..."):
                        reply = _get_reply(q)
                    st.session_state.chat_history.append({"role": "assistant", "content": reply})
                    st.rerun()
        st.markdown("---")

    # Chat history
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"], avatar="🧑" if msg["role"] == "user" else "🧠"):
            st.markdown(msg["content"])

    # Input
    user_input = st.chat_input("Nhập câu hỏi của bạn...")
    if user_input:
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        with st.chat_message("user", avatar="🧑"):
            st.markdown(user_input)

        with st.chat_message("assistant", avatar="🧠"):
            with st.spinner("Đang trả lời..."):
                reply = _get_reply(user_input)
            st.markdown(reply)

        st.session_state.chat_history.append({"role": "assistant", "content": reply})

    # Clear button
    if st.session_state.chat_history:
        if st.button("🗑️  Xóa lịch sử chat", use_container_width=False):
            st.session_state.chat_history = []
            st.rerun()


def _get_reply(user_msg: str) -> str:
    history = st.session_state.chat_history
    messages_for_context = history[-8:]  # last 4 exchanges

    # Build context string
    context = ""
    for m in messages_for_context[:-1]:
        prefix = "Người dùng" if m["role"] == "user" else "Tư vấn viên"
        context += f"{prefix}: {m['content']}\n\n"

    prompt = f"{context}Người dùng: {user_msg}"
    try:
        return chat(prompt=prompt, system=SYSTEM, provider="groq")
    except Exception:
        return "Xin lỗi, tôi đang gặp sự cố kỹ thuật. Vui lòng thử lại sau ít phút."
