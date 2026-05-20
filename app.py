import streamlit as st
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(
    page_title="CareerMind AI — Trợ lý nghề nghiệp thông minh",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
    /* Reset sidebar padding */
    [data-testid="stSidebar"] { padding-top: 0; }
    [data-testid="stSidebar"] > div:first-child { padding-top: 1.5rem; }

    /* Sidebar brand */
    .sidebar-brand {
        font-size: 1.3rem;
        font-weight: 700;
        color: #667eea;
        padding: 0 1rem 1rem 1rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    .sidebar-tagline {
        font-size: 0.78rem;
        color: #9ca3af;
        padding: 0 1rem 1rem 1rem;
        margin-top: -0.8rem;
    }

    /* Hide radio label */
    [data-testid="stRadio"] > label { display: none; }

    /* Style radio options as nav items */
    [data-testid="stRadio"] > div {
        gap: 0.2rem;
    }
    [data-testid="stRadio"] > div > label {
        display: flex !important;
        align-items: center;
        padding: 0.6rem 1rem;
        border-radius: 8px;
        cursor: pointer;
        font-size: 0.95rem;
        color: #374151;
        transition: background 0.15s;
        width: 100%;
    }
    [data-testid="stRadio"] > div > label:hover {
        background: #f3f4f6;
    }
    [data-testid="stRadio"] > div > label:has(input:checked) {
        background: #ede9fe;
        color: #7c3aed;
        font-weight: 600;
    }
    [data-testid="stRadio"] > div > label > div:first-child { display: none; }

    /* Main content */
    .main-hero-title {
        font-size: 2.8rem;
        font-weight: 800;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        line-height: 1.2;
        margin-bottom: 0.75rem;
    }
    .main-hero-sub {
        color: #6b7280;
        font-size: 1.15rem;
        margin-bottom: 2.5rem;
        line-height: 1.6;
    }
    .feature-card {
        background: white;
        border: 1px solid #e5e7eb;
        border-radius: 16px;
        padding: 1.75rem;
        height: 100%;
        box-shadow: 0 1px 4px rgba(0,0,0,0.06);
        transition: box-shadow 0.2s, transform 0.2s;
    }
    .feature-card:hover {
        box-shadow: 0 4px 16px rgba(102,126,234,0.15);
        transform: translateY(-2px);
    }
    .feature-card h3 {
        font-size: 1.1rem;
        font-weight: 700;
        color: #1f2937;
        margin-bottom: 0.5rem;
    }
    .feature-card p {
        font-size: 0.9rem;
        color: #6b7280;
        line-height: 1.55;
        margin: 0;
    }
    .feature-card .badge {
        display: inline-block;
        font-size: 0.7rem;
        font-weight: 600;
        padding: 0.15rem 0.5rem;
        border-radius: 20px;
        margin-bottom: 0.75rem;
    }
    .badge-active { background: #d1fae5; color: #065f46; }
    .badge-soon { background: #f3f4f6; color: #9ca3af; }

    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white !important;
        border: none !important;
        border-radius: 10px;
        padding: 0.65rem 2rem;
        font-weight: 600;
        font-size: 1rem;
        letter-spacing: 0.01em;
        transition: opacity 0.2s, transform 0.1s;
    }
    .stButton > button:hover {
        opacity: 0.9;
        transform: translateY(-1px);
    }
    .stButton > button:active { transform: translateY(0); }

    /* Upload area */
    [data-testid="stFileUploader"] {
        border-radius: 12px;
    }

    /* Coming soon page */
    .coming-soon-box {
        text-align: center;
        padding: 5rem 2rem;
        color: #9ca3af;
    }
    .coming-soon-box .icon { font-size: 4rem; margin-bottom: 1rem; }
    .coming-soon-box h2 { color: #374151; font-size: 1.5rem; margin-bottom: 0.5rem; }
    .coming-soon-box p { font-size: 1rem; color: #6b7280; }

    /* Divider */
    hr { border: none; border-top: 1px solid #f3f4f6; margin: 2rem 0; }

    /* Success/info styling */
    .stAlert { border-radius: 10px; }

    /* Selectbox */
    [data-testid="stSelectbox"] label { font-weight: 600; color: #374151; }
</style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown('<div class="sidebar-brand">🧠 CareerMind AI</div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-tagline">Trợ lý nghề nghiệp thông minh</div>', unsafe_allow_html=True)
    st.markdown("---")

    page = st.radio(
        "Menu",
        [
            "🏠  Trang chủ",
            "📄  Phân tích CV",
            "✍️  Tạo CV mới",
            "💼  Thư xin việc",
            "🎯  Phân tích tin tuyển dụng",
            "🎤  Phỏng vấn thử",
            "💬  Tư vấn nghề nghiệp",
        ],
        label_visibility="collapsed",
    )

# Routing
if page == "🏠  Trang chủ":
    from pages_app import home
    home.render()
elif page == "📄  Phân tích CV":
    from pages_app import cv_analyzer
    cv_analyzer.render()
elif page == "✍️  Tạo CV mới":
    from pages_app import cv_generator
    cv_generator.render()
elif page == "💼  Thư xin việc":
    from pages_app import cover_letter
    cover_letter.render()
elif page == "🎯  Phân tích tin tuyển dụng":
    from pages_app import jd_analyzer
    jd_analyzer.render()
elif page == "🎤  Phỏng vấn thử":
    from pages_app import mock_interview
    mock_interview.render()
elif page == "💬  Tư vấn nghề nghiệp":
    from pages_app import career_chat
    career_chat.render()
