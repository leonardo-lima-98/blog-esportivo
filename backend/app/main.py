# backend/app/main.py

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.routes import news, tags
import time

from backend.app.routes import teams

app = FastAPI(
    title="Blog Esportivo API",
    description="API para o blog esportivo com notícias, categorias, tags e sistema de usuários",
    version="0.1.0"
)

# Configuração de CORS
origins = [
    "http://localhost:3000",  # Frontend Next.js
    "http://localhost:8000",  # Desenvolvimento local
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Middleware para logging
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response

# Incluir todas as rotas
app.include_router(news.router)
app.include_router(teams.router)
app.include_router(tags.router)

@app.get("/")
def root():
    return {
        "message": "API do blog esportivo está rodando!",
        "docs": "/docs",
        "redoc": "/redoc"
    }

# Tratamento de exceções global
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"detail": "Erro interno do servidor"}
    )