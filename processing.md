# CareerMind AI — Nhật ký tiến độ dự án

> File này ghi lại **toàn bộ quá trình xây dựng** từng bước. Đọc từ đầu để nắm bức tranh tổng thể, đọc phần cuối để biết đang làm đến đâu và cần làm gì tiếp.

---

## Tổng quan dự án

**Mục tiêu:** Xây dựng MVP AI career assistant trong 6 tuần, deploy production, dùng thật được và khoe portfolio.

**Tech stack:**
- Frontend: Streamlit
- LLM: Groq (`llama-3.3-70b-versatile`) + Gemini Flash (dự phòng)
- Vector DB: ChromaDB (persistent, lưu local)
- Document parsing: pdfplumber, python-docx
- Deployment: Railway (free tier) — Tuần 5
- Python: 3.10.11
- Venv: `venv/` (không commit)

**Cách chạy local:**
```bash
cd "D:\Projects for CV\CareerMindAI"
venv\Scripts\activate
streamlit run app.py
# → http://localhost:8501
```

**API keys** (trong file `.env`, không commit):
- `GROQ_API_KEY` — đã có, đang dùng
- `GEMINI_API_KEY` — chưa cần, để dự phòng

---

## Cấu trúc thư mục

```
CareerMindAI/
├── app.py                      # Entry point: config, CSS, sidebar nav, routing
├── processing.md               # File này — nhật ký tiến độ
├── requirements.txt            # Dependencies
├── .env                        # API keys (không commit)
├── .env.example                # Template .env
├── .gitignore
├── .streamlit/
│   └── config.toml             # Theme tím, port 8501
├── .claude/
│   └── launch.json             # Preview server config cho Claude Code
├── chroma_db/                  # Vector DB lưu CV + analysis (tự tạo khi chạy)
├── pages_app/
│   ├── __init__.py
│   ├── home.py                 # Trang chủ: hero + 6 feature cards
│   └── cv_analyzer.py          # Phân tích CV: upload → chọn role → analyze
└── utils/
    ├── __init__.py
    ├── document_parser.py      # Extract text từ PDF và DOCX
    ├── llm_client.py           # Wrapper gọi Groq / Gemini
    ├── cv_analyzer.py          # Prompt phân tích CV, gọi LLM
    └── vector_store.py         # Lưu CV + analysis vào ChromaDB
```

---

## Kế hoạch 6 tuần

| Tuần | Mục tiêu | Trạng thái |
|------|-----------|------------|
| 1 | Nền tảng + CV Analyzer | ✅ Xong |
| 2 | CV Generator | ✅ Xong |
| 3 | Cover Letter + JD Analyzer | ✅ Xong |
| 4 | Mock Interview + Career Chat | ✅ Xong |
| 5 | Deploy Railway + Google Login | 🔜 Chưa bắt đầu |
| 6 | Polish, README, Video demo | 🔜 Chưa bắt đầu |

---

## ✅ TUẦN 1 — Nền tảng & CV Analyzer (XONG)

### Đã làm

**1. Setup project**
- Tạo venv Python 3.10, cài toàn bộ dependencies
- Cấu hình Streamlit theme (màu tím `#667eea`)
- Bỏ `sentence-transformers` (quá nặng, kéo theo PyTorch ~2GB) → dùng `DefaultEmbeddingFunction` của ChromaDB (dùng onnxruntime, nhẹ hơn nhiều)
- Sửa model Groq: `llama-3.1-70b-versatile` đã bị decommission → đổi sang `llama-3.3-70b-versatile`

**2. CV Analyzer** (`pages_app/cv_analyzer.py`)
- Upload PDF / DOCX → tự động extract text (ẩn, không hiện raw text cho user)
- Chọn vị trí ứng tuyển: dropdown 6 role phổ biến + option "✏️ Nhập vị trí khác..." → hiện text input tự do
- Gọi Groq LLM phân tích: điểm /100, strengths, weaknesses, improvements, missing keywords, quick wins, match score
- Lưu CV + analysis vào ChromaDB (session_id random)
- Download kết quả dạng `.txt`
- Nút "Phân tích lại" xóa state và rerun

**3. UI/UX — toàn bộ tiếng Việt, thiết kế theo góc nhìn người dùng**
- Sidebar: navigation tiếng Việt, không có radio button thô, item active highlight tím
- Bỏ hoàn toàn: "Week 1 MVP", "✅/🔜", "LLM Provider", "Extracted CV Text", "character count"
- Trang "Sắp ra mắt" thay vì "Coming in Week 2!" bằng tiếng Anh
- Home page: hero gradient, 6 feature cards với badge "Có sẵn" / "Sắp ra mắt"
- CV Analyzer: flow 3 bước rõ ràng (Tải lên → Chọn vị trí → Phân tích)
- Empty state có dashed border + icon thay vì trang trắng

### Vấn đề đã gặp & cách xử lý

| Vấn đề | Giải pháp |
|--------|-----------|
| `pip install` MemoryError do torch quá nặng | Bỏ `sentence-transformers`, cài từng nhóm package nhỏ |
| Model `llama-3.1-70b-versatile` bị decommission | Đổi sang `llama-3.3-70b-versatile` trong `utils/llm_client.py` |
| Windows encoding: UnicodeDecodeError khi đọc file | Mở file với `encoding='utf-8'` |

---

## ✅ TUẦN 2 — CV Generator (XONG)

### Cần làm

1. **Tạo file** `pages_app/cv_generator.py`
2. **Form nhập thông tin:**
   - Họ tên, email, phone, địa chỉ, LinkedIn/GitHub
   - Tóm tắt bản thân (summary)
   - Kinh nghiệm làm việc (dynamic: thêm/xóa từng mục)
   - Học vấn
   - Kỹ năng
   - Dự án cá nhân
3. **Chọn template:** IT-focused, tối giản, chuyên nghiệp
4. **Generate CV** dùng LLM: cải thiện ngôn từ, viết bullet points ấn tượng
5. **Export PDF:** dùng `reportlab` hoặc `weasyprint`
6. Thêm route trong `app.py`: `elif page == "✍️  Tạo CV mới":`

### Dependencies cần cài thêm
```
reportlab  # hoặc weasyprint để export PDF
```

---

## ✅ TUẦN 3 — Cover Letter & JD Analyzer (XONG)

### Cần làm

**JD Analyzer** (`pages_app/jd_analyzer.py`):
1. Textarea nhập nội dung JD (paste từ website tuyển dụng)
2. LLM trích xuất: yêu cầu kỹ năng, kinh nghiệm, văn hóa công ty
3. So sánh với CV đã lưu trong session → tính % match
4. Hiển thị: kỹ năng có, kỹ năng thiếu, gợi ý bổ sung

**Cover Letter** (`pages_app/cover_letter.py`):
1. Input: tên công ty, vị trí, tên người nhận (tùy chọn)
2. Lấy CV text từ session (đã upload ở CV Analyzer) HOẶC cho upload lại
3. LLM generate thư xin việc cá nhân hóa theo JD
4. Cho chỉnh sửa trực tiếp trên app
5. Copy to clipboard + download `.docx`

---

## ✅ TUẦN 4 — Mock Interview & Career Chat (XONG)

### Cần làm

**Mock Interview** (`pages_app/mock_interview.py`):
1. Chọn loại phỏng vấn: Technical / Behavioral / Mixed
2. Chọn vị trí → LLM sinh câu hỏi phù hợp
3. User trả lời → LLM chấm điểm + nhận xét từng câu
4. Tổng kết sau phỏng vấn: điểm mạnh, điểm cần cải thiện

**Career Chat** (`pages_app/career_chat.py`):
1. Chat interface (`st.chat_message`, `st.chat_input`)
2. System prompt: chuyên gia tư vấn nghề nghiệp IT tại Việt Nam
3. Nhớ context trong session (lưu history vào `st.session_state`)
4. Gợi ý câu hỏi mẫu cho user mới

---

## 🔜 TUẦN 5 — Deploy + Auth (Chưa bắt đầu)

### Cần làm

1. **Deploy Railway:**
   - Tạo `Procfile`: `web: streamlit run app.py --server.port $PORT --server.address 0.0.0.0`
   - Set environment variables trên Railway dashboard
   - Push code lên GitHub → connect Railway

2. **Google Login (tùy chọn):**
   - Dùng `streamlit-google-auth` hoặc `authlib`
   - Lưu user session

3. **ChromaDB trên cloud:**
   - Hiện tại lưu local (`chroma_db/`) — cần chuyển sang persistent storage
   - Option 1: Mount Railway volume
   - Option 2: Dùng Chroma Cloud (có free tier)

---

## 🔜 TUẦN 6 — Polish & Portfolio (Chưa bắt đầu)

### Cần làm

1. **UI Polish:** kiểm tra responsive, dark mode, loading states
2. **README.md** chuyên nghiệp: badges, screenshot, demo GIF, hướng dẫn cài
3. **Video demo** (1-2 phút): quay màn hình, narrate bằng tiếng Anh/Việt
4. **Portfolio writeup:** Notion hoặc blog — vấn đề gặp, giải pháp, học được gì
5. **Chuẩn bị phỏng vấn:** câu hỏi về dự án (tech choices, challenges, scale)

---

## Ghi chú kỹ thuật

### Cách LLM phân tích CV
- File: `utils/cv_analyzer.py`
- System prompt: vai trò hiring manager tại tech company
- User prompt: CV text + target role → trả về markdown có cấu trúc cố định
- Ngôn ngữ output: tự động theo ngôn ngữ CV (tiếng Việt CV → tiếng Việt kết quả)
- Provider mặc định: `groq` (nhanh, miễn phí)

### ChromaDB
- Lưu tại: `chroma_db/` (tự tạo khi chạy lần đầu)
- Collection: `cv_store`
- Mỗi lần phân tích → upsert 1 document với session_id ngẫu nhiên
- Embedding: `DefaultEmbeddingFunction` (onnxruntime, không cần GPU)

### Session state Streamlit
| Key | Nội dung |
|-----|----------|
| `cv_text` | Text extract từ CV |
| `last_file` | Tên file CV đã upload |
| `cv_analysis` | Kết quả phân tích markdown |
| `analysis_role` | Vị trí ứng tuyển (tiếng Việt) |
| `cv_session_id` | UUID lưu vào ChromaDB |

---

## Nhật ký cập nhật

| Ngày | Nội dung |
|------|----------|
| 2026-05-21 | Khởi tạo project, setup venv, cài dependencies |
| 2026-05-21 | Build CV Analyzer: upload, extract, LLM analysis, ChromaDB |
| 2026-05-21 | Redesign UI: tiếng Việt toàn bộ, bỏ backend noise, flow 3 bước |
| 2026-05-21 | Fix: model Groq decommissioned → llama-3.3-70b-versatile |
| 2026-05-21 | Fix Bước 2: thêm option "Nhập vị trí khác..." với text input tự do |
| 2026-05-21 | Build Tuần 2: CV Generator — form 4 tab, dynamic add/remove, AI enhance, export DOCX |
| 2026-05-21 | Build Tuần 3: JD Analyzer — phân tích JD + so sánh CV; Cover Letter — generate + edit + export |
| 2026-05-21 | Build Tuần 4: Mock Interview — gen câu hỏi, chấm điểm, tổng kết; Career Chat — chat với context history |
| 2026-05-21 | Update home page: tất cả 6 tính năng badge "Có sẵn"; update app.py routing đầy đủ |
