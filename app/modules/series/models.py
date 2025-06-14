# app/modules/series/models.py

from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

from app.modules.core.database import Base
from app.modules.serie_genre.models import serie_genre  # Tabela associativa M2M
from app.modules.episodes.models import Episode  # Certifique-se de que existe
from app.modules.user.models import User         # Certifique-se de que existe

class Series(Base):
    __tablename__ = "series"

    id = Column(Integer, primary_key=True, index=True)

    # Campos principais
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    start_year = Column(Integer, nullable=True)
    end_year = Column(Integer, nullable=True)
    poster = Column(String(255), nullable=True)  # 🖼️ Caminho para o pôster da série

    # Auditoria e controle
    created_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    deleted_at = Column(DateTime, nullable=True)

    # 🔗 Relacionamentos

    genres = relationship(
        "Genre",
        secondary=serie_genre,
        back_populates="series"
    )

    creator = relationship("User", back_populates="series")

    episodes = relationship(
        "Episode",
        back_populates="series",
        cascade="all, delete-orphan"
    )
