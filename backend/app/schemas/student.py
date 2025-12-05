from typing import List, Optional

from pydantic import BaseModel, EmailStr


class StudentBase(BaseModel):
    student_id: str
    full_name: str
    email: EmailStr
    phone: Optional[str] = None
    department: Optional[str] = None
    class_name: Optional[str] = None
    year: Optional[str] = None
    division: Optional[str] = None
    roll_number: Optional[str] = None


class StudentCreate(StudentBase):
    pass


class StudentUpdate(BaseModel):
    full_name: Optional[str] = None
    phone: Optional[str] = None
    department: Optional[str] = None
    class_name: Optional[str] = None
    year: Optional[str] = None
    division: Optional[str] = None
    roll_number: Optional[str] = None


class StudentImageResponse(BaseModel):
    id: int
    file_path: str

    class Config:
        from_attributes = True


class StudentResponse(StudentBase):
    id: int
    images: List[StudentImageResponse] = []

    class Config:
        from_attributes = True

