# backend/app/config.py
import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

# Carregar variáveis do arquivo .env
load_dotenv(override=True)

class Settings(BaseSettings):
    """Configurações da aplicação"""
    # Banco de dados
    DATABASE_URL: str = os.getenv("DATABASE_URL")
    
    # Segurança
    SECRET_KEY: str = os.getenv("SECRET_KEY", "secret_key_for_development_only")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Aplicação
    PROJECT_NAME: str = "Blog Esportivo API"
    PROJECT_VERSION: str = "0.1.0"
    
    # CORS
    ALLOWED_ORIGINS: list = [
        "http://localhost:3000",  # Frontend Next.js
        "http://localhost:8000",  # Desenvolvimento local
    ]
    
    # Uploads
    UPLOAD_DIR: str = "uploads"
    
    class Config:
        case_sensitive = True

# Criar uma instância global das configurações
settings = Settings()