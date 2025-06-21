import logging
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.modules.core.database import get_db
from app.modules.core.dependencies import get_current_user
from app.modules.user.models import User
from . import schemas, services

logger = logging.getLogger("cinepetro.watch_progress")

router = APIRouter(prefix="/progress", tags=["Watch Progress"])

# 📥 Salvar ou atualizar progresso de filme ou episódio
@router.post("/save", response_model=schemas.WatchProgressOut)
def save_progress(
    progress_in: schemas.WatchProgressCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    logger.info(f"💾 Salvando progresso para user_id={current_user.id}")
    try:
        progress = services.save_or_update_progress(
            db=db,
            user_id=current_user.id,
            movie_id=progress_in.movie_id,
            episode_id=progress_in.episode_id,
            time_seconds=progress_in.time_seconds
        )
        return progress
    except Exception as e:
        logger.error(f"❌ Erro ao salvar progresso: {e}")
        raise HTTPException(status_code=500, detail="Erro ao salvar progresso")

# 🔍 Obter progresso de filme ou episódio
@router.get("/get", response_model=schemas.WatchProgressOut)
def get_progress(
    movie_id: int = None,
    episode_id: int = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if not movie_id and not episode_id:
        raise HTTPException(status_code=400, detail="É necessário informar movie_id ou episode_id")

    logger.info(f"🔍 Buscando progresso para user_id={current_user.id}")
    progress = services.get_progress(
        db=db,
        user_id=current_user.id,
        movie_id=movie_id,
        episode_id=episode_id
    )
    return progress
