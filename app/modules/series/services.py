from sqlalchemy.orm import Session
from . import models, schemas
from datetime import datetime
from app.modules.genres.models import Genre

def get_all(db: Session):
    return db.query(models.Series).filter(models.Series.deleted_at == None).all()

def get_by_id(db: Session, series_id: int):
    return db.query(models.Series).filter(models.Series.id == series_id, models.Series.deleted_at == None).first()

def create(db: Session, data: schemas.SeriesCreate):
    db_series = models.Series(
        title=data.title,
        description=data.description,
        start_year=data.start_year,
        end_year=data.end_year
    )
    if data.genre_ids:
        db_series.genres = db.query(Genre).filter(Genre.id.in_(data.genre_ids)).all()

    db.add(db_series)
    db.commit()
    db.refresh(db_series)
    return db_series

def update(db: Session, series_id: int, data: schemas.SeriesUpdate):
    series = get_by_id(db, series_id)
    if not series:
        return None

    for field, value in data.dict(exclude_unset=True).items():
        if field == "genre_ids":
            series.genres = db.query(Genre).filter(Genre.id.in_(value)).all()
        else:
            setattr(series, field, value)

    db.commit()
    db.refresh(series)
    return series

def delete(db: Session, series_id: int):
    series = get_by_id(db, series_id)
    if not series:
        return None
    series.deleted_at = datetime.utcnow()
    db.commit()
    return series
