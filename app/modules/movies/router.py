from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.modules.core.database import get_db
from app.modules.core.dependencies import get_current_user
from app.modules.user.models import User
from . import schemas, services

router = APIRouter(prefix="/movies", tags=["Movies"])

@router.get("/", response_model=list[schemas.MovieOut])
def list_movies(db: Session = Depends(get_db)):
    return services.get_all(db)

@router.post("/", response_model=schemas.MovieOut)
def create_movie(
    movie: schemas.MovieCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return services.create(db, movie, user_id=current_user.id)

@router.put("/{movie_id}", response_model=schemas.MovieOut)
def update_movie(
    movie_id: int,
    movie: schemas.MovieUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return services.update(db, movie_id, movie)

@router.delete("/{movie_id}")
def delete_movie(
    movie_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return services.delete(db, movie_id)
