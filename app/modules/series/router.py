from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from . import schemas, services
from app.modules.core.database import get_db
from app.modules.core.dependencies import get_current_user
from app.modules.user.models import User

router = APIRouter(prefix="/series", tags=["Series"])

@router.get("/", response_model=list[schemas.SeriesOut])
def list_series(db: Session = Depends(get_db)):
    return services.get_all(db)

@router.get("/{series_id}", response_model=schemas.SeriesOut)
def get_series(series_id: int, db: Session = Depends(get_db)):
    series = services.get_by_id(db, series_id)
    if not series:
        raise HTTPException(status_code=404, detail="Series not found")
    return series

@router.post("/", response_model=schemas.SeriesOut)
def create_series(
    series: schemas.SeriesCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)  # Protegido por token
):
    return services.create(db, series)

@router.put("/{series_id}", response_model=schemas.SeriesOut)
def update_series(
    series_id: int,
    series: schemas.SeriesUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)  # Protegido por token
):
    updated = services.update(db, series_id, series)
    if not updated:
        raise HTTPException(status_code=404, detail="Series not found")
    return updated

@router.delete("/{series_id}")
def delete_series(
    series_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)  # Protegido por token
):
    deleted = services.delete(db, series_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Series not found")
    return {"detail": "Series deleted"}
