from pydantic import BaseModel

class SerieGeneroIn(BaseModel):
    serie_id: int
    genero_id: int
