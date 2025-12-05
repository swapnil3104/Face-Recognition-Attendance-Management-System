from __future__ import annotations

import base64
import io
from pathlib import Path
from typing import List, Sequence

import face_recognition
import numpy as np


class FaceRecognizer:
    """
    Thin wrapper around face_recognition to encode and compare faces.
    Stores embeddings in-memory; hook up to DB/cache later.
    """

    def __init__(self) -> None:
        self.known_encodings: list[np.ndarray] = []
        self.known_student_ids: list[int] = []

    def load_embeddings(self, embeddings: Sequence[tuple[int, Sequence[float]]]) -> None:
        self.known_encodings = [np.array(vector) for _, vector in embeddings]
        self.known_student_ids = [student_id for student_id, _ in embeddings]

    def add_embedding(self, student_id: int, encoding: Sequence[float]) -> None:
        self.known_encodings.append(np.array(encoding))
        self.known_student_ids.append(student_id)

    def encode_images(self, image_paths: List[Path]) -> List[np.ndarray]:
        encodings: list[np.ndarray] = []
        for path in image_paths:
            image = face_recognition.load_image_file(path)
            face_encodings = face_recognition.face_encodings(image)
            if not face_encodings:
                raise ValueError(f"No face found in image {path}")
            encodings.append(face_encodings[0])
        return encodings

    def encode_base64_image(self, image_data: str) -> List[np.ndarray]:
        raw = base64.b64decode(image_data)
        image = face_recognition.load_image_file(io.BytesIO(raw))
        return face_recognition.face_encodings(image)

    def recognize(self, encoding: np.ndarray, tolerance: float = 0.45) -> tuple[int, float] | None:
        if not self.known_encodings:
            return None
        distances = face_recognition.face_distance(self.known_encodings, encoding)
        best_match_index = int(np.argmin(distances))
        if distances[best_match_index] <= tolerance:
            confidence = max(0.0, 1.0 - distances[best_match_index])
            return self.known_student_ids[best_match_index], float(confidence)
        return None

