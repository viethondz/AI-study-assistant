# main.py
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
import models
from database import engine, get_db

# Lệnh này yêu cầu SQLAlchemy tạo các bảng trong DB ngay khi app khởi động
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="AI Study Assistant API")

# Endpoint gốc để kiểm tra xem server có chạy không
@app.get("/")
def read_root():
    return {"message": "Server đang chạy! Chào mừng đến với AI Study Assistant."}

# Endpoint test kết nối Database
@app.get("/test-db")
def test_db(db: Session = Depends(get_db)):
    return {"status": "Kết nối Database thành công! Đã sẵn sàng lưu dữ liệu."}