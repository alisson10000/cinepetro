from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr

from app.modules.user import models as user_models
from app.modules.core.database import get_db
from app.modules.core.security import verify_password, create_access_token
from app.modules.core.logger import logger  # ⬅️ Importa o logger

router = APIRouter(prefix="/auth", tags=["auth"])


# 📥 Modelo da requisição
class LoginRequest(BaseModel):
    email: EmailStr
    password: str


# 📤 Modelo da resposta (opcional, mas recomendado)
class LoginResponse(BaseModel):
    access_token: str
    token_type: str
    user_id: int
    is_admin: bool
    name: str
    email: str


@router.post("/login", response_model=LoginResponse)
def login(data: LoginRequest, db: Session = Depends(get_db)):
    logger.info(f"🛎️ [LOGIN] Tentativa de login recebida | email={data.email}")  # ⬅️ Registro da tentativa

    # 🔍 Buscar usuário no banco
    user = db.query(user_models.User).filter(
        user_models.User.email == data.email,
        user_models.User.deleted_at == None
    ).first()

    # ❌ Verificação de credenciais
    if not user or not verify_password(data.password, user.password_hash):
        logger.warning(f"❌ [LOGIN] Falha no login | email={data.email}")  # ⬅️ Falha de login
        raise HTTPException(status_code=401, detail="Credenciais inválidas")

    # 🔐 Gerar token JWT
    token = create_access_token(data={
        "sub": str(user.id),
        "email": user.email,
        "is_admin": user.is_admin
    })

    logger.info(f"✅ [LOGIN] Login bem-sucedido | user_id={user.id} | email={user.email}")  # ⬅️ Sucesso

    # ✅ Retornar todos os dados necessários
    return {
        "access_token": token,
        "token_type": "bearer",
        "user_id": user.id,
        "is_admin": user.is_admin,
        "name": user.name,
        "email": user.email
    }
