from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException

from app.modules.WhatchProgress.Models import WatchProgress
from app.modules.WhatchProgress.schemas import WatchProgressCreate, WatchProgressOut, MovieProgressOut
from app.modules.core.logger import logger
from app.modules.movies.models import Movie  # 🔗 Import necessário para o JOIN

# 🔍 Recuperar progresso individual (filme ou episódio)
def get_progress(db: Session, user_id: int, movie_id: int = None, episode_id: int = None) -> WatchProgressOut:
    query = db.query(WatchProgress).filter(WatchProgress.user_id == user_id)

    if movie_id is not None:
        query = query.filter(WatchProgress.movie_id == movie_id)
    if episode_id is not None:
        query = query.filter(WatchProgress.episode_id == episode_id)
    else:
        query = query.filter(WatchProgress.episode_id.is_(None))

    progress = query.first()
    if not progress:
        logger.warning(f"⚠️ Progresso não encontrado | user_id={user_id}, movie_id={movie_id}, episode_id={episode_id}")
        raise HTTPException(status_code=404, detail="Progresso não encontrado")

    logger.info(f"📤 Progresso recuperado | user_id={user_id}, movie_id={movie_id}, episode_id={episode_id}, time={progress.time_seconds}s")
    return WatchProgressOut.from_orm(progress)

# 💾 Salvar ou atualizar progresso de filme ou episódio
def save_or_update_progress(
    db: Session,
    user_id: int,
    movie_id: int = None,
    episode_id: int = None,
    time_seconds: float = 0
) -> WatchProgressOut:
    query = db.query(WatchProgress).filter(
        WatchProgress.user_id == user_id,
        WatchProgress.movie_id == movie_id,
    )

    if episode_id is not None:
        query = query.filter(WatchProgress.episode_id == episode_id)
    else:
        query = query.filter(WatchProgress.episode_id.is_(None))

    existing = query.first()

    if existing:
        existing.time_seconds = time_seconds
        db.commit()
        db.refresh(existing)
        logger.info(f"🔄 Progresso atualizado | user_id={user_id}, movie_id={movie_id}, episode_id={episode_id}, time={time_seconds}s")
        return WatchProgressOut.from_orm(existing)

    new_progress = WatchProgress(
        user_id=user_id,
        movie_id=movie_id,
        episode_id=episode_id,
        time_seconds=time_seconds
    )
    db.add(new_progress)
    try:
        db.commit()
        logger.info(f"🆕 Novo progresso salvo | user_id={user_id}, movie_id={movie_id}, episode_id={episode_id}, time={time_seconds}s")
    except IntegrityError as e:
        db.rollback()
        logger.error(f"❌ Erro de integridade ao salvar progresso | user_id={user_id}, movie_id={movie_id}, episode_id={episode_id} | erro={e}")
        raise HTTPException(status_code=400, detail="Violação de integridade: combinação já existente")

    db.refresh(new_progress)
    return WatchProgressOut.from_orm(new_progress)

# 🧠 Buscar lista de filmes parcialmente assistidos (para "Continuar Assistindo")
def get_movies_to_continue(db: Session, user_id: int) -> list[MovieProgressOut]:
    try:
        resultados = (
            db.query(WatchProgress, Movie)
            .join(Movie, Movie.id == WatchProgress.movie_id)
            .filter(WatchProgress.user_id == user_id)
            .filter(WatchProgress.movie_id != None)
            .filter(WatchProgress.episode_id.is_(None))  # ✅ Apenas filmes
            .filter(WatchProgress.time_seconds > 0)
            .filter(Movie.duration != None)
            .filter(WatchProgress.time_seconds < Movie.duration * 60 * 0.95)
            .all()
        )
    except Exception as e:
        logger.error(f"❌ Erro na query do get_movies_to_continue: {e}")
        raise HTTPException(status_code=500, detail="Erro interno ao consultar filmes para continuar")

    retorno = []
    for progress, movie in resultados:
        try:
            retorno.append(MovieProgressOut(
                movie_id=movie.id,
                title=movie.title,
                poster=movie.poster,
                time_seconds=progress.time_seconds,
                duration_seconds=movie.duration
            ))
        except Exception as e:
            logger.error(f"❌ Erro ao montar MovieProgressOut: {e} | movie={movie} | progress={progress}")
            continue

    logger.info(f"📋 Filmes para continuar assistindo encontrados: {len(retorno)}")
    return retorno
