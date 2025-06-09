from sqlalchemy import Table, Column, ForeignKey
from app.modules.core.database import Base



movie_genre = Table(
    "movie_genre",
    Base.metadata,
    Column("movie_id", ForeignKey("movies.id"), primary_key=True),
    Column("genre_id", ForeignKey("genres.id"), primary_key=True)
)
