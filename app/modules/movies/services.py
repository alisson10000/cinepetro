import os
import re
import logging
from datetime import datetime
from sqlalchemy.orm import Session, joinedload

from . import models, schemas
from app.modules.genres.models import Genre

logger = logging.getLogger("cinepetro.movies.services")

# 📁 Diretórios para armazenar pôsteres
POSTER_FOLDER = "app/static/posters"
POSTER_URL_PREFIX = "posters/"

# 🔐 Sanitiza o nome do arquivo para evitar riscos de segurança
def sanitize_filename(filename: str) -> str:
    return re.sub(r'[^a-zA-Z0-9_.-]', '_', filename)

# 💾 Salva um novo pôster localmente
def save_poster(poster_file) -> str:
    try:
        os.makedirs(POSTER_FOLDER, exist_ok=True)
        filename = f"{datetime.utcnow().timestamp()}_{sanitize_filename(poster_file.filename)}"
        poster_path = os.path.join(POSTER_FOLDER, filename)
        with open(poster_path, "wb") as f:
            f.write(poster_file.file.read())
        logger.info(f"💾 Pôster salvo em: {poster_path}")
        return f"{POSTER_URL_PREFIX}{filename}"
    except Exception as e:
        logger.error(f"❌ Erro ao salvar pôster: {e}")
        return ""

# 🧹 Remove o pôster do sistema de arquivos
def remove_poster(poster_path: str):
    if poster_path:
        full_path = os.path.join("app/static", poster_path)
        if os.path.exists(full_path):
            try:
                os.remove(full_path)
                logger.info(f"🧹 Pôster removido: {full_path}")
            except Exception as e:
                logger.warning(f"⚠️ Falha ao remover pôster: {e}")

# 📋 Lista todos os filmes não deletados
def get_all(db: Session):
    logger.info("📋 Buscando todos os filmes não deletados")
    return db.query(models.Movie).filter(models.Movie.deleted_at == None).all()

# 🔍 Busca um filme específico por ID e carrega os gêneros relacionados
def get_by_id(db: Session, movie_id: int):
    logger.info(f"🔍 Buscando filme por ID={movie_id} com gêneros")
    return db.query(models.Movie)\
        .options(joinedload(models.Movie.genres))\
        .filter(models.Movie.id == movie_id, models.Movie.deleted_at == None).first()

# ➕ Criação de um novo filme
def create(db: Session, movie: schemas.MovieCreate, user_id: int):
    logger.info("🎬 Criando novo filme")
    poster_path = save_poster(movie.poster) if movie.poster else ""

    db_movie = models.Movie(
        title=movie.title,
        description=movie.description,
        year=movie.year,
        duration=movie.duration,
        poster=poster_path,
        created_by=user_id
    )

    if movie.genre_ids:
        logger.info(f"🎭 Associando gêneros: {movie.genre_ids}")
        db_movie.genres = db.query(Genre).filter(Genre.id.in_(movie.genre_ids)).all()

    db.add(db_movie)
    db.commit()
    db.refresh(db_movie)
    logger.info(f"✅ Filme criado com ID={db_movie.id}")
    return db_movie

# ✏️ Atualização sem upload de pôster
def update(db: Session, movie_id: int, movie_data: schemas.MovieUpdate):
    logger.info(f"✏️ Atualizando filme ID={movie_id} via JSON")
    movie = get_by_id(db, movie_id)
    if not movie:
        logger.warning(f"❌ Filme não encontrado para atualização: ID={movie_id}")
        return None

    update_data = movie_data.dict(exclude_unset=True)

    for field, value in update_data.items():
        if field == "genre_ids":
            logger.info(f"🔁 Atualizando gêneros: {value}")
            movie.genres = db.query(Genre).filter(Genre.id.in_(value)).all()
        elif field == "poster" and value != movie.poster:
            remove_poster(movie.poster)
            movie.poster = value
        else:
            setattr(movie, field, value)

    db.commit()
    db.refresh(movie)
    logger.info(f"✅ Filme atualizado com sucesso: ID={movie.id}")
    return movie

# ✏️ Atualização com FormData e novo upload
def update_with_upload(db: Session, movie_id: int, movie_data: schemas.MovieCreate):
    logger.info(f"🖊️ Atualizando filme com FormData ID={movie_id}")
    movie = get_by_id(db, movie_id)
    if not movie:
        logger.warning(f"❌ Filme não encontrado para atualização com upload: ID={movie_id}")
        return None

    if movie_data.poster:
        remove_poster(movie.poster)
        movie.poster = save_poster(movie_data.poster)

    movie.title = movie_data.title
    movie.description = movie_data.description
    movie.year = movie_data.year
    movie.duration = movie_data.duration

    logger.info(f"🎭 Atualizando gêneros para: {movie_data.genre_ids}")
    movie.genres = db.query(Genre).filter(Genre.id.in_(movie_data.genre_ids)).all()

    db.commit()
    db.refresh(movie)
    logger.info(f"✅ Filme atualizado com novo pôster: ID={movie.id}")
    return movie

# 🗑️ Exclusão lógica do filme (com remoção do pôster)
def delete(db: Session, movie_id: int):
    logger.info(f"🗑️ Solicitando exclusão lógica do filme ID={movie_id}")
    movie = get_by_id(db, movie_id)
    if not movie:
        logger.warning(f"❌ Filme não encontrado para exclusão: ID={movie_id}")
        return None

    remove_poster(movie.poster)
    movie.deleted_at = datetime.utcnow()
    db.commit()
    logger.info(f"✅ Filme marcado como deletado: ID={movie.id}")
    return movie

# 💀 Exclusão permanente do banco de dados + pôster
def hard_delete(db: Session, movie_id: int):
    logger.info(f"💀 Solicitando exclusão permanente do filme ID={movie_id}")
    movie = db.query(models.Movie).filter(models.Movie.id == movie_id).first()
    if not movie:
        logger.warning(f"❌ Filme não encontrado para exclusão permanente: ID={movie_id}")
        return None

    remove_poster(movie.poster)
    db.delete(movie)
    db.commit()
    logger.info(f"✅ Filme excluído permanentemente: ID={movie.id}")
    return True
