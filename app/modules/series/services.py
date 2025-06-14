import os
import re
import logging
from datetime import datetime
from sqlalchemy.orm import Session, joinedload

from . import models, schemas
from app.modules.genres.models import Genre

logger = logging.getLogger("cinepetro.series.services")

# 📁 Diretórios e prefixo de URLs para pôsteres
POSTER_FOLDER = "app/static/series"
POSTER_URL_PREFIX = "series/"


def sanitize_filename(filename: str) -> str:
    """Sanitiza nomes de arquivos para evitar falhas e ataques."""
    return re.sub(r'[^a-zA-Z0-9_.-]', '_', filename)


def save_poster(poster_file) -> str:
    """Salva o arquivo de pôster no disco e retorna o caminho relativo."""
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


def get_all(db: Session):
    """Lista todas as séries ativas."""
    logger.info("📋 Listando todas as séries disponíveis")
    return db.query(models.Series).filter(models.Series.deleted_at == None).all()


def get_by_id(db: Session, series_id: int):
    """Busca uma série por ID com seus gêneros."""
    logger.info(f"🔍 Buscando série ID={series_id}")
    return db.query(models.Series)\
        .options(joinedload(models.Series.genres))\
        .filter(models.Series.id == series_id, models.Series.deleted_at == None)\
        .first()


def create(db: Session, data: schemas.SeriesCreate, user_id: int):
    """Cria uma nova série com ou sem pôster."""
    logger.info("📥 Criando nova série")

    poster_path = save_poster(data.poster) if data.poster else ""

    db_series = models.Series(
        title=data.title,
        description=data.description,
        start_year=data.start_year,
        end_year=data.end_year,
        poster=poster_path,
        created_by=user_id
    )

    if data.genre_ids:
        logger.info(f"🎭 Associando gêneros: {data.genre_ids}")
        db_series.genres = db.query(Genre).filter(Genre.id.in_(data.genre_ids)).all()

    db.add(db_series)
    db.commit()
    db.refresh(db_series)
    logger.info(f"✅ Série criada com ID={db_series.id}")
    return db_series


def update(db: Session, series_id: int, data: schemas.SeriesUpdate):
    """Atualiza parcialmente uma série."""
    logger.info(f"🛠️ Atualizando série ID={series_id}")
    series = get_by_id(db, series_id)
    if not series:
        logger.warning(f"❌ Série não encontrada ID={series_id}")
        return None

    update_data = data.dict(exclude_unset=True)

    for field, value in update_data.items():
        if field == "genre_ids":
            logger.info(f"🔁 Atualizando gêneros: {value}")
            series.genres = db.query(Genre).filter(Genre.id.in_(value)).all()
        elif field == "poster" and value != series.poster:
            old_path = os.path.join("app/static", series.poster or "")
            if os.path.exists(old_path):
                try:
                    os.remove(old_path)
                    logger.info(f"🗑️ Pôster antigo removido: {old_path}")
                except Exception as e:
                    logger.warning(f"⚠️ Falha ao remover pôster antigo: {e}")
            series.poster = value
        else:
            setattr(series, field, value)

    db.commit()
    db.refresh(series)
    logger.info(f"✅ Série atualizada com sucesso ID={series.id}")
    return series


def delete(db: Session, series_id: int):
    """Marca uma série como deletada e remove seu pôster físico."""
    logger.info(f"🗑️ Solicitando exclusão lógica da série ID={series_id}")
    series = get_by_id(db, series_id)
    if not series:
        logger.warning(f"❌ Série não encontrada ID={series_id}")
        return None

    if series.poster:
        poster_path = os.path.join("app/static", series.poster)
        if os.path.exists(poster_path):
            try:
                os.remove(poster_path)
                logger.info(f"🧹 Pôster removido: {poster_path}")
            except Exception as e:
                logger.warning(f"⚠️ Falha ao remover pôster da série: {e}")

    series.deleted_at = datetime.utcnow()
    db.commit()
    logger.info(f"✅ Série marcada como deletada ID={series.id}")
    return series

def hard_delete(db: Session, series_id: int):
    series = db.query(models.Series).filter(models.Series.id == series_id).first()
    if not series:
        return None

    if series.poster:
        poster_path = os.path.join("app/static", series.poster)
        if os.path.exists(poster_path):
            try:
                os.remove(poster_path)
                logger.info(f"🧹 Pôster (hard delete) removido: {poster_path}")
            except Exception as e:
                logger.warning(f"⚠️ Falha ao remover pôster no hard delete: {e}")

    db.delete(series)
    db.commit()
    logger.info(f"🔥 Série removida permanentemente ID={series.id}")
    return series
