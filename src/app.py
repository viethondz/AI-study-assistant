import streamlit as st
import requests

# Cấu hình giao diện Streamlit
st.set_page_config(page_title="AI Study Assistant", page_icon="📚", layout="wide")

# --- CUSTOM CSS FOR DARK GLASSMORPHIC THEME ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

    html, body, [class*="css"]  {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    .stApp {
        background: linear-gradient(135deg, #090d16 0%, #0f172a 50%, #1e1b4b 100%);
        color: #f8fafc;
    }

    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 4rem;
        max-width: 1300px;
    }

    /* Custom Header Banner */
    .header-banner {
        text-align: center;
        padding: 2rem 1.5rem;
        background: rgba(30, 41, 59, 0.45);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 24px;
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.35);
        margin-bottom: 1.75rem;
    }

    .header-title {
        background: linear-gradient(135deg, #38bdf8 0%, #818cf8 50%, #c084fc 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 2.6rem;
        font-weight: 800;
        letter-spacing: -0.03em;
        margin-bottom: 0.4rem;
    }

    .header-subtitle {
        color: #94a3b8;
        font-size: 1.05rem;
        font-weight: 500;
    }

    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: rgba(15, 23, 42, 0.95) !important;
        border-right: 1px solid rgba(255, 255, 255, 0.08);
    }
    
    section[data-testid="stSidebar"] .stButton > button {
        width: 100%;
        background: rgba(30, 41, 59, 0.6);
        color: #cbd5e1;
        border: 1px solid rgba(255, 255, 255, 0.06);
        border-radius: 12px;
        text-align: left;
        padding: 0.65rem 1rem;
        font-weight: 500;
        transition: all 0.2s ease;
    }

    section[data-testid="stSidebar"] .stButton > button:hover {
        background: linear-gradient(135deg, rgba(99, 102, 241, 0.25), rgba(168, 85, 247, 0.25));
        border-color: rgba(168, 85, 247, 0.5);
        color: #ffffff;
        transform: translateX(4px);
    }

    /* Primary Button Styling */
    .stButton > button {
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
        color: white;
        border: none;
        border-radius: 12px;
        font-weight: 600;
        font-size: 0.95rem;
        padding: 0.65rem 1.4rem;
        box-shadow: 0 4px 15px rgba(99, 102, 241, 0.35);
        transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
    }

    .stButton > button:hover {
        background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%);
        box-shadow: 0 6px 20px rgba(124, 58, 237, 0.5);
        transform: translateY(-2px);
        color: white;
    }

    /* File Uploader Container */
    section[data-testid="stFileUploader"] {
        background: rgba(30, 41, 59, 0.35);
        border: 2px dashed rgba(99, 102, 241, 0.4);
        border-radius: 18px;
        padding: 1.5rem;
        transition: border-color 0.3s ease;
    }

    section[data-testid="stFileUploader"]:hover {
        border-color: #818cf8;
    }

    /* Custom Card */
    .glass-card {
        background: rgba(30, 41, 59, 0.45);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 18px;
        padding: 1.5rem;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
        margin-top: 1rem;
    }

    /* Radio Group Box for Quiz */
    div[role="radiogroup"] {
        background: rgba(15, 23, 42, 0.6);
        padding: 0.85rem 1.1rem;
        border-radius: 12px;
        border: 1px solid rgba(255, 255, 255, 0.06);
        margin-top: 0.5rem;
        margin-bottom: 0.75rem;
    }

    .stAlert {
        border-radius: 14px;
        backdrop-filter: blur(8px);
        border: 1px solid rgba(255, 255, 255, 0.08);
    }
</style>
""", unsafe_allow_html=True)

BACKEND_URL = "http://127.0.0.1:8000"

# --- HOOK LẤY DANH SÁCH LỊCH SỬ ---
def get_history():
    try:
        res = requests.get(f"{BACKEND_URL}/api/history", timeout=3)
        if res.status_code == 200:
            return res.json()
    except Exception:
        pass
    return []

# --- GIAO DIỆN CHÍNH ---
st.markdown("""
<div class="header-banner">
    <div class="header-title">📚 AI Study Assistant</div>
    <div class="header-subtitle">Trợ lý học tập thông minh — Tóm tắt bài giảng & Soạn câu hỏi Trắc nghiệm tự động</div>
</div>
""", unsafe_allow_html=True)

# Kiểm tra kết nối Backend
history = get_history()

try:
    requests.get(f"{BACKEND_URL}/", timeout=1)
except Exception:
    st.warning("⚠️ Chưa kết nối được với Server Backend (FastAPI). Hãy đảm bảo bạn đã chạy lệnh `uvicorn src.main:app --reload` ở một Terminal khác!")

# --- SIDEBAR: LỊCH SỬ TÀI LIỆU ---
st.sidebar.header("📁 Lịch sử tài liệu")
if history:
    for doc in history:
        doc_name = doc.get("filename", "Tài liệu không tên")
        doc_id = doc.get("document_id")
        if st.sidebar.button(f"📄 {doc_name}", key=f"doc_{doc_id}"):
            st.session_state.current_doc_id = doc_id
            st.rerun()
else:
    st.sidebar.write("Chưa có tài liệu nào trong lịch sử.")

# --- KHU VỰC UPLOAD FILE ---
st.subheader("📤 Tải lên bài giảng mới")
uploaded_file = st.file_uploader("Chọn file PDF hoặc TXT", type=["pdf", "txt"])

if uploaded_file is not None:
    if "last_uploaded" not in st.session_state or st.session_state.last_uploaded != uploaded_file.name:
        with st.spinner("Đang tải file lên server và đọc nội dung..."):
            try:
                files = {"file": (uploaded_file.name, uploaded_file.getvalue())}
                res = requests.post(f"{BACKEND_URL}/api/upload", files=files)
                if res.status_code == 200:
                    data = res.json()
                    st.session_state.current_doc_id = data["document_id"]
                    st.session_state.last_uploaded = uploaded_file.name
                    st.success(f"Đã tải lên thành công file: {uploaded_file.name}")
                    st.rerun()
                else:
                    st.error("Lỗi server khi upload file!")
            except Exception as e:
                st.error(f"Không thể kết nối Backend: {e}")

# --- KHU VỰC XỬ LÝ TÀI LIỆU ĐANG CHỌN ---
if "current_doc_id" in st.session_state and st.session_state.current_doc_id:
    doc_id = st.session_state.current_doc_id
    st.divider()
    st.info(f"📌 Đang chọn tài liệu ID: **{doc_id}**")

    col1, col2 = st.columns(2)

    # CỘT 1: TÓM TẮT BÀI GIẢNG
    with col1:
        st.subheader("📝 Tóm tắt bài giảng")
        if st.button("✨ Tạo tóm tắt mới bằng AI"):
            with st.spinner("Gemini đang viết tóm tắt..."):
                try:
                    res = requests.post(f"{BACKEND_URL}/api/documents/{doc_id}/summarize")
                    if res.status_code == 200:
                        st.session_state.summary_data = res.json().get("summary")
                    else:
                        try:
                            err_msg = res.json().get("detail", res.text)
                        except Exception:
                            err_msg = res.text
                        st.error(f"❌ Không thể tạo tóm tắt!\n\n**Chi tiết lỗi:** {err_msg}")
                except Exception as e:
                    st.error(f"Lỗi kết nối: {e}")

        if "summary_data" in st.session_state:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.markdown(st.session_state.summary_data)
            st.markdown('</div>', unsafe_allow_html=True)

    # CỘT 2: TRẮC NGHIỆM QUIZ (PHÂN BỐ ĐỒNG ĐỀU DẠNG GRID 2 CỘT)
    with col2:
        st.subheader("🧠 Thử thách Trắc nghiệm (Quiz)")
        if st.button("🎲 Tạo bộ câu hỏi mới"):
            with st.spinner("Gemini đang soạn câu hỏi..."):
                try:
                    res = requests.post(f"{BACKEND_URL}/api/documents/{doc_id}/quiz")
                    if res.status_code == 200:
                        st.session_state.quiz_data = res.json().get("quiz")
                    else:
                        st.error("Không thể tạo Quiz!")
                except Exception as e:
                    st.error(f"Lỗi kết nối: {e}")

        if "quiz_data" in st.session_state and isinstance(st.session_state.quiz_data, list):
            quiz_list = st.session_state.quiz_data
            
            # Phân bố các câu hỏi thành Lưới 2 cột (2-Column Grid) để giao diện cân đối, đều đặn
            for i in range(0, len(quiz_list), 2):
                q_cols = st.columns(2)
                
                # Câu hỏi cột 1
                with q_cols[0]:
                    q1 = quiz_list[i]
                    st.markdown(f"**❓ Câu {i + 1}: {q1.get('question')}**")
                    user_ans1 = st.radio("Chọn đáp án:", q1.get("options", []), key=f"q_{i}")
                    if st.button("Nộp bài", key=f"btn_{i}"):
                        if user_ans1 == q1.get("answer"):
                            st.success("🎉 Chính xác!")
                        else:
                            st.error(f"❌ Sai rồi! Đáp án: **{q1.get('answer')}**")
                
                # Câu hỏi cột 2 (nếu có)
                if i + 1 < len(quiz_list):
                    with q_cols[1]:
                        q2 = quiz_list[i + 1]
                        st.markdown(f"**❓ Câu {i + 2}: {q2.get('question')}**")
                        user_ans2 = st.radio("Chọn đáp án:", q2.get("options", []), key=f"q_{i+1}")
                        if st.button("Nộp bài", key=f"btn_{i+1}"):
                            if user_ans2 == q2.get("answer"):
                                st.success("🎉 Chính xác!")
                            else:
                                st.error(f"❌ Sai rồi! Đáp án: **{q2.get('answer')}**")
                
                st.write("") # Khoảng cách nhỏ giữa các hàng