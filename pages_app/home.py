import streamlit as st


def render():
    # Hero
    st.markdown('<h1 class="main-hero-title">Tìm việc thông minh hơn<br>với AI bên cạnh bạn</h1>', unsafe_allow_html=True)
    st.markdown(
        '<p class="main-hero-sub">CareerMind AI phân tích CV, viết thư xin việc và luyện phỏng vấn —<br>giúp bạn tự tin ứng tuyển vào bất kỳ vị trí nào.</p>',
        unsafe_allow_html=True,
    )

    # Feature cards — row 1
    col1, col2, col3 = st.columns(3, gap="medium")

    with col1:
        st.markdown("""
        <div class="feature-card">
            <span class="badge badge-active">✦ Có sẵn</span>
            <h3>📄 Phân tích CV</h3>
            <p>Tải CV lên và nhận ngay nhận xét chi tiết: điểm mạnh, điểm yếu và gợi ý cải thiện cụ thể theo từng vị trí ứng tuyển.</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="feature-card">
            <span class="badge badge-active">✦ Có sẵn</span>
            <h3>✍️ Tạo CV mới</h3>
            <p>Tạo CV chuyên nghiệp, chuẩn ATS từ thông tin của bạn. AI cải thiện ngôn từ và xuất file Word ngay.</p>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="feature-card">
            <span class="badge badge-active">✦ Có sẵn</span>
            <h3>💼 Thư xin việc</h3>
            <p>Viết thư xin việc cá nhân hoá trong vài giây — tự động khớp với yêu cầu của từng tin tuyển dụng.</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='margin-top:1.25rem'></div>", unsafe_allow_html=True)

    # Feature cards — row 2
    col4, col5, col6 = st.columns(3, gap="medium")

    with col4:
        st.markdown("""
        <div class="feature-card">
            <span class="badge badge-active">✦ Có sẵn</span>
            <h3>🎯 Phân tích tin tuyển dụng</h3>
            <p>Dán nội dung JD vào — xem ngay bạn phù hợp bao nhiêu % và cần bổ sung kỹ năng gì.</p>
        </div>
        """, unsafe_allow_html=True)

    with col5:
        st.markdown("""
        <div class="feature-card">
            <span class="badge badge-active">✦ Có sẵn</span>
            <h3>🎤 Phỏng vấn thử</h3>
            <p>Luyện tập câu hỏi kỹ thuật và hành vi với AI — nhận phản hồi tức thì cho từng câu trả lời.</p>
        </div>
        """, unsafe_allow_html=True)

    with col6:
        st.markdown("""
        <div class="feature-card">
            <span class="badge badge-active">✦ Có sẵn</span>
            <h3>💬 Tư vấn nghề nghiệp</h3>
            <p>Hỏi bất cứ điều gì về lộ trình sự nghiệp, mức lương thị trường hay kỹ năng cần học tiếp theo.</p>
        </div>
        """, unsafe_allow_html=True)

    # CTA
    st.markdown("<div style='margin-top:2.5rem'></div>", unsafe_allow_html=True)
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, #667eea15 0%, #764ba215 100%);
        border: 1px solid #667eea30;
        border-radius: 16px;
        padding: 2rem 2.5rem;
        display: flex;
        align-items: center;
        justify-content: space-between;
        flex-wrap: wrap;
        gap: 1rem;
    ">
        <div>
            <h3 style="margin:0; color:#1f2937; font-size:1.2rem;">Bắt đầu ngay với CV của bạn</h3>
            <p style="margin:0.4rem 0 0 0; color:#6b7280; font-size:0.9rem;">
                Chỉ mất 30 giây để nhận phân tích CV đầy đủ từ AI.
            </p>
        </div>
        <div style="font-size:0.9rem; color:#667eea; font-weight:600;">
            👈 Chọn <em>Phân tích CV</em> ở menu bên trái
        </div>
    </div>
    """, unsafe_allow_html=True)
