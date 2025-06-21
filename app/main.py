from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
import logging
from fastapi.staticfiles import StaticFiles
import os

# —— CONFIGURAÇÃO GLOBAL DO LOGGER ———————————————————————
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s - %(message)s"
)
logger = logging.getLogger("cinepetro")
logger.info("🚀 Iniciando a API CinePetro...")

# —— IMPORTAÇÃO DOS ROUTERS DA APLICAÇÃO ——————————————————
from app.modules.user.router import router as users_router
from app.modules.auth.router import router as auth_router
from app.modules.genres.router import router as genres_router
from app.modules.movies.router import router as movies_router
from app.modules.series.router import router as series_router
from app.modules.episodes.router import router as episodes_router
from app.modules.serie_genre.router import router as serie_genero_router
from app.modules.WhatchProgress.router import router as watch_progress_router  # ✅ NOVO

# —— GARANTIR QUE TODAS AS MODELS SEJAM REGISTRADAS ————————
# Isso evita o erro de relacionamento não resolvido (WatchProgress)
import app.modules.user.models
import app.modules.movies.models
import app.modules.episodes.models
import app.modules.WhatchProgress.Models  # ✅ NOVO

# —— INSTÂNCIA DO APP FASTAPI ————————————————————————————————
app = FastAPI(
    title="🎬 CinePetro API",
    version="1.0.0",
    description="API oficial do sistema CinePetro para gerenciamento de filmes, séries e episódios.",
    openapi_tags=[
        {"name": "Auth", "description": "Autenticação e login de usuários"},
        {"name": "Users", "description": "Cadastro e gerenciamento de usuários"},
        {"name": "Movies", "description": "Cadastro e consulta de filmes"},
        {"name": "Series", "description": "Cadastro e consulta de séries"},
        {"name": "Episodes", "description": "Cadastro e consulta de episódios"},
        {"name": "Genres", "description": "Gerenciamento de gêneros"},
        {"name": "SerieGenre", "description": "Associação entre séries e gêneros"},
        {"name": "WatchProgress", "description": "Progresso de visualização de filmes e episódios"},  # ✅ NOVO
        {"name": "Health", "description": "Verificação de status da API"},
    ]
)

# —— MIDDLEWARE DE CORS ——————————————————————————————————————
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Em produção, restrinja os domínios confiáveis
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# —— INCLUSÃO DOS ROUTERS —————————————————————————————————————
app.include_router(auth_router, tags=["Auth"])
app.include_router(users_router, tags=["Users"])
app.include_router(genres_router, tags=["Genres"])
app.include_router(movies_router, tags=["Movies"])
app.include_router(series_router, tags=["Series"])
app.include_router(episodes_router, tags=["Episodes"])
app.include_router(serie_genero_router, tags=["SerieGenre"])
app.include_router(watch_progress_router, tags=["WatchProgress"])  # ✅ NOVO

# —— ROTAS DE SAÚDE ————————————————————————————————————————————
@app.get("/", tags=["Health"])
def root():
    logger.info("🔍 Acessando a rota raiz '/'")
    return {"msg": "🎬 CinePetro API is online!"}

@app.get("/health", tags=["Health"])
def health_check():
    logger.info("📈 Health check realizado")
    return {"status": "ok", "message": "API CinePetro está no ar!"}

# —— PERSONALIZAÇÃO DO OPENAPI PARA JWT ————————————————————
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )

    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        }
    }

    for path in openapi_schema["paths"].values():
        for operation in path.values():
            operation.setdefault("security", []).append({"BearerAuth": []})

    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

logger.info("✅ CinePetro API carregada com sucesso.")

# 📦 Servir arquivos estáticos (como pôsteres de filmes)
app.mount(
    "/static",
    StaticFiles(directory=os.path.join("app", "static")),
    name="static"
)
app.mount(
    "/static/series",
    StaticFiles(directory=os.path.join("app", "static", "series")),
    name="series"
)
