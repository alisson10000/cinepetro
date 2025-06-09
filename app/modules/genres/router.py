from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from . import schemas, services
from app.modules.core.database import get_db
from app.modules.core.dependencies import get_current_user
from app.modules.user.models import User
from typing import List

router = APIRouter(prefix="/genres", tags=["Genres"])

# Listar todos os gêneros
@router.get("/", response_model=List[schemas.GenreOut])
def list_genres(db: Session = Depends(get_db)):
    return services.get_all(db)

# Obter gênero por ID
@router.get("/{genre_id}", response_model=schemas.GenreOut)
def get_genre(genre_id: int, db: Session = Depends(get_db)):
    genre = services.get_by_id(db, genre_id)
    if not genre:
        raise HTTPException(status_code=404, detail="Genre not found")
    return genre

# Criar um único gênero
@router.post("/", response_model=schemas.GenreOut)
def create_genre(
    genre: schemas.GenreCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)  # Protegido por JWT
):
    return services.create(db, genre)

# Atualizar um gênero existente
@router.put("/{genre_id}", response_model=schemas.GenreOut)
def update_genre(
    genre_id: int,
    genre: schemas.GenreUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    updated = services.update(db, genre_id, genre)
    if not updated:
        raise HTTPException(status_code=404, detail="Genre not found")
    return updated

# Deletar um gênero
@router.delete("/{genre_id}")
def delete_genre(
    genre_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    deleted = services.delete(db, genre_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Genre not found")
    return {"detail": "Genre deleted"}

# Criar múltiplos gêneros de uma vez
@router.post("/batch", response_model=List[schemas.GenreOut])
def create_genres_batch(
    genres: List[schemas.GenreCreate],
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return services.create_many(db, genres)
