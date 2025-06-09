from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.modules.core.database import get_db
from app.modules.core.dependencies import get_current_user
from app.modules.user.models import User
from . import schema, service

router = APIRouter(prefix="/serie-genero", tags=["SerieGenero"])

@router.post("/", status_code=201)
def vincular_serie_genero(
    dados: schema.SerieGeneroIn,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    service.vincular_genero_a_serie(db, dados.serie_id, dados.genero_id)
    return {"detail": "Gênero vinculado à série com sucesso."}

@router.delete("/", status_code=200)
def desvincular_serie_genero(
    dados: schema.SerieGeneroIn,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    service.desvincular_genero_de_serie(db, dados.serie_id, dados.genero_id)
    return {"detail": "Gênero desvinculado da série com sucesso."}
