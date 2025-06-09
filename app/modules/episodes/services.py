from sqlalchemy.orm import Session
from . import models, schemas
from datetime import datetime

def get_all(db: Session):
    return db.query(models.Episode).filter(models.Episode.deleted_at == None).all()

def get_by_id(db: Session, episode_id: int):
    return db.query(models.Episode).filter(models.Episode.id == episode_id, models.Episode.deleted_at == None).first()

def create(db: Session, episode: schemas.EpisodeCreate):
    db_episode = models.Episode(**episode.dict())
    db.add(db_episode)
    db.commit()
    db.refresh(db_episode)
    return db_episode

def update(db: Session, episode_id: int, data: schemas.EpisodeUpdate):
    episode = get_by_id(db, episode_id)
    if not episode:
        return None
    for field, value in data.dict(exclude_unset=True).items():
        setattr(episode, field, value)
    db.commit()
    db.refresh(episode)
    return episode

def delete(db: Session, episode_id: int):
    episode = get_by_id(db, episode_id)
    if not episode:
        return None
    episode.deleted_at = datetime.utcnow()
    db.commit()
    return episode
