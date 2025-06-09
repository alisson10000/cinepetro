from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

# Base para criação e edição
class SeriesBase(BaseModel):
    title: str
    description: Optional[str] = None
    start_year: Optional[int] = None
    end_year: Optional[int] = None
    genre_ids: Optional[List[int]] = []  # Permitir ausência e default

# Para criação
class SeriesCreate(SeriesBase):
    pass

# Para atualização parcial
class SeriesUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    start_year: Optional[int] = None
    end_year: Optional[int] = None
    genre_ids: Optional[List[int]] = None

# Para resposta
class SeriesOut(SeriesBase):
    id: int
    created_by: Optional[int] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
