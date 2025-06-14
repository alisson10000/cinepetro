import logging
import json
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import List

from . import schemas, services
from app.modules.core.database import get_db
from app.modules.core.dependencies import get_current_user
from app.modules.user.models import User

logger = logging.getLogger("cinepetro.series")

router = APIRouter(prefix="/series", tags=["Series"])

# 📋 Listar todas as séries não deletadas
@router.get("/", response_model=List[schemas.SeriesOut])
def list_series(db: Session = Depends(get_db)):
    logger.info("📋 Listando todas as séries disponíveis")
    return services.get_all(db)

# 🔍 Buscar série por ID
@router.get("/{series_id}", response_model=schemas.SeriesOut)
def get_series(series_id: int, db: Session = Depends(get_db)):
    logger.info(f"🔍 Buscando detalhes da série ID={series_id}")
    series = services.get_by_id(db, series_id)
    if not series:
        logger.warning(f"❌ Série não encontrada ID={series_id}")
        raise HTTPException(status_code=404, detail="Série não encontrada")
    return series

# 🆕 Criar série via JSON (sem pôster)
@router.post("/", response_model=schemas.SeriesOut)
def create_series(
    series: schemas.SeriesCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    logger.info(f"🆕 Criando nova série: {series.title}")
    return services.create(db, series, user_id=current_user.id)

# 🖼️ Criar série com upload via FormData
@router.post("/upload", response_model=schemas.SeriesOut)
async def create_series_with_upload(
    title: str = Form(...),
    description: str = Form(None),
    start_year: int = Form(None),
    end_year: int = Form(None),
    genre_ids: str = Form(...),  # JSON string: '[1, 2]'
    poster: UploadFile = File(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    logger.info("🖼️ [UPLOAD] Criando série com pôster")
    
    try:
        genre_ids_list = json.loads(genre_ids)
        if not isinstance(genre_ids_list, list):
            raise ValueError()
    except Exception as e:
        logger.error(f"❌ Erro ao processar genre_ids: {genre_ids} | {e}")
        raise HTTPException(status_code=400, detail="Campo 'genre_ids' deve ser uma lista JSON válida")

    data = schemas.SeriesCreate(
        title=title,
        description=description,
        start_year=start_year,
        end_year=end_year,
        genre_ids=genre_ids_list,
        poster=poster
    )

    return services.create(db, data, user_id=current_user.id)

# ✏️ Atualizar série via JSON
@router.put("/{series_id}", response_model=schemas.SeriesOut)
def update_series(
    series_id: int,
    series: schemas.SeriesUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    logger.info(f"✏️ Atualizando série ID={series_id}")
    updated = services.update(db, series_id, series)
    if not updated:
        logger.warning(f"❌ Série não encontrada para atualizar ID={series_id}")
        raise HTTPException(status_code=404, detail="Série não encontrada")
    return updated

# ✏️ Atualizar série com pôster via FormData
@router.put("/upload/{series_id}", response_model=schemas.SeriesOut)
async def update_series_with_upload(
    series_id: int,
    title: str = Form(...),
    description: str = Form(None),
    start_year: int = Form(None),
    end_year: int = Form(None),
    genre_ids: str = Form(...),
    poster: UploadFile = File(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    logger.info(f"🖊️ Atualizando série com upload ID={series_id}")

    try:
        genre_ids_list = json.loads(genre_ids)
        if not isinstance(genre_ids_list, list):
            raise ValueError()
    except Exception as e:
        logger.error(f"❌ Erro ao processar genre_ids: {genre_ids} | {e}")
        raise HTTPException(status_code=400, detail="Campo 'genre_ids' deve ser uma lista JSON válida")

    data = schemas.SeriesCreate(
        title=title,
        description=description,
        start_year=start_year,
        end_year=end_year,
        genre_ids=genre_ids_list,
        poster=poster
    )

    return services.update_with_upload(db, series_id, data)

# 🗑️ Soft delete (marcar como deletado)
@router.delete("/{series_id}")
def delete_series(
    series_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    logger.info(f"🗑️ Solicitando exclusão lógica da série ID={series_id}")
    deleted = services.delete(db, series_id)
    if not deleted:
        logger.warning(f"❌ Série não encontrada para exclusão lógica ID={series_id}")
        raise HTTPException(status_code=404, detail="Série não encontrada")
    return {"detail": "Série excluída (soft delete)"}

# 🔥 Exclusão definitiva (hard delete)
@router.delete("/hard/{series_id}")
def hard_delete_series(
    series_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    logger.warning(f"🔥 HARD DELETE solicitado para série ID={series_id}")
    deleted = services.hard_delete(db, series_id)
    if not deleted:
        logger.error(f"❌ Série não encontrada para hard delete ID={series_id}")
        raise HTTPException(status_code=404, detail="Série não encontrada")
    return {"detail": "Série removida definitivamente"}
