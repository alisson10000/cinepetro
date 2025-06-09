from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from . import schemas, services
from app.modules.core.database import get_db

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/", response_model=list[schemas.UserOut])
def list_users(db: Session = Depends(get_db)):
    return services.get_all(db)

@router.get("/{user_id}", response_model=schemas.UserOut)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = services.get_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.post("/", response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    if services.get_by_email(db, user.email):
        raise HTTPException(status_code=400, detail="Email already registered")
    return services.create(db, user)

@router.put("/{user_id}", response_model=schemas.UserOut)
def update_user(user_id: int, data: schemas.UserUpdate, db: Session = Depends(get_db)):
    updated = services.update(db, user_id, data)
    if not updated:
        raise HTTPException(status_code=404, detail="User not found")
    return updated

@router.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    deleted = services.delete(db, user_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="User not found")
    return {"detail": "User deleted"}
