from fastapi import FastAPI, Request, APIRouter, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import logging
import os

# 🚀 Logger
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s - %(message)s"
)
logger = logging.getLogger("cinepetro")
logger.info("🚀 Iniciando a API CinePetro...")

# 📦 Importação dos módulos da aplicação
from app.modules.user.router import router as users_router
from app.modules.auth.router import router as auth_router
from app.modules.genres.router import router as genres_router
from app.modules.movies.router import router as movies_router
from app.modules.series.router import router as series_router
from app.modules.episodes.router import router as episodes_router
from app.modules.serie_genre.router import router as serie_genero_router
from app.modules.WhatchProgress.router import router as watch_progress_router

# 🔁 Importação dos modelos
import app.modules.user.models
import app.modules.movies.models
import app.modules.episodes.models
import app.modules.WhatchProgress.Models

# 🎬 Instância da API
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
        {"name": "WatchProgress", "description": "Progresso de visualização de filmes e episódios"},
        {"name": "Health", "description": "Verificação de status da API"},
    ]
)

# 🌐 CORS Totalmente Livre
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 🔌 Inclusão dos routers
app.include_router(auth_router, tags=["Auth"])
app.include_router(users_router, tags=["Users"])
app.include_router(genres_router, tags=["Genres"])
app.include_router(movies_router, tags=["Movies"])
app.include_router(series_router, tags=["Series"])
app.include_router(episodes_router, tags=["Episodes"])
app.include_router(serie_genero_router, tags=["SerieGenre"])
app.include_router(watch_progress_router, tags=["WatchProgress"])

# ✅ Healthcheck
@app.get("/", tags=["Health"])
def root():
    logger.info("🔍 Acessando '/'")
    return {"msg": "🎬 CinePetro API is online!"}

@app.get("/health", tags=["Health"])
def health_check():
    logger.info("📈 Health check OK")
    return {"status": "ok", "message": "API CinePetro está no ar!"}

# 🔐 JWT no Swagger
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )

    schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT"
        }
    }

    for path in schema["paths"].values():
        for operation in path.values():
            operation.setdefault("security", []).append({"BearerAuth": []})

    app.openapi_schema = schema
    return app.openapi_schema

app.openapi = custom_openapi

# 📁 Diretório base para arquivos estáticos
static_base = os.path.join("app", "static")

# 🎞️ Servir vídeos com CORS totalmente livre
video_router = APIRouter()

@video_router.get("/static/videos/{filename}", tags=["Movies"])
async def serve_video_with_cors(filename: str, request: Request):
    video_path = os.path.join(static_base, "videos", filename)

    if not os.path.exists(video_path):
        raise HTTPException(status_code=404, detail="Arquivo de vídeo não encontrado.")

    response = FileResponse(video_path, media_type="video/mp4")
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Cross-Origin-Resource-Policy"] = "cross-origin"
    return response

# 🎞️ Servir episódios organizados por série e temporada
@video_router.get("/static/videos_series/{serie_id}/{season_number}/{episode_id}.mp4", tags=["Episodes"])
async def serve_episode_video(serie_id: int, season_number: int, episode_id: int, request: Request):
    episode_path = os.path.join(static_base, "videos_series", str(serie_id), str(season_number), f"{episode_id}.mp4")

    if not os.path.exists(episode_path):
        raise HTTPException(status_code=404, detail="Episódio não encontrado.")

    response = FileResponse(episode_path, media_type="video/mp4")
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Cross-Origin-Resource-Policy"] = "cross-origin"
    return response

app.include_router(video_router)

# 📁 Demais arquivos estáticos (sem CORS especial)
app.mount("/static/series", StaticFiles(directory=os.path.join(static_base, "series")), name="series")
app.mount("/static/subtitles", StaticFiles(directory=os.path.join(static_base, "subtitles")), name="subtitles")
app.mount("/static/posters", StaticFiles(directory=os.path.join(static_base, "posters")), name="posters")

logger.info("✅ CinePetro API carregada com sucesso.")
