from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# Schema base
class WatchProgressBase(BaseModel):
    time_seconds: float

    class Config:
        from_attributes = True  # ✅ Substitui orm_mode no Pydantic v2

# Para criação de um novo progresso
class WatchProgressCreate(WatchProgressBase):
   
    movie_id: Optional[int] = None
    episode_id: Optional[int] = None

# Para atualização (salvar novo tempo)
class WatchProgressUpdate(BaseModel):
    time_seconds: float

# ✅ Schema completo de resposta
class WatchProgressOut(WatchProgressBase):
    id: int
    user_id: int
    movie_id: Optional[int]
    episode_id: Optional[int]
    updated_at: datetime
