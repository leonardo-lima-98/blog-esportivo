# backend/app/routes/tags.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.db import get_db
from app.models import Tag
from app.schemas import TagResponse

router = APIRouter(prefix="/tags", tags=["Tags"])

@router.get("/", response_model=List[TagResponse])
def get_tags(db: Session = Depends(get_db)):
    """
    Recupera todas as tags
    """
    return db.query(Tag).all()

@router.get("/{tag_slug}", response_model=List[TagResponse])
def get_tag(tag_slug: str, db: Session = Depends(get_db)):
    """
    Recupera uma tag pelo ID
    """
    tag = db.query(Tag).filter(Tag.slug == tag_slug).all()
    if not tag:
        raise HTTPException(status_code=404, detail="Tag não encontrada")
    return tag