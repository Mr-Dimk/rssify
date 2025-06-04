"""
SQLAlchemy models for RSSify project.
"""
from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, Index
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime

class Site(Base):
    __tablename__ = "sites"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(128), nullable=False)
    url = Column(String(512), nullable=False, unique=True)
    selector = Column(String(256), nullable=False)
    title_selector = Column(String(256), nullable=True)
    desc_selector = Column(String(256), nullable=True)
    link_selector = Column(String(256), nullable=True)
    description = Column(Text, nullable=True)
    is_active = Column(Integer, default=1)
    # Можно добавить другие поля: created_at, updated_at, etc.

    posts = relationship("Post", back_populates="site", cascade="all, delete-orphan")

    __table_args__ = (
        Index("ix_sites_url", "url"),
        Index("ix_sites_name", "name"),
    )

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    site_id = Column(Integer, ForeignKey("sites.id"), nullable=False, index=True)
    title = Column(String(256), nullable=False)
    description = Column(Text, nullable=True)
    url = Column(String(512), nullable=False)
    content_hash = Column(String(64), nullable=True, index=True)
    published_at = Column(DateTime, default=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)

    site = relationship("Site", back_populates="posts")

    __table_args__ = (
        Index("ix_posts_site_id", "site_id"),
        Index("ix_posts_content_hash", "content_hash"),
        Index("ix_posts_url", "url"),
    )
