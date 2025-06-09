from sqlalchemy.orm import Session
from app.modules.serie_genre.models import serie_genre

def vincular_genero_a_serie(db: Session, serie_id: int, genero_id: int):
    insert_stmt = serie_genre.insert().values(serie_id=serie_id, genre_id=genero_id)
    db.execute(insert_stmt)
    db.commit()

def desvincular_genero_de_serie(db: Session, serie_id: int, genero_id: int):
    delete_stmt = serie_genre.delete().where(
        (serie_genre.c.serie_id == serie_id) &
        (serie_genre.c.genre_id == genero_id)
    )
    db.execute(delete_stmt)
    db.commit()
