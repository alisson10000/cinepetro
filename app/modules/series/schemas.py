from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from fastapi import UploadFile

# 🔹 Base comum para criação e edição
class SeriesBase(BaseModel):
    title: str
    description: Optional[str] = None
    start_year: Optional[int] = None
    end_year: Optional[int] = None
    genre_ids: Optional[List[int]] = []

# 🔹 Para criação tradicional via JSON
class SeriesCreate(SeriesBase):
    poster: Optional[UploadFile] = None  # Para uso interno no service, caso venha via FormData

# 🔹 Para atualização parcial via JSON
class SeriesUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    start_year: Optional[int] = None
    end_year: Optional[int] = None
    genre_ids: Optional[List[int]] = None
    poster: Optional[str] = None  # Caminho já salvo (quando atualização tradicional)

# 🔹 Para resposta detalhada da API
class SeriesOut(SeriesBase):
    id: int
    poster: Optional[str] = None
    created_by: Optional[int] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True  # ✅ Converte de ORM para Pydantic
