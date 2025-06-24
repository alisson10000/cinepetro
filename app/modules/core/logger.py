# app/core/logger.py

import logging
from logging.handlers import RotatingFileHandler
import os

# Cria o diretório de logs se ainda não existir
LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

# Caminho do arquivo de log
LOG_FILE = os.path.join(LOG_DIR, "cinepetro.log")

# Handler com rotação: 5MB por arquivo, até 5 backups
file_handler = RotatingFileHandler(
    LOG_FILE, maxBytes=5 * 1024 * 1024, backupCount=5, encoding='utf-8'
)
file_handler.setLevel(logging.INFO)

# Formato do log
formatter = logging.Formatter(
    "%(asctime)s [%(levelname)s] %(name)s - %(message)s"
)
file_handler.setFormatter(formatter)

# Logger principal do projeto
logger = logging.getLogger("cinepetro")
logger.setLevel(logging.INFO)
logger.addHandler(file_handler)
logger.propagate = False  # Evita duplicação
