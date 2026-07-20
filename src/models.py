# models.py
from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from src.database import Base

class Document(Base):
    __tablename__ = "documents" # Tên bảng trong DB
    
    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, index=True, unique=True) # Tên file PDF/TXT
    content = Column(Text) # Chứa văn bản text gốc sau khi đọc từ PDF/TXT
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    # Mối quan hệ 1-Nhiều: 1 Document có thể có nhiều StudyNote
    notes = relationship("StudyNote", back_populates="document")

class StudyNote(Base):
    __tablename__ = "study_notes"
    
    id = Column(Integer, primary_key=True, index=True)
    document_id = Column(Integer, ForeignKey("documents.id"))
    note_type = Column(String) # Phân loại: 'summary' hoặc 'quiz'
    ai_response = Column(Text) # Chứa kết quả do Gemini trả về
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    document = relationship("Document", back_populates="notes")