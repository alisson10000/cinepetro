from sqlalchemy.orm import Session
from passlib.hash import bcrypt
from . import models, schemas
from datetime import datetime

def get_by_email(db: Session, email: str):
    """Retorna o usuário ativo pelo email (se não foi deletado)."""
    return db.query(models.User).filter(
        models.User.email == email,
        models.User.deleted_at == None
    ).first()

def get_by_id(db: Session, user_id: int):
    """Retorna o usuário ativo pelo ID."""
    return db.query(models.User).filter(
        models.User.id == user_id,
        models.User.deleted_at == None
    ).first()

def get_all(db: Session):
    """Lista todos os usuários ativos."""
    return db.query(models.User).filter(
        models.User.deleted_at == None
    ).all()

def create(db: Session, user: schemas.UserCreate):
    """Cria um novo usuário com senha criptografada."""
    password_hash = bcrypt.hash(user.password)
    db_user = models.User(
        name=user.name,
        email=user.email,
        password_hash=password_hash  # ✅ Correto agora
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update(db: Session, user_id: int, data: schemas.UserUpdate):
    """Atualiza o nome e/ou senha de um usuário existente."""
    user = get_by_id(db, user_id)
    if not user:
        return None
    if data.name:
        user.name = data.name
    if data.password:
        user.password_hash = bcrypt.hash(data.password)  # ✅ Corrigido para o campo certo
    db.commit()
    db.refresh(user)
    return user

def delete(db: Session, user_id: int):
    """Marca o usuário como deletado (soft delete)."""
    user = get_by_id(db, user_id)
    if not user:
        return None
    user.deleted_at = datetime.utcnow()
    db.commit()
    return user
