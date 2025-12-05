from pathlib import Path
from typing import List

from fastapi import APIRouter, Depends, File, Form, UploadFile, status, HTTPException

from app.services.recognizer import FaceRecognizer


router = APIRouter()


def get_recognizer() -> FaceRecognizer:
    # In production we would use dependency injection / singletons.
    # For now a module-level instance is fine.
    from app.main import recognizer

    return recognizer


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register_student(
    student_id: int = Form(...),
    files: List[UploadFile] = File(...),
    recognizer: FaceRecognizer = Depends(get_recognizer),
):
    temp_paths: list[Path] = []
    try:
        for file in files:
            tmp_path = Path(f"/tmp/{student_id}_{file.filename}")
            tmp_path.write_bytes(await file.read())
            temp_paths.append(tmp_path)
        encodings = recognizer.encode_images(temp_paths)
        for encoding in encodings:
            recognizer.add_embedding(student_id, encoding)
        return {"student_id": student_id, "embeddings": len(encodings)}
    finally:
        for path in temp_paths:
            if path.exists():
                path.unlink(missing_ok=True)


@router.post("/recognize")
async def recognize_face(
    file: UploadFile = File(...),
    recognizer: FaceRecognizer = Depends(get_recognizer),
):
    temp_path = Path(f"/tmp/recognize_{file.filename}")
    try:
        temp_path.write_bytes(await file.read())
        encodings = recognizer.encode_images([temp_path])
        matches = []
        for encoding in encodings:
            match = recognizer.recognize(encoding)
            if match:
                student_id, confidence = match
                matches.append({"student_id": student_id, "confidence": confidence})
        if not matches:
            raise HTTPException(status_code=404, detail="No match")
        return {"matches": matches}
    finally:
        if temp_path.exists():
            temp_path.unlink(missing_ok=True)

