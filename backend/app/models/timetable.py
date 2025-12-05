from sqlalchemy import Column, ForeignKey, Integer, String, Time
from sqlalchemy.orm import relationship

from app.db.session import Base


class TimetableEntry(Base):
    __tablename__ = "timetable_entries"

    id = Column(Integer, primary_key=True, index=True)
    class_id = Column(Integer, ForeignKey("classes.id"), nullable=False)
    subject_id = Column(Integer, ForeignKey("subjects.id"), nullable=False)
    day_of_week = Column(String(9), nullable=False)
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)
    teacher_name = Column(String(255), nullable=True)

    classroom = relationship("ClassRoom", back_populates="timetables")
    subject = relationship("Subject", back_populates="timetables")
    attendance_records = relationship("AttendanceRecord", back_populates="timetable_entry")

