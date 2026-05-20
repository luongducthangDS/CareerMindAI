# 🧠 CareerMind AI

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10-blue?logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/Streamlit-1.45-FF4B4B?logo=streamlit&logoColor=white" />
  <img src="https://img.shields.io/badge/Groq-LLaMA%203.3%2070B-f55036?logo=meta&logoColor=white" />
  <img src="https://img.shields.io/badge/Deploy-Railway-0B0D0E?logo=railway&logoColor=white" />
  <img src="https://img.shields.io/badge/License-MIT-green" />
</p>

<p align="center">
  <b>Trợ lý nghề nghiệp AI toàn diện — từ phân tích CV đến luyện phỏng vấn</b><br/>
  AI-powered career assistant built with Streamlit & Groq LLaMA 3.3
</p>

---

## ✨ Tính năng

| Tính năng | Mô tả |
|-----------|-------|
| 📄 **Phân tích CV** | Upload PDF/DOCX → AI chấm điểm, liệt kê điểm mạnh/yếu, gợi ý cải thiện |
| ✍️ **Tạo CV mới** | Form nhập thông tin → AI cải thiện ngôn từ → Export file Word (.docx) |
| 💼 **Thư xin việc** | Nhập thông tin công ty → AI viết thư cá nhân hóa → Chỉnh sửa & tải về |
| 🎯 **Phân tích JD** | Dán tin tuyển dụng → AI phân tích yêu cầu + tính % match với CV |
| 🎤 **Phỏng vấn thử** | Chọn role/level → AI tạo câu hỏi → Chấm điểm từng câu → Tổng kết |
| 💬 **Tư vấn nghề nghiệp** | Chat với AI về lộ trình, lương, kỹ năng IT tại Việt Nam |

---

## 🛠️ Tech Stack

- **Frontend:** [Streamlit](https://streamlit.io/)
- **LLM:** [Groq](https://groq.com/) — LLaMA 3.3 70B (fast inference, free tier)
- **Document parsing:** `pdfplumber`, `python-docx`
- **Vector DB:** ChromaDB (lưu lịch sử phân tích)
- **Export:** `python-docx` (Word .docx)
- **Deploy:** [Railway](https://railway.app/)

---

## 🚀 Chạy local

### 1. Clone repo
```bash
git clone https://github.com/YOUR_USERNAME/CareerMindAI.git
cd CareerMindAI
```

### 2. Tạo virtual environment
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

### 3. Cài dependencies
```bash
pip install -r requirements.txt
```

### 4. Tạo file `.env`
```bash
cp .env.example .env
```
Mở `.env` và điền API key:
```
GROQ_API_KEY=your_groq_api_key_here
```
> 🔑 Lấy Groq API key miễn phí tại [console.groq.com](https://console.groq.com)

### 5. Chạy app
```bash
streamlit run app.py
```
Truy cập: **http://localhost:8501**

---

## ☁️ Deploy lên Railway

### 1. Push code lên GitHub
```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/YOUR_USERNAME/CareerMindAI.git
git push -u origin main
```

### 2. Deploy Railway
1. Vào [railway.app](https://railway.app) → **New Project** → **Deploy from GitHub repo**
2. Chọn repo `CareerMindAI`
3. Vào **Settings → Variables**, thêm:
   ```
   GROQ_API_KEY = your_groq_api_key_here
   ```
4. Railway tự động build và deploy ✅

> Railway free tier: $5 credit/tháng, đủ dùng cho demo portfolio.

---

## 📁 Cấu trúc project

```
CareerMindAI/
├── app.py                    # Entry point & routing
├── pages_app/
│   ├── home.py               # Trang chủ
│   ├── cv_analyzer.py        # Phân tích CV
│   ├── cv_generator.py       # Tạo CV mới
│   ├── cover_letter.py       # Thư xin việc
│   ├── jd_analyzer.py        # Phân tích JD
│   ├── mock_interview.py     # Phỏng vấn thử
│   └── career_chat.py        # Tư vấn nghề nghiệp
├── utils/
│   ├── llm_client.py         # Groq / Gemini wrapper
│   ├── document_parser.py    # PDF & DOCX text extraction
│   ├── cv_analyzer.py        # CV analysis prompts
│   ├── cv_generator_llm.py   # CV enhancement prompts
│   ├── jd_analyzer_llm.py    # JD analysis prompts
│   ├── cover_letter_llm.py   # Cover letter prompts
│   ├── interview_llm.py      # Interview Q&A prompts
│   ├── docx_exporter.py      # Word document export
│   └── vector_store.py       # ChromaDB (optional)
├── .streamlit/config.toml    # Theme & server config
├── railway.toml              # Railway deploy config
├── Procfile                  # Alternative deploy config
├── requirements.txt
└── .env.example
```

---

## 🔧 Biến môi trường

| Biến | Bắt buộc | Mô tả |
|------|----------|-------|
| `GROQ_API_KEY` | ✅ | API key từ console.groq.com |
| `GEMINI_API_KEY` | ❌ | Dự phòng, không bắt buộc |
| `CHROMA_PATH` | ❌ | Đường dẫn lưu ChromaDB (mặc định: `chroma_db/`) |

---

## 👨‍💻 Tác giả

**Lương Đức Thắng**
- Email: luongducthang289@gmail.com
- GitHub: [@YOUR_USERNAME](https://github.com/YOUR_USERNAME)

---

## 📄 License

MIT License — free to use, modify and distribute.
