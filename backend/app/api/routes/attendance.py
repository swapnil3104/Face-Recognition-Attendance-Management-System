from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import and_

from app.api import deps
from app.db.session import get_db
from app.models.student import Student
from app.models.classroom import ClassRoom
from app.models.timetable import TimetableEntry
from app.models.attendance import AttendanceRecord
from app.schemas.attendance import AttendanceMarkRequest, AttendanceMarkResponse

router = APIRouter(prefix="/attendance", tags=["attendance"])

@router.post("/mark", response_model=AttendanceMarkResponse)
def mark_attendance(
    data: AttendanceMarkRequest,
    db: Session = Depends(get_db),
):
    # 1. Get Student
    student = db.get(Student, data.student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    # 2. Find ClassRoom
    # Assuming class_name maps to ClassRoom.name
    classroom = db.query(ClassRoom).filter(
        ClassRoom.name == student.class_name
    ).first()
    
    if not classroom:
        # If no classroom found, we can't find a timetable.
        # However, for demo purposes, if we can't find a class, we might just log it without a subject/timetable
        # But the user asked to link to Timetable.
        raise HTTPException(status_code=404, detail=f"Classroom '{student.class_name}' not found")

    # 3. Find Active Timetable Entry
    now = datetime.now()
    current_day = now.strftime("%A") # e.g., "Monday"
    current_time = now.time()

    entry = db.query(TimetableEntry).filter(
        TimetableEntry.class_id == classroom.id,
        TimetableEntry.day_of_week == current_day,
        TimetableEntry.start_time <= current_time,
        TimetableEntry.end_time >= current_time
    ).first()

    if not entry:
        raise HTTPException(status_code=404, detail="No active class found for this student at this time")

    # 4. Check if already marked
    existing = db.query(AttendanceRecord).filter(
        AttendanceRecord.student_id == student.id,
        AttendanceRecord.timetable_entry_id == entry.id,
        AttendanceRecord.date == now.date()
    ).first()

    if existing:
        return AttendanceMarkResponse(
            status="already_marked",
            student_name=student.full_name,
            class_name=classroom.name,
            subject_name=entry.subject.name,
            time_in=existing.time_in
        )

    # 5. Create Record
    record = AttendanceRecord(
        student_id=student.id,
        class_id=classroom.id,
        subject_id=entry.subject_id,
        timetable_entry_id=entry.id,
        date=now.date(),
        time_in=now,
        status="present",
        confidence=data.confidence,
        source="camera"
    )
    db.add(record)
    db.commit()
    db.refresh(record)

    return AttendanceMarkResponse(
        status="marked",
        student_name=student.full_name,
        class_name=classroom.name,
        subject_name=entry.subject.name,
        time_in=record.time_in
    )
