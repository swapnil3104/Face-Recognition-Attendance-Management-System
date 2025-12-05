from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.db.session import Base


class Subject(Base):
    __tablename__ = "subjects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    code = Column(String(50), nullable=True)
    class_id = Column(Integer, ForeignKey("classes.id"), nullable=False)

    classroom = relationship("ClassRoom", back_populates="subjects")
    timetables = relationship("TimetableEntry", back_populates="subject")
    attendance_records = relationship("AttendanceRecord", back_populates="subject")

