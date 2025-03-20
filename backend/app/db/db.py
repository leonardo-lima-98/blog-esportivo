# backend/app/db.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from backend.app.core.config import settings
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Criar engine do SQLAlchemy
try:
    engine = create_engine(
        settings.DATABASE_URL,
        echo=False,  # Definir como True para logs SQL
        pool_pre_ping=True,  # Verificar conexão antes de usar
        pool_recycle=3600  # Reciclar conexões a cada hora
    )
    logger.info("Conexão com banco de dados estabelecida")
except Exception as e:
    logger.error(f"Erro ao conectar ao banco de dados: {e}")
    raise

# Criar sessão
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para os modelos
Base = declarative_base()

# Função para obter sessão do banco
def get_db():
    """Provedor de dependência para obter uma sessão de banco de dados"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    """Inicializa o banco de dados e cria as tabelas"""
    from app.models import Base
    Base.metadata.create_all(bind=engine)
    logger.info("Tabelas criadas no banco de dados")