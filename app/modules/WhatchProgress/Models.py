from sqlalchemy import Column, Integer, Float, ForeignKey, DateTime, UniqueConstraint
from sqlalchemy.orm import relationship
from datetime import datetime

from app.modules.core.database import Base

class WatchProgress(Base):
    """
    Modelo ORM da tabela 'watch_progress', que armazena o progresso de visualização
    por usuário, seja de um filme ou episódio.
    """

    __tablename__ = "watch_progress"
    __table_args__ = (
        UniqueConstraint("user_id", "movie_id", "episode_id", name="unique_user_movie_episode"),
    )

    id = Column(Integer, primary_key=True, autoincrement=True)

    # 🔗 Referência ao usuário
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # 🎬 Filme assistido (pode ser nulo se for episódio)
    movie_id = Column(Integer, ForeignKey("movies.id"), nullable=True)

    # 📺 Episódio assistido (pode ser nulo se for filme)
    episode_id = Column(Integer, ForeignKey("episodes.id"), nullable=True)

    # ⏱️ Tempo atual de reprodução em segundos
    time_seconds = Column(Float, default=0, nullable=False)

    # 🕒 Última atualização do progresso
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # 🔁 Relacionamentos ORM

    user = relationship("User", back_populates="watch_progress")
    movie = relationship("Movie", back_populates="watch_progress")
    episode = relationship("Episode", back_populates="watch_progress")
