from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

# 🔹 Base comum: usado para herança, não para retorno
class UserBase(BaseModel):
    name: str
    email: EmailStr

# 🔹 Criação de usuário
class UserCreate(UserBase):
    password: str
    is_admin: Optional[bool] = False  # caso você permita criar admin pelo sistema

# 🔹 Atualização parcial (sem obrigatoriedade)
class UserUpdate(BaseModel):
    name: Optional[str] = None
    password: Optional[str] = None
    is_admin: Optional[bool] = None  # útil em painéis admin

# 🔹 Resposta para o frontend (usuário autenticado ou consultado)
class UserOut(UserBase):
    id: int
    is_admin: bool
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime] = None

    class Config:
        from_attributes = True
