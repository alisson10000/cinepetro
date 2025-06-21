import os
import re
import logging
from datetime import datetime
from sqlalchemy.orm import Session, joinedload

from . import models, schemas
from app.modules.genres.models import Genre

logger = logging.getLogger("cinepetro.series.services")

# 📁 Caminho onde os pôsteres serão salvos
POSTER_FOLDER = "app/static/series"
POSTER_URL_PREFIX = "series/"

# 🔐 Proteção contra nomes maliciosos
def sanitize_filename(filename: str) -> str:
    return re.sub(r'[^a-zA-Z0-9_.-]', '_', filename)

# 💾 Função para salvar arquivo de imagem
def save_poster(poster_file) -> str:
    try:
        os.makedirs(POSTER_FOLDER, exist_ok=True)
        filename = f"{datetime.utcnow().timestamp()}_{sanitize_filename(poster_file.filename)}"
        poster_path = os.path.join(POSTER_FOLDER, filename)

        with open(poster_path, "wb") as f:
            f.write(poster_file.file.read())

        logger.info(f"💾 Pôster salvo com sucesso: {poster_path}")
        return f"{POSTER_URL_PREFIX}{filename}"
    except Exception as e:
        logger.error(f"❌ Falha ao salvar pôster: {e}")
        return ""

# 🔍 Busca série por ID com gêneros
def get_by_id(db: Session, series_id: int):
    logger.info(f"🔍 Buscando série ID={series_id}")
    return db.query(models.Series)\
        .options(joinedload(models.Series.genres))\
        .filter(models.Series.id == series_id)\
        .first()

# 📋 Lista todas as séries
def get_all(db: Session):
    logger.info("📋 Listando todas as séries")
    return db.query(models.Series)\
        .options(joinedload(models.Series.genres))\
        .all()

# ➕ Criação de nova série
def create(db: Session, data: schemas.SeriesCreate, user_id: int):
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
    logger.info(f"✅ Série criada com sucesso ID={db_series.id}")
    return db_series

# 🔁 Atualização parcial via JSON
def update(db: Session, series_id: int, data: schemas.SeriesUpdate):
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

# 📤 Atualização com upload de pôster (via FormData)
def update_with_upload(db: Session, series_id: int, data: schemas.SeriesCreate):
    logger.info(f"📤 Atualizando série com upload ID={series_id}")
    series = get_by_id(db, series_id)
    if not series:
        logger.warning(f"❌ Série não encontrada ID={series_id}")
        return None

    series.title = data.title
    series.description = data.description
    series.start_year = data.start_year
    series.end_year = data.end_year

    if data.genre_ids:
        logger.info(f"🎭 Atualizando gêneros: {data.genre_ids}")
        series.genres = db.query(Genre).filter(Genre.id.in_(data.genre_ids)).all()

    if data.poster:
        if series.poster:
            old_path = os.path.join("app/static", series.poster)
            if os.path.exists(old_path):
                try:
                    os.remove(old_path)
                    logger.info(f"🧹 Pôster antigo removido: {old_path}")
                except Exception as e:
                    logger.warning(f"⚠️ Falha ao remover pôster antigo: {e}")
        new_poster = save_poster(data.poster)
        series.poster = new_poster

    db.commit()
    db.refresh(series)
    logger.info(f"✅ Série atualizada com sucesso ID={series.id}")
    return series

# ❌ Exclusão única (real)
def delete(db: Session, series_id: int):
    logger.info(f"🗑️ Deletando série ID={series_id}")
    series = get_by_id(db, series_id)
    if not series:
        logger.warning(f"❌ Série não encontrada ID={series_id}")
        return None

    if series.poster:
        poster_path = os.path.join("app/static", series.poster)
        if os.path.exists(poster_path):
            try:
                os.remove(poster_path)
                logger.info(f"🧨 Pôster removido: {poster_path}")
            except Exception as e:
                logger.warning(f"⚠️ Erro ao remover pôster: {e}")

    db.delete(series)
    db.commit()
    logger.info(f"✅ Série removida permanentemente ID={series.id}")
    return series
