from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

# Base comum para criação e atualização
class GenreBase(BaseModel):
    name: str

# Schema para criação de um único gênero
class GenreCreate(GenreBase):
    pass

# Schema para atualização de gênero
class GenreUpdate(GenreBase):
    pass

# Schema de saída com metadados
class GenreOut(GenreBase):
    id: int
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime] = None

    class Config:
        from_attributes = True  # necessário para conversão ORM -> Pydantic

# Schema para criação em lote de múltiplos gêneros
class GenreCreateBatch(BaseModel):
    genres: List[GenreCreate]
