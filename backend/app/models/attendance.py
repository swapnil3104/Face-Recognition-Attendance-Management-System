from datetime import datetime, date

from sqlalchemy import Column, Date, DateTime, ForeignKey, Integer, Numeric, String
from sqlalchemy.orm import relationship

from app.db.session import Base


class AttendanceRecord(Base):
    __tablename__ = "attendance_records"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    class_id = Column(Integer, ForeignKey("classes.id"), nullable=False)
    subject_id = Column(Integer, ForeignKey("subjects.id"), nullable=False)
    timetable_entry_id = Column(Integer, ForeignKey("timetable_entries.id"), nullable=True)
    date = Column(Date, default=date.today, nullable=False)
    time_in = Column(DateTime, default=datetime.utcnow, nullable=False)
    status = Column(String(50), default="present", nullable=False)
    confidence = Column(Numeric(5, 2), nullable=True)
    source = Column(String(50), default="auto")

    student = relationship("Student", back_populates="attendance_records")
    subject = relationship("Subject", back_populates="attendance_records")
    timetable_entry = relationship("TimetableEntry", back_populates="attendance_records")

