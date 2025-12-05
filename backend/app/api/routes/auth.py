from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api import deps
from app.core.config import get_settings
from app.core.security import create_token, verify_password
from app.db.session import get_db
from app.models.user import User, UserRole
from app.schemas import auth as auth_schema


router = APIRouter(prefix="/auth", tags=["auth"])
settings = get_settings()


@router.post("/login", response_model=auth_schema.TokenResponse)
def login(data: auth_schema.LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == data.email).first()
    if not user or not verify_password(data.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    access_token = create_token(
        subject=user.id,
        expires_delta_minutes=settings.access_token_expire_minutes,
        token_type="access",
    )
    refresh_token = create_token(
        subject=user.id,
        expires_delta_minutes=settings.refresh_token_expire_minutes,
        token_type="refresh",
    )
    return auth_schema.TokenResponse(access_token=access_token, refresh_token=refresh_token)


@router.get("/me")
def read_me(current_user: User = Depends(deps.get_current_active_user)):
    return {"id": current_user.id, "email": current_user.email, "role": current_user.role}


@router.post("/bootstrap-admin", response_model=dict)
def bootstrap_admin(data: auth_schema.LoginRequest, db: Session = Depends(get_db)):
    """One-time helper to create the first admin user."""
    existing = db.query(User).filter(User.email == data.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Admin already exists")

    from app.core.security import get_password_hash

    admin = User(
        email=data.email,
        hashed_password=get_password_hash(data.password),
        role=UserRole.ADMIN,
    )
    db.add(admin)
    db.commit()
    db.refresh(admin)
    return {"id": admin.id, "email": admin.email}

