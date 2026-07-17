# database.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Dùng SQLite cho giai đoạn phát triển (tạo ra một file tên là study_assistant.db trong thư mục)
SQLALCHEMY_DATABASE_URL = "sqlite:///./study_assistant.db"

# Nếu sau này bạn dùng PostgreSQL, chỉ cần đổi dòng URL trên thành:
# SQLALCHEMY_DATABASE_URL = "postgresql://username:password@localhost/dbname"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    # check_same_thread chỉ bắt buộc đối với SQLite, do cái này nó chỉ cho phép một thread truy cập vào DB, nhưng FastAPI có thể tạo ra nhiều thread để xử lý các Request cùng lúc, nên cần phải tắt check_same_thread đi.
    connect_args={"check_same_thread": False} 
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)# tao ra một class SessionLocal để tạo ra các session kết nối tới DB, mỗi session sẽ được tạo ra cho mỗi Request gửi tới API.

Base = declarative_base()

# Hàm này sẽ được gọi mỗi khi có một Request gửi tới API để lấy kết nối DB
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()