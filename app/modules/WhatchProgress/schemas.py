from pydantic import BaseModel
from typing import Optional, Union, Literal
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


# 🆕 Schema para exibição de filmes em /progress/continuar
class MovieProgressOut(BaseModel):
    type: Literal["movie"] = "movie"  # ✅ Para identificar no frontend
    movie_id: int
    title: str
    poster: str
    time_seconds: float
    duration_seconds: float

    class Config:
        from_attributes = True


# 🆕 Schema para exibição de episódios de séries em /progress/continuar
class EpisodeProgressOut(BaseModel):
    type: Literal["series"] = "series"  # ✅ Para identificar no frontend
    episode_id: int
    series_id: int
    series_title: str
    episode_number: int
    season_number: int
    title: str
    poster: str
    time_seconds: float
    duration_seconds: float

    class Config:
        from_attributes = True


# ✅ Schema unificado para retorno misto (filmes + episódios)
GenericProgressOut = Union[MovieProgressOut, EpisodeProgressOut]
