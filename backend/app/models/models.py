# backend/app/models.py
from sqlalchemy import Column, String, Text, DateTime, ForeignKey, Table, Boolean, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

Base = declarative_base()

# Tabela de relacionamento entre notícias e times
news_categories = Table(
    "news_categories",
    Base.metadata,
    Column("news_id", UUID(as_uuid=True), ForeignKey("news.id")),
    Column("time_id", UUID(as_uuid=True), ForeignKey("teams.id"))
)

# Tabela de relacionamento entre notícias e tags
news_tags = Table(
    "news_tags",
    Base.metadata,
    Column("news_id", UUID(as_uuid=True), ForeignKey("news.id")),
    Column("tag_id", UUID(as_uuid=True), ForeignKey("tags.id"))
)

class News(Base):
    __tablename__ = "news"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    author = Column(String(100), nullable=False)
    featured_image = Column(String(255), nullable=True)  # URL da imagem
    published = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.timestamp)
    updated_at = Column(DateTime, onupdate=datetime.timestamp)
    views = Column(Integer, default=0)
    slug = Column(String(255), unique=True, nullable=True)
    
    # Relacionamentos
    teams = relationship("Time", secondary=news_categories, back_populates="news")
    tags = relationship("Tag", secondary=news_tags, back_populates="news")

class Time(Base):
    __tablename__ = "teams"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    name = Column(String(50), unique=True, nullable=False)
    slug_name = Column(String(50), unique=True, nullable=False)
    category = Column(String(50), nullable=False)
    slug_category = Column(String(50), nullable=False)
    content_link = Column(String(550), nullable=False)
    image_url = Column(String(550), nullable=True)
    
    # Relacionamentos
    news = relationship("News", secondary=news_categories, back_populates="teams")

class Tag(Base):
    __tablename__ = "tags"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    name = Column(String(50), unique=True, nullable=False)
    slug = Column(String(50), unique=True, nullable=False)
    description = Column(String(150), nullable=True)
    
    # Relacionamentos
    news = relationship("News", secondary=news_tags, back_populates="tags")

