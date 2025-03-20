# backend/app/routes/news.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from typing import List, Optional
from app.db import get_db
from app.models import News, Time, Tag
from app.schemas import (NewsResponse, NewsDetailResponse)

router = APIRouter(prefix="/news", tags=["News"])

@router.get("/", response_model=List[NewsResponse])
def get_news(
    skip: int = 0, 
    limit: int = 10, 
    category: Optional[str] = None,
    tag: Optional[str] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    Recupera uma lista de notícias com filtros opcionais
    """
    query = db.query(News).filter(News.published == True)
    
    # Aplicar filtros se fornecidos
    if category:
        query = query.join(News.categories).filter(Time.slug == category)
    
    if tag:
        query = query.join(News.tags).filter(Tag.slug == tag)
    
    if search:
        query = query.filter(News.title.ilike(f"%{search}%") | News.content.ilike(f"%{search}%"))
    
    # Ordenar por mais recentes primeiro
    query = query.order_by(News.created_at.desc())
    
    # Paginação
    news = query.offset(skip).limit(limit).all()
    
    return news

@router.get("/{news_name}", response_model=NewsDetailResponse)
def get_news_detail(news_name: str, db: Session = Depends(get_db)):
    """
    Recupera detalhes de uma notícia específica
    """
    news = db.query(News).options(
        joinedload(News.categories),
        joinedload(News.tags)
    ).filter(News.name == news_name).first()
    
    if not news:
        raise HTTPException(status_code=404, detail="Notícia não encontrada")
    
    # Incrementar visualizações
    news.views += 1
    db.commit()
    
    return news
