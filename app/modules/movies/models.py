from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
import logging

from app.modules.core.database import Base

# 📋 Logger para depuração durante o carregamento da model
logger = logging.getLogger("cinepetro.movies.models")
logger.info("📦 Modelo Movie carregado com sucesso")

class Movie(Base):
    """
    Modelo ORM da tabela 'movies' do banco de dados CinePetro.

    Representa filmes cadastrados, com atributos descritivos, 
    relacionamento com gêneros e controle de autoria e exclusão lógica.
    """

    __tablename__ = "movies"

    # 🔑 ID único do filme
    id = Column(Integer, primary_key=True, index=True)

    # 🎬 Título do filme (obrigatório, até 255 caracteres)
    title = Column(String(255), nullable=False)

    # 📝 Sinopse ou descrição (opcional)
    description = Column(Text, nullable=True)

    # 📅 Ano de lançamento (opcional)
    year = Column(Integer, nullable=True)

    # ⏱️ Duração total em minutos (opcional)
    duration = Column(Integer, nullable=True)

    # 🖼️ Caminho do pôster salvo em /static/posters/
    poster = Column(String(255), nullable=False, default="")

    # 👤 ID do usuário criador (relacionamento externo)
    created_by = Column(Integer, ForeignKey("users.id"), nullable=True)

    # 🕒 Controle de criação e atualização
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    deleted_at = Column(DateTime, nullable=True)  # 🗑️ Exclusão lógica (soft delete)

    # 🔗 Relacionamentos

    # Muitos para muitos com gêneros
    genres = relationship("Genre", secondary="movie_genre", back_populates="movies")

    # Criador do filme (relacionamento reverso com User)
    creator = relationship("User", back_populates="movies")
