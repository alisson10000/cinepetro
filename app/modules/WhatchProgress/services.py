from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException

from app.modules.WhatchProgress.Models import WatchProgress
from app.modules.WhatchProgress.schemas import WatchProgressCreate, WatchProgressOut


def get_progress(db: Session, user_id: int, movie_id: int = None, episode_id: int = None) -> WatchProgressOut:
    query = db.query(WatchProgress).filter(WatchProgress.user_id == user_id)

    if movie_id:
        query = query.filter(WatchProgress.movie_id == movie_id)
    if episode_id:
        query = query.filter(WatchProgress.episode_id == episode_id)

    progress = query.first()
    if not progress:
        raise HTTPException(status_code=404, detail="Progresso não encontrado")

    return WatchProgressOut.from_orm(progress)


def save_or_update_progress(
    db: Session,
    user_id: int,
    movie_id: int = None,
    episode_id: int = None,
    time_seconds: float = 0
) -> WatchProgressOut:
    query = db.query(WatchProgress).filter(
        WatchProgress.user_id == user_id,
        WatchProgress.movie_id == movie_id,
        WatchProgress.episode_id == episode_id
    )

    existing = query.first()

    if existing:
        existing.time_seconds = time_seconds
        db.commit()
        db.refresh(existing)
        return WatchProgressOut.from_orm(existing)

    new_progress = WatchProgress(
        user_id=user_id,
        movie_id=movie_id,
        episode_id=episode_id,
        time_seconds=time_seconds
    )
    db.add(new_progress)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Violação de integridade: combinação já existente")

    db.refresh(new_progress)
    return WatchProgressOut.from_orm(new_progress)
