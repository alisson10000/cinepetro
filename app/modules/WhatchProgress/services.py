from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException

from app.modules.WhatchProgress.Models import WatchProgress
from app.modules.WhatchProgress.schemas import (
    WatchProgressOut,
    MovieProgressOut,
    EpisodeProgressOut,
    GenericProgressOut,
)
from app.modules.core.logger import logger
from app.modules.movies.models import Movie
from app.modules.series.models import Episode, Series


# 🔍 Recuperar progresso individual (filme ou episódio)
def get_progress(db: Session, user_id: int, movie_id: int = None, episode_id: int = None) -> WatchProgressOut:
    logger.info(f"🔍 [get_progress] user_id={user_id}, movie_id={movie_id}, episode_id={episode_id}")
    query = db.query(WatchProgress).filter(WatchProgress.user_id == user_id)

    if movie_id is not None:
        query = query.filter(WatchProgress.movie_id == movie_id)
    if episode_id is not None:
        query = query.filter(WatchProgress.episode_id == episode_id)
    else:
        query = query.filter(WatchProgress.episode_id.is_(None))

    progress = query.first()
    if not progress:
        logger.warning(f"⚠️ [get_progress] Progresso não encontrado")
        raise HTTPException(status_code=404, detail="Progresso não encontrado")

    logger.info(f"✅ [get_progress] Progresso recuperado com sucesso | id={progress.id}, time={progress.time_seconds}s")
    return WatchProgressOut.from_orm(progress)


# 📅 Salvar ou atualizar progresso
def save_or_update_progress(
    db: Session,
    user_id: int,
    movie_id: int = None,
    episode_id: int = None,
    time_seconds: float = 0
) -> WatchProgressOut:
    logger.info(f"📅 [save_or_update_progress] user_id={user_id}, movie_id={movie_id}, episode_id={episode_id}, time={time_seconds}")

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
        logger.info(f"🔁 [save_or_update_progress] Atualizando progresso existente | id={existing.id}")
        existing.time_seconds = time_seconds
        db.commit()
        db.refresh(existing)
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
        db.refresh(new_progress)
        logger.info(f"🌟 [save_or_update_progress] Novo progresso salvo | id={new_progress.id}")
        return WatchProgressOut.from_orm(new_progress)
    except IntegrityError as e:
        db.rollback()
        logger.error(f"❌ [save_or_update_progress] Erro de integridade | {e}")
        raise HTTPException(status_code=400, detail="Violacão de integridade: combinação já existente")


# 🎬 Buscar filmes parcialmente assistidos
def get_movies_to_continue(db: Session, user_id: int) -> list[MovieProgressOut]:
    logger.info(f"🎬 [get_movies_to_continue] user_id={user_id}")
    try:
        resultados = (
            db.query(WatchProgress, Movie)
            .join(Movie, Movie.id == WatchProgress.movie_id)
            .filter(WatchProgress.user_id == user_id)
            .filter(WatchProgress.movie_id != None)
            .filter(WatchProgress.episode_id.is_(None))
            .filter(WatchProgress.time_seconds > 0)
            .filter(Movie.duration != None)
            .filter(WatchProgress.time_seconds < Movie.duration * 60 * 0.95)
            .all()
        )
    except Exception as e:
        logger.error(f"❌ [get_movies_to_continue] Erro na query | {e}")
        raise HTTPException(status_code=500, detail="Erro ao consultar filmes para continuar")

    retorno = []
    for progress, movie in resultados:
        try:
            retorno.append(MovieProgressOut(
                movie_id=movie.id,
                title=movie.title,
                poster=movie.poster,
                time_seconds=progress.time_seconds,
                duration_seconds=movie.duration * 60,
                type="movie"
            ))
        except Exception as e:
            logger.warning(f"⚠️ [get_movies_to_continue] Falha ao montar MovieProgressOut | movie_id={movie.id}, erro={e}")
            continue

    logger.info(f"📋 [get_movies_to_continue] Total de filmes: {len(retorno)}")
    return retorno


# 📺 Buscar episódios parcialmente assistidos
def get_episodes_to_continue(db: Session, user_id: int) -> list[EpisodeProgressOut]:
    logger.info(f"📺 [get_episodes_to_continue] user_id={user_id}")
    try:
        resultados = (
            db.query(WatchProgress, Episode, Series)
            .join(Episode, Episode.id == WatchProgress.episode_id)
            .join(Series, Series.id == Episode.series_id)
            .filter(WatchProgress.user_id == user_id)
            .filter(WatchProgress.episode_id != None)
            .filter(WatchProgress.time_seconds > 0)
            .filter(Episode.duration != None)
            .filter(WatchProgress.time_seconds < Episode.duration * 60 * 0.95)
            .all()
        )
    except Exception as e:
        logger.error(f"❌ [get_episodes_to_continue] Erro na query | {e}")
        raise HTTPException(status_code=500, detail="Erro ao consultar episódios para continuar")

    retorno = []
    for progress, episode, series in resultados:
        try:
            retorno.append(EpisodeProgressOut(
            episode_id=episode.id,
            series_id=series.id,
            series_title=series.title,
            poster=series.poster,
            time_seconds=progress.time_seconds,
            duration_seconds=episode.duration * 60,
            episode_number=episode.episode_number,
            season_number=episode.season_number,
            title=episode.title,  # ✅ Aqui estava faltando
            type="series"
            ))
        except Exception as e:
            logger.warning(f"⚠️ [get_episodes_to_continue] Falha ao montar EpisodeProgressOut | episode_id={episode.id}, erro={e}")
            continue

    logger.info(f"📺 [get_episodes_to_continue] Total de episódios: {len(retorno)}")
    return retorno


# 🔁 Unifica tudo
def get_all_progress_to_continue(db: Session, user_id: int) -> list[GenericProgressOut]:
    logger.info(f"📊 [get_all_progress_to_continue] Iniciando agregação | user_id={user_id}")
    filmes = get_movies_to_continue(db, user_id)
    episodios = get_episodes_to_continue(db, user_id)

    logger.info(f"📊 [get_all_progress_to_continue] Total geral: filmes={len(filmes)}, episódios={len(episodios)}")
    return filmes + episodios
