from sqlalchemy.orm import Session
from datetime import datetime
from . import models, schemas
from typing import List, Optional

def get_all(db: Session) -> List[models.Genre]:
    """Retorna todos os gêneros ativos (não deletados)"""
    return db.query(models.Genre).filter(models.Genre.deleted_at == None).all()

def get_by_id(db: Session, genre_id: int) -> Optional[models.Genre]:
    """Busca um gênero pelo ID"""
    return db.query(models.Genre).filter(
        models.Genre.id == genre_id,
        models.Genre.deleted_at == None
    ).first()

def create(db: Session, genre: schemas.GenreCreate) -> models.Genre:
    """Cria um novo gênero"""
    db_genre = models.Genre(name=genre.name)
    db.add(db_genre)
    db.commit()
    db.refresh(db_genre)
    return db_genre

def create_many(db: Session, genres: List[schemas.GenreCreate]) -> List[models.Genre]:
    """Cria múltiplos gêneros de uma vez"""
    if not genres:
        return []

    db_genres = [models.Genre(name=genre.name) for genre in genres]
    db.add_all(db_genres)
    db.commit()
    for genre in db_genres:
        db.refresh(genre)
    return db_genres

def update(db: Session, genre_id: int, genre_data: schemas.GenreUpdate) -> Optional[models.Genre]:
    """Atualiza um gênero existente"""
    genre = get_by_id(db, genre_id)
    if not genre:
        return None
    genre.name = genre_data.name
    db.commit()
    db.refresh(genre)
    return genre

def delete(db: Session, genre_id: int) -> Optional[models.Genre]:
    """Marca um gênero como deletado (soft delete)"""
    genre = get_by_id(db, genre_id)
    if not genre:
        return None
    genre.deleted_at = datetime.utcnow()
    db.commit()
    return genre
