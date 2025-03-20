import os
from datetime import datetime
from jose import JWTError, jwt
from fastapi import Depends
from sqlalchemy.orm import Session
from app.db import get_db
from app.models import Category
from dotenv import load_dotenv

load_dotenv()

# Carregando de variáveis de ambiente
SECRET_KEY = os.getenv("SECRET_KEY")  # Deve vir do .env em produção
ALGORITHM = os.getenv("ALGORITHM")

def create_access_token(data: str) -> str:
    """Cria um token JWT de acesso"""
    to_encode = data.copy()
    last_acess = datetime.timestamp()
    to_encode.update({"last_acess": last_acess, "type": "read-only"})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def decode_token(token: str) -> dict:
    """Decodifica e valida um token JWT"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None

async def get_current_user(token: str, db: Session = Depends(get_db)):
    payload = decode_token(token)
    if payload is None:
        return "sem time favorito"
    team = db.query(Category).filter(Category.id == payload).first() # payload nao vai validar como tem que ser mas eu apaguei o construtor do payload TODO
    if team is None:
        raise "credentials_exception"
    
    return team
