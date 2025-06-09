from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

from app.modules.core.database import Base
from app.modules.movie_genre.models import movie_genre
from app.modules.serie_genre.models import serie_genre

class Genre(Base):
    """
    Modelo de Gênero, utilizado tanto para filmes quanto para séries.
    Implementa:
    - Campos de controle: created_at, updated_at, deleted_at (soft delete)
    - Relacionamentos N:N com filmes e séries
    """

    __tablename__ = "genres"

    # Identificador único do gênero
    id = Column(Integer, primary_key=True, index=True)

    # Nome do gênero (ex: Ação, Drama)
    name = Column(String(100), unique=True, nullable=False)

    # Timestamps e soft delete
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    deleted_at = Column(DateTime, nullable=True)

    # Relacionamento com filmes (muitos para muitos via movie_genre)
    movies = relationship(
        "Movie",
        secondary=movie_genre,
        back_populates="genres",
        lazy="joined"
    )

    # Relacionamento com séries (muitos para muitos via serie_genre)
    series = relationship(
        "Series",
        secondary=serie_genre,
        back_populates="genres",
        lazy="joined"
    )
