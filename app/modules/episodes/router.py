from fastapi import APIRouter, Depends, HTTPException
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
        raise HTTPException(status_code=404, detail="Episode not found")
    return ep

@router.post("/", response_model=schemas.EpisodeOut)
def create_episode(
    episode: schemas.EpisodeCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)  # Protegido por JWT
):
    return services.create(db, episode)

@router.put("/{episode_id}", response_model=schemas.EpisodeOut)
def update_episode(
    episode_id: int,
    episode: schemas.EpisodeUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)  # Protegido por JWT
):
    updated = services.update(db, episode_id, episode)
    if not updated:
        raise HTTPException(status_code=404, detail="Episode not found")
    return updated

@router.delete("/{episode_id}")
def delete_episode(
    episode_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)  # Protegido por JWT
):
    deleted = services.delete(db, episode_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Episode not found")
    return {"detail": "Episode deleted"}
