from datetime import datetime
from pydantic import BaseModel

class AttendanceMarkRequest(BaseModel):
    student_id: int
    confidence: float

class AttendanceMarkResponse(BaseModel):
    status: str
    student_name: str
    class_name: str
    subject_name: str
    time_in: datetime
