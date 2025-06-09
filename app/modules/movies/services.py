from sqlalchemy.orm import Session
from datetime import datetime
from . import models, schemas
from app.modules.genres.models import Genre

def get_all(db: Session):
    return db.query(models.Movie).filter(models.Movie.deleted_at == None).all()

def get_by_id(db: Session, movie_id: int):
    return db.query(models.Movie).filter(
        models.Movie.id == movie_id,
        models.Movie.deleted_at == None
    ).first()

def create(db: Session, movie: schemas.MovieCreate, user_id: int):
    db_movie = models.Movie(
        title=movie.title,
        description=movie.description,
        year=movie.year,
        duration=movie.duration,
        created_by=user_id  # ⚠️ Aqui usamos o ID, não o objeto User
    )

    if movie.genre_ids:
        db_movie.genres = db.query(Genre).filter(Genre.id.in_(movie.genre_ids)).all()

    db.add(db_movie)
    db.commit()
    db.refresh(db_movie)
    return db_movie

def update(db: Session, movie_id: int, movie_data: schemas.MovieUpdate):
    movie = get_by_id(db, movie_id)
    if not movie:
        return None

    for field, value in movie_data.dict(exclude_unset=True).items():
        if field == "genre_ids":
            movie.genres = db.query(Genre).filter(Genre.id.in_(value)).all()
        else:
            setattr(movie, field, value)

    db.commit()
    db.refresh(movie)
    return movie

def delete(db: Session, movie_id: int):
    movie = get_by_id(db, movie_id)
    if not movie:
        return None
    movie.deleted_at = datetime.utcnow()
    db.commit()
    return movie
