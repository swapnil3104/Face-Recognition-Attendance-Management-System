from sqlalchemy import Column, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from app.db.session import Base


class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(String(50), unique=True, nullable=False, index=True)
    full_name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False, index=True)
    phone = Column(String(50), nullable=True)
    department = Column(String(255), nullable=True)
    class_name = Column(String(255), nullable=True)
    year = Column(String(50), nullable=True)
    division = Column(String(50), nullable=True)
    roll_number = Column(String(50), nullable=True)
    notes = Column(Text, nullable=True)

    user = relationship("User", back_populates="student", uselist=False)
    images = relationship("StudentImage", back_populates="student", cascade="all, delete-orphan")
    embeddings = relationship("FaceEmbedding", back_populates="student", cascade="all, delete-orphan")
    attendance_records = relationship("AttendanceRecord", back_populates="student")


class StudentImage(Base):
    __tablename__ = "student_images"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id", ondelete="CASCADE"), nullable=False)
    file_path = Column(String(500), nullable=False)

    student = relationship("Student", back_populates="images")
    embeddings = relationship("FaceEmbedding", back_populates="image")


class FaceEmbedding(Base):
    __tablename__ = "face_embeddings"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id", ondelete="CASCADE"), nullable=False)
    image_id = Column(Integer, ForeignKey("student_images.id", ondelete="SET NULL"), nullable=True)
    encoding = Column(Text, nullable=False)  # store as JSON string
    model_version = Column(String(50), default="v1")

    student = relationship("Student", back_populates="embeddings")
    image = relationship("StudentImage", back_populates="embeddings")

