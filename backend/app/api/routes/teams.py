# backend/app/routes/teams.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db import get_db
from app.models import Time
from app.schemas import TimeResponse

router = APIRouter(prefix="/teams", tags=["Times"])

@router.get("/", response_model=List[TimeResponse])
def get_categories(db: Session = Depends(get_db)):
    return db.query(Time).all()


@router.get("/{slug_name}", response_model=TimeResponse)
def filter_by_slug_name(slug_name: str, db: Session = Depends(get_db)):
    slug_name = db.query(Time).filter(Time.slug_name == slug_name).first()
    if not slug_name:
        raise HTTPException(status_code=404, detail="Time não encontrado")
    return slug_name


@router.get("/regiao/{slug_sub_Time}", response_model=List[TimeResponse])
def filter_by_slug_sub_Time(slug_sub_Time: str, db: Session = Depends(get_db)):
    slug_sub_Time = db.query(Time).filter(Time.slug_sub_Time == slug_sub_Time).all()

    if not slug_sub_Time:
        raise HTTPException(status_code=404, detail="Região não encontrada")
    return slug_sub_Time