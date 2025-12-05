from enum import Enum

from sqlalchemy import Boolean, Column, Enum as PgEnum, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.db.session import Base


class UserRole(str, Enum):
    ADMIN = "admin"
    STUDENT = "student"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    role = Column(PgEnum(UserRole, name="user_role"), default=UserRole.STUDENT, nullable=False)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=True)

    student = relationship("Student", back_populates="user", uselist=False)

