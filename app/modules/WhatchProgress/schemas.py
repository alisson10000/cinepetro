from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# 📦 Schema base de progresso
class WatchProgressBase(BaseModel):
    time_seconds: float

    class Config:
        from_attributes = True  # ✅ Compatível com Pydantic v2

# ➕ Para criação de um novo progresso
class WatchProgressCreate(WatchProgressBase):
    movie_id: Optional[int] = None
    episode_id: Optional[int] = None

# 🔄 Para atualização de progresso existente
class WatchProgressUpdate(BaseModel):
    time_seconds: float

# ✅ Schema completo usado como resposta em save/get
class WatchProgressOut(WatchProgressBase):
    id: int
    user_id: int
    movie_id: Optional[int]
    episode_id: Optional[int]
    updated_at: datetime

    class Config:
        from_attributes = True

# 🆕 Schema para /progress/continuar (resumo de filmes)
class MovieProgressOut(BaseModel):
    movie_id: int
    title: str
    poster: str   # ✅ Adicionado
    time_seconds: float
    duration_seconds: float

    class Config:
        from_attributes = True
