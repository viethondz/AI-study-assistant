# src/main.py
from fastapi import FastAPI, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
import json

# CHÚ Ý: Cập nhật các đường dẫn import theo cấu trúc thư mục src/
from src import models
from src import services
from src.database import engine, get_db

# Tự động tạo bảng trong Database
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="AI Study Assistant API")

@app.get("/")
def read_root():
    return {"message": "Server đang chạy! Sẵn sàng upload file và tóm tắt."}

# 1. API UPLOAD FILE
@app.post("/api/upload")
async def upload_document(file: UploadFile = File(...), db: Session = Depends(get_db)):
    extracted_text = services.extract_text_from_file(file)
    db_document = models.Document(filename=file.filename, content=extracted_text)
    db.add(db_document)
    db.commit()
    db.refresh(db_document)
    return {
        "message": "Upload thành công!",
        "document_id": db_document.id,
        "filename": db_document.filename,
        "char_count": len(str(extracted_text or ""))
    }

# 2. API TÓM TẮT TÀI LIỆU
@app.post("/api/documents/{doc_id}/summarize")
def summarize_document(doc_id: int, db: Session = Depends(get_db)):
    document = db.query(models.Document).filter(models.Document.id == doc_id).first()
    if not document:
        raise HTTPException(status_code=404, detail="Không tìm thấy tài liệu với ID này.")
    
    try:
        summary_result = services.call_gemini_to_summarize(str(document.content or ""))
    except Exception as e:
        # 🟢 ÉP TERMINAL IN FULL TRACEBACK
        import traceback
        print("\n🔴🔴🔴 LỖI CHI TIẾT TỪ GEMINI TẠI SUMMARIZE:")
        traceback.print_exc()
        print("🔴🔴🔴\n")
        raise HTTPException(status_code=500, detail=f"Lỗi khi gọi AI Gemini: {str(e)}")

    db_note = models.StudyNote(document_id=document.id, note_type="summary", ai_response=summary_result)
    db.add(db_note)
    db.commit()
    return {"document_id": document.id, "filename": document.filename, "summary": summary_result}

# 3. API TẠO CÂU HỎI TRẮC NGHIỆM (QUIZ)
@app.post("/api/documents/{doc_id}/quiz")
def generate_quiz_document(doc_id: int, db: Session = Depends(get_db)):
    document = db.query(models.Document).filter(models.Document.id == doc_id).first()
    if not document:
        raise HTTPException(status_code=404, detail="Không tìm thấy tài liệu với ID này.")
    
    try:
        quiz_list = services.call_gemini_to_generate_quiz(str(document.content or ""))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Lỗi khi gọi AI Gemini: {str(e)}")

    db_note = models.StudyNote(
        document_id=document.id, 
        note_type="quiz", 
        ai_response=json.dumps(quiz_list, ensure_ascii=False)
    )
    db.add(db_note)
    db.commit()
    return {"document_id": document.id, "filename": document.filename, "quiz": quiz_list}

# 4. API LẤY DANH SÁCH LỊCH SỬ
@app.get("/api/history")
def get_study_history(db: Session = Depends(get_db)):
    documents = db.query(models.Document).order_by(models.Document.created_at.desc()).all()
    history_list = []
    for doc in documents:
        history_list.append({
            "document_id": doc.id,
            "filename": doc.filename,
            "created_at": doc.created_at,
            "char_count": len(str(doc.content or ""))
        })
    return history_list

# 5. API XEM CHI TIẾT LỊCH SỬ 1 TÀI LIỆU
@app.get("/api/history/{doc_id}")
def get_history_detail(doc_id: int, db: Session = Depends(get_db)):
    document = db.query(models.Document).filter(models.Document.id == doc_id).first()
    if not document:
        raise HTTPException(status_code=404, detail="Không tìm thấy tài liệu này trong lịch sử.")
    
    processed_notes = []
    for note in document.notes:
        note_content = note.ai_response
        if note.note_type == "quiz":
            try:
                note_content = json.loads(note.ai_response)
            except Exception:
                pass
        processed_notes.append({
            "note_id": note.id,
            "note_type": note.note_type,
            "result": note_content,
            "created_at": note.created_at
        })
        
    return {
        "document_id": document.id,
        "filename": document.filename,
        "content_raw": document.content,
        "created_at": document.created_at,
        "saved_notes": processed_notes
    }