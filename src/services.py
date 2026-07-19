# services.py
import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
import json

# Tải cấu hình từ file .env
load_dotenv()

# KHỞI TẠO CLIENT MỚI THEO CHUẨN GOOGLE GENAI
# Nó sẽ tự động tìm biến GEMINI_API_KEY hoặc GOOGLE_API_KEY trong file .env của bạn
api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
client = genai.Client(api_key=api_key)

# 1. HÀM ĐỌC FILE (Giữ nguyên logic cũ của bạn)
def extract_text_from_file(file):
    try:
        import pypdf
        reader = pypdf.PdfReader(file.file)
        text = ""
        for page in reader.pages:
            text += page.extract_text() or ""
        return text
    except Exception:
        file.file.seek(0)
        return file.file.read().decode("utf-8", errors="ignore")

# 2. HÀM GỌI GEMINI ĐỂ TÓM TẮT (CÚ PHÁP MỚI)
def call_gemini_to_summarize(text_content: str) -> str:
    if not text_content.strip():
        return "Tài liệu trống, không có nội dung để tóm tắt."
    
    prompt = f"Hãy tóm tắt ngắn gọn, súc tích và rõ ràng nội dung sau đây bằng Tiếng Việt:\n\n{text_content}"
    
    # Chuẩn gọi model mới: client.models.generate_content
    response = client.models.generate_content(
        model='gemini-2.0-flash',
        contents=prompt,
    )
    return response.text or "Không thể lấy nội dung tóm tắt."

# 3. HÀM GỌI GEMINI ĐỂ TẠO QUIZ (CÚ PHÁP MỚI + ÉP RA JSON SẠCH)
def call_gemini_to_generate_quiz(text_content: str) -> list:
    if not text_content.strip():
        return []
        
    prompt = (
        "Dựa vào nội dung sau, hãy tạo ra 5 câu hỏi trắc nghiệm bằng Tiếng Việt. "
        "Trả về kết quả dưới dạng một mảng JSON duy nhất, không kèm theo bất kỳ chữ giải thích nào khác ngoài JSON.\n"
        "Cấu trúc JSON:\n"
        "[\n"
        "  {\n"
        "    \"question\": \"Câu hỏi?\",\n"
        "    \"options\": [\"Đáp án A\", \"Đáp án B\", \"Đáp án C\", \"Đáp án D\"],\n"
        "    \"answer\": \"Đáp án đúng (phải khớp chính xác với 1 trong 4 lựa chọn ở trên)\"\n"
        "  }\n"
        "]"
    )
    
    # FIX 1: Gộp prompt và text_content thành 1 chuỗi str duy nhất để Pyrefly không bắt bẻ
    full_content = f"{prompt}\n\n{text_content}"
    
    response = client.models.generate_content(
        model='gemini-2.0-flash',
        contents=full_content,
        config=types.GenerateContentConfig(
            response_mime_type="application/json"
        )
    )
    
    try:
        # FIX 2: Ép kiểu str( ... or "[]") để đảm bảo không bao giờ bị None, vừa lòng json.loads
        ai_reply = str(response.text or "[]")
        return json.loads(ai_reply)
    except Exception:
        return [{"question": "Lỗi cấu trúc dữ liệu Quiz từ AI", "options": ["", "", "", ""], "answer": ""}]