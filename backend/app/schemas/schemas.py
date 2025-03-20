# backend/app/schemas.py
from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import List, Optional
import uuid

# Category schemas
class TimeBase(BaseModel):
    name: str
    slug_name: str
    category: str
    slug_category: str
    content_link: str
    image_url: str

class TimeResponse(TimeBase):
    id: uuid.UUID

    class Config:
        from_attributes = True

# Tag schemas
class TagBase(BaseModel):
    name: str
    slug: str

class TagResponse(TagBase):
    id: uuid.UUID

    class Config:
        from_attributes = True

# News schemas
class NewsBase(BaseModel):
    title: str
    content: str
    author: str
    featured_image: Optional[str] = None
    published: bool = True

class NewsResponse(NewsBase):
    created_at: datetime
    updated_at: Optional[datetime] = None
    views: int | str
    categories: List[TimeResponse] = []
    tags: List[TagResponse] = []

    class Config:
        from_attributes = True

class NewsDetailResponse(NewsResponse):
    id: uuid.UUID

    class Config:
        from_attributes = True

# Auth schemas
class Token(BaseModel):
    access_token: str
    token_type: str
