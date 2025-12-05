from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.db.session import Base


class ClassRoom(Base):
    __tablename__ = "classes"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    department = Column(String(255), nullable=True)
    year = Column(String(50), nullable=True)
    division = Column(String(50), nullable=True)

    subjects = relationship("Subject", back_populates="classroom")
    timetables = relationship("TimetableEntry", back_populates="classroom")

