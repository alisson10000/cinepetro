from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from fastapi import UploadFile

# 🔁 Importa os gêneros para detalhar no MovieOut
from app.modules.genres.schemas import GenreOut  # ajuste o path se necessário

# 🔹 Base comum para criação, atualização e leitura
class MovieBase(BaseModel):
    title: str                                 # 🎬 Título do filme
    description: Optional[str] = None          # 📝 Descrição opcional
    year: Optional[int] = None                 # 📅 Ano de lançamento
    duration: Optional[int] = None             # ⏱️ Duração em minutos
    genre_ids: Optional[List[int]] = []        # 🎭 IDs dos gêneros (relacionamento)

# 🔸 Modelo para criação de filme com possível upload de pôster
class MovieCreate(MovieBase):
    poster: Optional[UploadFile] = None        # 🖼️ Upload opcional do pôster

# 🔸 Modelo para atualização via JSON (sem upload direto)
class MovieUpdate(MovieBase):
    poster: Optional[str] = None               # ✏️ Caminho do pôster (string)

# 🔸 Modelo de saída da API (resposta)
class MovieOut(MovieBase):
    id: int                                    # 🆔 ID único do filme
    poster: Optional[str] = None               # 📷 Caminho ou URL do pôster
    genres: List[GenreOut] = []                # 🎭 Detalhamento dos gêneros
    created_at: datetime                       # 🕒 Criado em
    updated_at: datetime                       # 🕒 Atualizado em
    deleted_at: Optional[datetime] = None      # 🗑️ Deletado em (soft delete)

    class Config:
        from_attributes = True                 # ✅ Converte de ORM para Pydantic automaticamente
