from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from . import schemas, services
from app.modules.core.database import get_db
from app.modules.core.dependencies import get_current_user  # ✅ Reutiliza sua lógica de auth

router = APIRouter(prefix="/users", tags=["Users"])

# 🔒 Rota protegida: retorna o usuário autenticado (para saber se é admin ou não)
@router.get("/me", response_model=schemas.UserOut)
def get_current_authenticated_user(current_user: schemas.UserOut = Depends(get_current_user)):
    return current_user

# 📋 Listar todos os usuários ativos (apenas para fins administrativos)
@router.get("/", response_model=list[schemas.UserOut])
def list_users(db: Session = Depends(get_db)):
    return services.get_all(db)

# 🔍 Obter usuário por ID
@router.get("/{user_id}", response_model=schemas.UserOut)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = services.get_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# ➕ Criar novo usuário
@router.post("/", response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    if services.get_by_email(db, user.email):
        raise HTTPException(status_code=400, detail="Email already registered")
    return services.create(db, user)

# ✏️ Atualizar usuário
@router.put("/{user_id}", response_model=schemas.UserOut)
def update_user(user_id: int, data: schemas.UserUpdate, db: Session = Depends(get_db)):
    updated = services.update(db, user_id, data)
    if not updated:
        raise HTTPException(status_code=404, detail="User not found")
    return updated

# ❌ Soft delete
@router.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    deleted = services.delete(db, user_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="User not found")
    return {"detail": "User deleted"}
