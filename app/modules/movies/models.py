from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

from app.modules.core.database import Base
from app.modules.movie_genre.models import movie_genre
from app.modules.user.models import User  # Garante visibilidade clara para tipagem
from app.modules.genres.models import Genre  # Garante visibilidade clara para tipagem

class Movie(Base):
    __tablename__ = "movies"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    year = Column(Integer, nullable=True)
    duration = Column(Integer, nullable=True)  # em minutos

    # Relacionamento com o usuário criador
    created_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    creator = relationship("User", back_populates="movies")

    # Datas de controle
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    deleted_at = Column(DateTime, nullable=True)

    # Relacionamento N:N com gêneros
    genres = relationship(
        "Genre",
        secondary=movie_genre,
        back_populates="movies"
    )
