import logging
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.modules.core.database import get_db
from app.modules.core.dependencies import get_current_user
from app.modules.user.models import User
from . import schemas, services

logger = logging.getLogger("cinepetro.watch_progress")

router = APIRouter(prefix="/progress", tags=["Watch Progress"])


# 📥 Salvar ou atualizar progresso
@router.post("/save", response_model=schemas.WatchProgressOut, status_code=status.HTTP_201_CREATED)
def save_progress(
    progress_in: schemas.WatchProgressCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    logger.info(
        f"📥 [SAVE] Início | user_id={current_user.id}, "
        f"movie_id={progress_in.movie_id}, episode_id={progress_in.episode_id}, "
        f"time={progress_in.time_seconds}s"
    )

    if progress_in.movie_id and progress_in.episode_id:
        logger.warning("⚠️ [SAVE] movie_id e episode_id informados ao mesmo tempo — inválido.")
        raise HTTPException(status_code=400, detail="Informe apenas movie_id ou episode_id, não ambos.")

    try:
        progress = services.save_or_update_progress(
            db=db,
            user_id=current_user.id,
            movie_id=progress_in.movie_id,
            episode_id=progress_in.episode_id,
            time_seconds=progress_in.time_seconds
        )
        logger.info(f"✅ [SAVE] Progresso salvo com sucesso | id={progress.id}")
        return progress
    except Exception:
        logger.exception("❌ [SAVE] Erro inesperado ao salvar progresso")
        raise HTTPException(status_code=500, detail="Erro interno ao salvar progresso")


# 🔍 Obter progresso de um item
@router.get("/get", response_model=schemas.WatchProgressOut)
def get_progress(
    movie_id: Optional[int] = None,
    episode_id: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    logger.info(
        f"🔍 [GET] Solicitando progresso | user_id={current_user.id}, "
        f"movie_id={movie_id}, episode_id={episode_id}"
    )

    if not movie_id and not episode_id:
        logger.warning("⚠️ [GET] Nenhum ID informado")
        raise HTTPException(status_code=400, detail="É necessário informar movie_id ou episode_id")

    if movie_id and episode_id:
        logger.warning("⚠️ [GET] Ambos movie_id e episode_id informados — inválido.")
        raise HTTPException(status_code=400, detail="Informe apenas movie_id ou episode_id, não ambos.")

    try:
        progress = services.get_progress(
            db=db,
            user_id=current_user.id,
            movie_id=movie_id,
            episode_id=episode_id
        )
        logger.info(f"✅ [GET] Progresso encontrado | id={progress.id}, time={progress.time_seconds}s")
        return progress
    except HTTPException:
        raise  # repassa o erro sem engolir
    except Exception:
        logger.exception("❌ [GET] Erro inesperado ao buscar progresso")
        raise HTTPException(status_code=500, detail="Erro ao buscar progresso")


# 🧠 Listar filmes e episódios para continuar assistindo
@router.get("/continuar", response_model=List[schemas.GenericProgressOut])
def continuar_assistindo(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    logger.info(f"📋 [CONTINUAR] Iniciando consulta de progresso | user_id={current_user.id}")

    try:
        retorno = services.get_all_progress_to_continue(db=db, user_id=current_user.id)

        logger.info(f"✅ [CONTINUAR] {len(retorno)} itens retornados")
        for item in retorno:
            tipo = "🎬 Filme" if getattr(item, "movie_id", None) else "📺 Episódio"
            logger.debug(f"  🔹 {tipo} | {item}")

        return retorno
    except Exception:
        logger.exception("❌ [CONTINUAR] Erro inesperado ao listar conteúdos para continuar assistindo")
        raise HTTPException(status_code=500, detail="Erro ao listar conteúdos para continuar assistindo")
