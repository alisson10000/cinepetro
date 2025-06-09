from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base  # ✅ Corrigido: import oficial para SQLAlchemy ≥2.0
from sqlalchemy.orm import sessionmaker

# ==========================================
# 🔧 CONFIGURAÇÃO DE CONEXÃO COM O BANCO DE DADOS
# ==========================================

# 🔑 String de conexão (substitua se necessário)
SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:@localhost:3306/cinepetro"

# 🔌 Cria o engine, que gerencia a conexão com o banco
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_pre_ping=True  # ✅ Mantém a conexão viva automaticamente (útil em MySQL/MariaDB)
)

# 💼 Cria a fábrica de sessões (SessionLocal será usado para gerar sessões de banco nas rotas)
SessionLocal = sessionmaker(
    autocommit=False,  # ✅ O commit deve ser manual (mais seguro)
    autoflush=False,   # ✅ O flush automático é desativado para evitar gravações acidentais
    bind=engine        # 🔗 Conecta à engine configurada acima
)

# 📦 Base declarativa para modelos ORM
# Todos os modelos do SQLAlchemy devem herdar dela
Base = declarative_base()

# ==========================================
# 📦 GERENCIADOR DE SESSÃO (DEPENDÊNCIA PARA FASTAPI/FLASK)
# ==========================================
def get_db():
    """
    Fornece uma sessão de banco de dados para cada request.
    Ele abre a sessão, entrega via yield e garante o fechamento no final.
    Ideal para usar como dependência em FastAPI, Flask, etc.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
