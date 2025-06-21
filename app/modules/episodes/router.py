from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from . import schemas, services
from app.modules.core.database import get_db
from app.modules.core.dependencies import get_current_user
from app.modules.user.models import User

router = APIRouter(prefix="/episodes", tags=["Episodes"])

@router.get("/", response_model=list[schemas.EpisodeOut])
def list_episodes(db: Session = Depends(get_db)):
    return services.get_all(db)

@router.get("/{episode_id}", response_model=schemas.EpisodeOut)
def get_episode(episode_id: int, db: Session = Depends(get_db)):
    ep = services.get_by_id(db, episode_id)
    if not ep:
        raise HTTPException(status_code=404, detail="🎬 Episódio não encontrado")
    return ep

@router.get("/by_serie/{serie_id}", response_model=list[schemas.EpisodeOut])
def get_episodes_by_serie(serie_id: int, db: Session = Depends(get_db)):
    episodes = services.get_by_serie_id(db, serie_id)
    if not episodes:
        raise HTTPException(status_code=404, detail="📭 Nenhum episódio encontrado para esta série")
    return episodes

@router.post("/", response_model=schemas.EpisodeOut, status_code=status.HTTP_201_CREATED)
def create_episode(
    episode: schemas.EpisodeCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return services.create(db, episode, user_id=current_user.id)

@router.put("/{episode_id}", response_model=schemas.EpisodeOut)
def update_episode(
    episode_id: int,
    episode: schemas.EpisodeUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    updated = services.update(db, episode_id, episode)
    if not updated:
        raise HTTPException(status_code=404, detail="🎬 Episódio não encontrado")
    return updated

@router.delete("/{episode_id}", status_code=status.HTTP_200_OK)
def delete_episode(
    episode_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    success = services.delete(db, episode_id)
    if not success:
        raise HTTPException(status_code=404, detail="🎬 Episódio não encontrado para exclusão")
    return {"detail": "🗑️ Episódio excluído com sucesso"}
