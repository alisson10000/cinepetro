# app/modules/serie_genre/schemas.py

from pydantic import BaseModel, Field

class SerieGeneroIn(BaseModel):
    serie_id: int = Field(..., description="ID da série", example=1)
    genero_id: int = Field(..., description="ID do gênero", example=3)

    class Config:
        from_attributes = True
