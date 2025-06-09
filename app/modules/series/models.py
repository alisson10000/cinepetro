# app/modules/series/models.py

from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

from app.modules.core.database import Base
from app.modules.serie_genre.models import serie_genre  # Tabela associativa M2M com Genre

class Series(Base):
    __tablename__ = "series"

    # Identificador principal
    id = Column(Integer, primary_key=True, index=True)

    # Campos principais da série
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    start_year = Column(Integer, nullable=True)
    end_year = Column(Integer, nullable=True)

    # Informações de autoria e timestamps
    created_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    deleted_at = Column(DateTime, nullable=True)

    # Relacionamentos

    # M2M com Genre (via tabela serie_genre)
    genres = relationship(
        "Genre",
        secondary=serie_genre,
        back_populates="series"
    )

    # Usuário criador da série (relacionamento com User)
    creator = relationship("User", back_populates="series")

    # Relacionamento com episódios (1 série → N episódios)
    episodes = relationship(
        "Episode",
        back_populates="series",
        cascade="all, delete-orphan"
    )
