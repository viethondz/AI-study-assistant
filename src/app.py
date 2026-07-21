import streamlit as st
import requests

# Cấu hình giao diện Streamlit
st.set_page_config(page_title="AI Study Assistant", page_icon="📚", layout="wide")

BACKEND_URL = "http://127.0.0.1:8000"

# --- HOOK LẤY DANH SÁCH LỊCH SỬ (BỌC BẪY LỖI CHỐNG ĐEN MÀN HÌNH) ---
def get_history():
    try:
        res = requests.get(f"{BACKEND_URL}/api/history", timeout=3)
        if res.status_code == 200:
            return res.json()
    except Exception:
        pass
    return []

# --- GIAO DIỆN CHÍNH ---
st.title("📚 AI Study Assistant")

# Kiểm tra kết nối Backend
history = get_history()

# BẢNG THÔNG BÁO NẾU CHƯA BẬT BACKEND
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

# --- KHU VỰC UPLOAD FILE (ĐÃ SỬA CHỐNG LẶP VO TẬN) ---
st.subheader("📤 Tải lên bài giảng mới")
uploaded_file = st.file_uploader("Chọn file PDF hoặc TXT", type=["pdf", "txt"])

if uploaded_file is not None:
    # Tránh gửi liên tục file đã upload
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
                        # Lấy chi tiết lỗi từ Backend để in ra màn hình
                        try:
                            err_msg = res.json().get("detail", res.text)
                        except Exception:
                            err_msg = res.text
                        st.error(f"❌ Không thể tạo tóm tắt!\n\n**Chi tiết lỗi:** {err_msg}")
                except Exception as e:
                    st.error(f"Lỗi kết nối: {e}")

        if "summary_data" in st.session_state:
            st.markdown(st.session_state.summary_data)

    # CỘT 2: TRẮC NGHIỆM QUIZ
    with col2:
        st.subheader("🧠 Thử thách Trắc nghiệm (Quiz)")
        if st.button("🎲 Tạo bộ 20 câu hỏi mới"):
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
            for idx, q in enumerate(st.session_state.quiz_data):
                st.write(f"**Câu {idx + 1}: {q.get('question')}**")
                user_ans = st.radio("Chọn đáp án:", q.get("options", []), key=f"q_{idx}")
                if st.button("Nộp bài", key=f"btn_{idx}"):
                    if user_ans == q.get("answer"):
                        st.success("🎉 Chính xác!")
                    else:
                        st.error(f"❌ Sai rồi! Đáp án đúng: {q.get('answer')}")