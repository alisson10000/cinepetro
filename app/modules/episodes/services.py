from sqlalchemy.orm import Session
from . import models, schemas

def get_all(db: Session):
    return db.query(models.Episode).all()

def get_by_serie_id(db: Session, serie_id: int):
    return (
        db.query(models.Episode)
        .filter(models.Episode.series_id == serie_id)
        .order_by(models.Episode.season_number, models.Episode.episode_number)
        .all()
    )

def get_by_id(db: Session, episode_id: int):
    return db.query(models.Episode).filter(models.Episode.id == episode_id).first()

def create(db: Session, episode: schemas.EpisodeCreate, user_id: int):
    data = episode.dict()
    data["created_by"] = user_id

    db_episode = models.Episode(**data)
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

    db.delete(episode)
    db.commit()
    return True
