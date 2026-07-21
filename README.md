# 📚 AI Study Assistant

> **Biến tài liệu học tập thành kiến thức — ngay lập tức, nhờ sức mạnh của Gemini AI.**

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100%2B-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.x-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io)
[![Gemini AI](https://img.shields.io/badge/Gemini-AI-4285F4?style=for-the-badge&logo=google&logoColor=white)](https://ai.google.dev)
[![SQLite](https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white)](https://sqlite.org)

---

## 🎯 Giới thiệu

**AI Study Assistant** là một ứng dụng web thông minh giúp sinh viên và người học tự động hóa quá trình ôn tập từ tài liệu bài giảng. Chỉ cần **upload file PDF hoặc TXT**, hệ thống sẽ:

- 📝 **Tóm tắt** toàn bộ nội dung bằng AI — rõ ràng, súc tích, bằng Tiếng Việt
- 🧠 **Tạo bộ câu hỏi trắc nghiệm** (20 câu) từ nội dung tài liệu để kiểm tra kiến thức
- 💾 **Lưu lịch sử** tất cả tài liệu đã xử lý, có thể xem lại bất cứ lúc nào

---

## ✨ Tính năng nổi bật

| Tính năng | Mô tả |
|---|---|
| 📤 **Upload thông minh** | Hỗ trợ PDF & TXT, tự động trích xuất nội dung |
| 🤖 **Tóm tắt bằng AI** | Dùng Google Gemini để tóm tắt bài giảng bằng Tiếng Việt |
| 🎲 **Sinh Quiz tự động** | Tạo 20 câu hỏi trắc nghiệm 4 lựa chọn từ tài liệu |
| ✅ **Chấm điểm tức thì** | Nộp bài và nhận kết quả ngay lập tức |
| 📁 **Lịch sử tài liệu** | Sidebar lưu toàn bộ file đã upload, click để xem lại |
| 🔒 **Không bị lặp** | Cơ chế chống upload trùng file, chống rerun vô tận |

---

## 🏗️ Kiến trúc hệ thống

```
┌─────────────────────────────────────────────────────────────┐
│                    NGƯỜI DÙNG (Browser)                     │
└──────────────────────────┬──────────────────────────────────┘
                           │ HTTP
┌──────────────────────────▼──────────────────────────────────┐
│              FRONTEND — Streamlit (port 8501)               │
│                        src/app.py                           │
│   Upload UI │ Tóm tắt │ Quiz │ Sidebar lịch sử             │
└──────────────────────────┬──────────────────────────────────┘
                           │ REST API calls
┌──────────────────────────▼──────────────────────────────────┐
│              BACKEND — FastAPI (port 8000)                  │
│                        src/main.py                          │
│  POST /api/upload  │  POST /api/documents/{id}/summarize   │
│  POST /api/documents/{id}/quiz  │  GET /api/history        │
└────────────┬─────────────────────────┬───────────────────────┘
             │                         │
┌────────────▼──────────┐   ┌──────────▼───────────────────────┐
│  SQLite Database      │   │   Google Gemini AI API           │
│  study_assistant.db   │   │   (gemini-flash-latest)          │
│                       │   │                                  │
│  Table: documents     │   │   • generate_content (text)      │
│  Table: study_notes   │   │   • response_mime_type JSON      │
└───────────────────────┘   └──────────────────────────────────┘
```

---

## 📂 Cấu trúc thư mục

```
ai_study_assistant/
│
├── 📁 src/
│   ├── app.py          # Frontend Streamlit — giao diện người dùng
│   ├── main.py         # Backend FastAPI — định nghĩa toàn bộ API endpoints
│   ├── services.py     # Logic AI — giao tiếp với Google Gemini
│   ├── database.py     # Cấu hình SQLAlchemy + SQLite
│   └── models.py       # ORM Models: Document, StudyNote
│
├── 📄 .env             # API keys (KHÔNG commit lên git!)
├── 📄 .gitignore
├── 📄 pyrefly.toml     # Cấu hình type checker Pyrefly
├── 📄 study_assistant.db  # SQLite database (tự tạo khi chạy)
└── 📄 README.md
```

---

## 🗄️ Database Schema

### Bảng `documents`
| Cột | Kiểu | Mô tả |
|---|---|---|
| `id` | INTEGER (PK) | ID tự tăng |
| `filename` | STRING (unique) | Tên file upload |
| `content` | TEXT | Nội dung text trích xuất |
| `created_at` | DATETIME | Thời điểm upload |

### Bảng `study_notes`
| Cột | Kiểu | Mô tả |
|---|---|---|
| `id` | INTEGER (PK) | ID tự tăng |
| `document_id` | INTEGER (FK) | Liên kết tới `documents.id` |
| `note_type` | STRING | `"summary"` hoặc `"quiz"` |
| `ai_response` | TEXT | Kết quả trả về từ Gemini |
| `created_at` | DATETIME | Thời điểm tạo |

---

## 🚀 Hướng dẫn cài đặt & chạy

### 1. Clone project

```bash
git clone <your-repo-url>
cd ai_study_assistant
```

### 2. Tạo môi trường ảo & cài dependencies

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS/Linux
source .venv/bin/activate

pip install fastapi uvicorn streamlit sqlalchemy python-dotenv google-genai pypdf
```

### 3. Cấu hình API Key

Tạo file `.env` ở thư mục gốc:

```env
GEMINI_API_KEY=your_api_key_here

# Tùy chọn: đổi model (mặc định là gemini-flash-latest)
# GEMINI_MODEL=gemini-pro-latest
```

> 🔑 Lấy API key miễn phí tại: https://aistudio.google.com/apikey

### 4. Chạy Backend (FastAPI)

```bash
uvicorn src.main:app --reload
```

Backend sẽ chạy tại: **http://127.0.0.1:8000**  
Tài liệu API tự động: **http://127.0.0.1:8000/docs**

### 5. Chạy Frontend (Streamlit) — mở terminal mới

```bash
streamlit run src/app.py
```

Frontend sẽ chạy tại: **http://localhost:8501**

---

## 📡 API Endpoints

| Method | Endpoint | Mô tả |
|---|---|---|
| `GET` | `/` | Kiểm tra server còn sống |
| `POST` | `/api/upload` | Upload file PDF/TXT |
| `POST` | `/api/documents/{id}/summarize` | Tạo tóm tắt AI |
| `POST` | `/api/documents/{id}/quiz` | Tạo 20 câu quiz |
| `GET` | `/api/history` | Lấy danh sách tất cả tài liệu |
| `GET` | `/api/history/{id}` | Xem chi tiết + lịch sử note của 1 tài liệu |

---

## ⚙️ Cấu hình Model AI

Model được cấu hình qua biến môi trường `GEMINI_MODEL` trong file `.env`:

```env
# Nhanh, miễn phí — dùng cho development (mặc định)
GEMINI_MODEL=gemini-flash-latest

# Mạnh hơn, phù hợp production
GEMINI_MODEL=gemini-pro-latest
```

> ⚠️ **Lưu ý quan trọng**: Không dùng model `gemini-2.5-flash-native-audio-latest` — đây là model xử lý **audio**, không sinh ra text output thông thường.

---

## 🛠️ Tech Stack

| Thành phần | Công nghệ | Vai trò |
|---|---|---|
| **Frontend** | Streamlit | Giao diện web, upload file, hiển thị kết quả |
| **Backend** | FastAPI + Uvicorn | REST API server, xử lý request |
| **AI Engine** | Google Gemini (`google-genai`) | Tóm tắt & sinh câu hỏi |
| **Database** | SQLite + SQLAlchemy ORM | Lưu trữ tài liệu & lịch sử |
| **PDF Parser** | pypdf | Đọc nội dung từ file PDF |
| **Config** | python-dotenv | Quản lý API key qua file `.env` |

---

## 🐛 Troubleshooting

### ❌ Lỗi "Chưa kết nối được với Backend"
→ Đảm bảo đã chạy `uvicorn src.main:app --reload` ở một terminal **riêng**.

### ❌ Lỗi `404 NOT_FOUND` khi gọi Gemini
→ Model đã bị deprecated. Kiểm tra và đổi `GEMINI_MODEL` trong `.env`.

### ❌ Lỗi `429 RESOURCE_EXHAUSTED`
→ API key đang dùng free tier đã hết quota. Chờ reset hoặc đổi sang model khác / nâng cấp plan tại Google AI Studio.

### ❌ Lỗi `response.text` trả về `None`
→ Model không hỗ trợ text output (ví dụ: audio model). Kiểm tra lại `GEMINI_MODEL`.

---

## 📋 Roadmap

- [ ] 🔐 Thêm xác thực người dùng (login/logout)
- [ ] 📊 Dashboard thống kê điểm quiz theo thời gian
- [ ] 🔍 Tìm kiếm trong lịch sử tài liệu
- [ ] 💬 Chat Q&A trực tiếp với tài liệu (RAG)
- [ ] 🌐 Deploy lên cloud (Railway / Render / GCP)
- [ ] 📱 Responsive mobile UI

---

## 👨‍💻 Tác giả

Được xây dựng trong khuôn khổ **Summer Project 2026** 🌞

---

> *"The beautiful thing about learning is that no one can take it away from you."* — B.B. King
