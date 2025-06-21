from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from fastapi import UploadFile

# 🔹 Saída estruturada de um gênero (usado em SeriesOut)
class GenreOut(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True  # FastAPI >= 0.95

# 🔹 Base comum entre criação e edição de série
class SeriesBase(BaseModel):
    title: str
    description: Optional[str] = None
    start_year: Optional[int] = None
    end_year: Optional[int] = None
    genre_ids: Optional[List[int]] = []  # IDs para associar gêneros (input apenas)

# 🔹 Usado na criação de série (JSON ou FormData)
class SeriesCreate(SeriesBase):
    poster: Optional[UploadFile] = None  # Upload opcional via FormData

# 🔹 Usado na edição parcial da série (PUT/PATCH)
class SeriesUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    start_year: Optional[int] = None
    end_year: Optional[int] = None
    genre_ids: Optional[List[int]] = None  # ⚠️ Aqui mantemos como None por padrão
    poster: Optional[str] = None  # Aqui já é a string com o caminho salvo

# 🔹 Usado na resposta da API (GET / GET BY ID)
class SeriesOut(SeriesBase):
    id: int
    poster: Optional[str] = None               # Caminho do pôster renderizável
    genres: List[GenreOut] = []                # Lista completa dos gêneros marcados
    created_by: Optional[int] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
