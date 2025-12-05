from fastapi import APIRouter

from app.api.routes import auth, students, attendance


api_router = APIRouter()
api_router.include_router(auth.router)
api_router.include_router(students.router)
api_router.include_router(attendance.router)

