"""
Rate limiting đơn giản theo session — tránh spam API.
Mỗi session (tab trình duyệt) có giới hạn riêng, lưu trong st.session_state.
"""
import streamlit as st

# Giới hạn số lần gọi LLM mỗi tính năng trong một session
LIMITS = {
    "cv_analyze": 5,
    "cv_enhance": 3,
    "cover_letter": 5,
    "jd_analyze": 10,
    "interview_gen": 3,
    "interview_eval": 20,
    "chat": 30,
}


def check_limit(feature: str) -> tuple[bool, int, int]:
    """
    Kiểm tra xem session còn được gọi không.
    Trả về (allowed: bool, used: int, limit: int).
    """
    key = f"rate_{feature}"
    if key not in st.session_state:
        st.session_state[key] = 0

    limit = LIMITS.get(feature, 10)
    used = st.session_state[key]
    return used < limit, used, limit


def consume(feature: str) -> None:
    """Tăng counter sau mỗi lần gọi thành công."""
    key = f"rate_{feature}"
    if key not in st.session_state:
        st.session_state[key] = 0
    st.session_state[key] += 1


def guard(feature: str) -> bool:
    """
    Dùng trước khi gọi LLM. Nếu hết lượt thì hiển thị cảnh báo và trả về False.
    """
    allowed, used, limit = check_limit(feature)
    if not allowed:
        st.warning(
            f"Bạn đã sử dụng tính năng này {used}/{limit} lần trong phiên hiện tại. "
            "Vui lòng tải lại trang để tiếp tục.",
            icon="⚠️",
        )
    return allowed
