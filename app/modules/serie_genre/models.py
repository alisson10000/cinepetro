# app/modules/serie_genre/models.py

from sqlalchemy import Table, Column, Integer, ForeignKey
from app.modules.core.database import Base

serie_genre = Table(
    "serie_genre",
    Base.metadata,
    Column("series_id", Integer, ForeignKey("series.id", ondelete="CASCADE"), primary_key=True),
    Column("genre_id", Integer, ForeignKey("genres.id", ondelete="CASCADE"), primary_key=True)
)
