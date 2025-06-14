import logging
import json
from typing import List

from fastapi import (
    APIRouter, Depends, UploadFile, File, Form, HTTPException
)
from sqlalchemy.orm import Session

from app.modules.core.database import get_db
from app.modules.core.dependencies import get_current_user
from app.modules.user.models import User
from . import schemas, services

# 🎬 Logger principal
logger = logging.getLogger("cinepetro.movies")

# 📍 Roteador
router = APIRouter(prefix="/movies", tags=["Movies"])

# 📋 Listar todos os filmes (não deletados)
@router.get("/", response_model=List[schemas.MovieOut])
def list_movies(db: Session = Depends(get_db)):
    logger.info("📋 Listando todos os filmes disponíveis")
    return services.get_all(db)

# 🔍 Obter um filme específico
@router.get("/{movie_id}", response_model=schemas.MovieOut)
def get_movie(
    movie_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    logger.info(f"🔍 Buscando detalhes do filme ID={movie_id}")
    movie = services.get_by_id(db, movie_id)
    if not movie:
        logger.warning(f"❌ Filme ID={movie_id} não encontrado")
        raise HTTPException(status_code=404, detail="Filme não encontrado")
    return movie

# 🆕 Criar novo filme via JSON puro
@router.post("/", response_model=schemas.MovieOut)
def create_movie(
    movie: schemas.MovieCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    logger.info(f"📥 Criando filme via JSON: {movie.title}")
    return services.create(db, movie, user_id=current_user.id)

# 🖼️ Criar filme com pôster (FormData)
@router.post("/upload", response_model=schemas.MovieOut)
async def create_movie_with_upload(
    title: str = Form(...),
    description: str = Form(...),
    year: int = Form(...),
    duration: int = Form(...),
    genre_ids: str = Form(...),
    poster: UploadFile = File(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    logger.info("🖼️ Criando novo filme com pôster via FormData")
    try:
        genre_ids_list = json.loads(genre_ids)
        if not isinstance(genre_ids_list, list):
            raise ValueError()
    except Exception as e:
        logger.error(f"❌ Erro ao interpretar 'genre_ids': {genre_ids} | {e}")
        raise HTTPException(status_code=400, detail="Campo 'genre_ids' deve ser uma lista JSON válida")

    movie_data = schemas.MovieCreate(
        title=title,
        description=description,
        year=year,
        duration=duration,
        genre_ids=genre_ids_list,
        poster=poster
    )
    return services.create(db, movie_data, user_id=current_user.id)

# ✏️ Atualizar via JSON puro
@router.put("/{movie_id}", response_model=schemas.MovieOut)
def update_movie(
    movie_id: int,
    movie: schemas.MovieUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    logger.info(f"✏️ Atualizando filme via JSON: ID={movie_id}")
    updated = services.update(db, movie_id, movie)
    if not updated:
        logger.warning(f"❌ Filme ID={movie_id} não encontrado para atualização")
        raise HTTPException(status_code=404, detail="Filme não encontrado")
    return updated

# ✏️ Atualizar com pôster via FormData
@router.put("/upload/{movie_id}", response_model=schemas.MovieOut)
async def update_movie_with_upload(
    movie_id: int,
    title: str = Form(...),
    description: str = Form(...),
    year: int = Form(...),
    duration: int = Form(...),
    genre_ids: str = Form(...),
    poster: UploadFile = File(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    logger.info(f"🖊️ Atualizando filme com upload: ID={movie_id}")
    try:
        genre_ids_list = json.loads(genre_ids)
        if not isinstance(genre_ids_list, list):
            raise ValueError()
    except Exception as e:
        logger.error(f"❌ Erro ao interpretar 'genre_ids': {genre_ids} | {e}")
        raise HTTPException(status_code=400, detail="Campo 'genre_ids' deve ser uma lista JSON válida")

    movie_data = schemas.MovieCreate(
        title=title,
        description=description,
        year=year,
        duration=duration,
        genre_ids=genre_ids_list,
        poster=poster
    )
    updated = services.update_with_upload(db, movie_id, movie_data)
    if not updated:
        logger.warning(f"❌ Filme ID={movie_id} não encontrado para atualização com upload")
        raise HTTPException(status_code=404, detail="Filme não encontrado")
    return updated

# 🗑️ Exclusão lógica (soft delete + remoção do pôster físico)
@router.delete("/{movie_id}")
def delete_movie(
    movie_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    logger.info(f"🗑️ Solicitando exclusão lógica do filme ID={movie_id}")
    result = services.delete(db, movie_id)
    if not result:
        logger.warning(f"❌ Filme ID={movie_id} não encontrado para exclusão")
        raise HTTPException(status_code=404, detail="Filme não encontrado para exclusão")
    return {"detail": "Filme excluído com sucesso"}

# 💀 Exclusão definitiva do banco (hard delete)
@router.delete("/{movie_id}/hard")
def hard_delete_movie(
    movie_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    logger.info(f"💀 Solicitando exclusão definitiva do filme ID={movie_id}")
    deleted = services.hard_delete(db, movie_id)
    if not deleted:
        logger.warning(f"❌ Filme ID={movie_id} não encontrado para exclusão definitiva")
        raise HTTPException(status_code=404, detail="Filme não encontrado para exclusão definitiva")
    return {"detail": "Filme removido permanentemente"}
