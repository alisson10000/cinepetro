from sqlalchemy.orm import Session
from sqlalchemy import select
from app.modules.serie_genre.models import serie_genre

def vincular_genero_a_serie(db: Session, serie_id: int, genero_id: int):
    """Associa um gênero à série, se ainda não estiver associado."""
    existe = db.execute(
        select(serie_genre).where(
            (serie_genre.c.series_id == serie_id) &
            (serie_genre.c.genre_id == genero_id)
        )
    ).first()

    if existe:
        return {"detail": "Gênero já está vinculado à série"}

    insert_stmt = serie_genre.insert().values(
        series_id=serie_id,
        genre_id=genero_id
    )
    db.execute(insert_stmt)
    db.commit()
    return {"detail": "Gênero vinculado com sucesso"}


def desvincular_genero_de_serie(db: Session, serie_id: int, genero_id: int):
    """Remove a associação entre um gênero e uma série."""
    delete_stmt = serie_genre.delete().where(
        (serie_genre.c.series_id == serie_id) &
        (serie_genre.c.genre_id == genero_id)
    )
    result = db.execute(delete_stmt)
    db.commit()

    if result.rowcount == 0:
        return {"detail": "Associação não encontrada"}

    return {"detail": "Gênero desvinculado com sucesso"}
