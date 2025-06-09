from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr

from app.modules.user import models as user_models
from app.modules.core.database import get_db
from app.modules.core.security import verify_password, create_access_token

router = APIRouter(prefix="/auth", tags=["auth"])

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

@router.post("/login")
def login(data: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(user_models.User).filter(
        user_models.User.email == data.email,
        user_models.User.deleted_at == None
    ).first()

    if not user or not verify_password(data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Credenciais inválidas")

    # Gerar token JWT
    token = create_access_token(data={
        "sub": str(user.id),
        "email": user.email,
        "is_admin": user.is_admin
    })

    return {
        "access_token": token,
        "token_type": "bearer",
        "user_id": user.id,
        "is_admin": user.is_admin
    }
