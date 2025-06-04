"""
Pydantic schemas for RSSify project.
"""
from pydantic import BaseModel, HttpUrl, Field, validator, field_validator
from typing import Optional, Any, List
from datetime import datetime

class SiteBase(BaseModel):
    """
    Базовая схема сайта для отображения и создания.
    name: Название сайта
    url: URL сайта (валидируется как HttpUrl)
    selector: CSS-селектор для поиска постов
    description: Описание сайта (опционально)
    is_active: Флаг активности сайта
    """
    name: str = Field(..., max_length=128)
    url: HttpUrl
    selector: str = Field(..., max_length=256)
    title_selector: Optional[str] = Field(None, max_length=256)
    desc_selector: Optional[str] = Field(None, max_length=256)
    link_selector: Optional[str] = Field(None, max_length=256)
    description: Optional[str] = None
    is_active: Optional[bool] = True
    check_interval: Optional[int] = 10  # Интервал проверки в минутах
    last_check: Optional[datetime] = None
    last_error: Optional[str] = None

    @field_validator("name")
    @classmethod
    def name_length(cls, v):
        if not (1 <= len(v) <= 128):
            raise ValueError("Name must be 1-128 characters long")
        return v

    @field_validator("selector")
    @classmethod
    def selector_length(cls, v):
        if not (1 <= len(v) <= 256):
            raise ValueError("Selector must be 1-256 characters long")
        return v

class SiteCreate(SiteBase):
    """
    Схема для создания нового сайта (наследует все поля SiteBase).
    """
    pass

class SiteUpdate(BaseModel):
    """
    Схема для обновления сайта. Все поля опциональны.
    name: Новое название сайта
    url: Новый URL сайта
    selector: Новый CSS-селектор
    description: Новое описание
    is_active: Новый флаг активности
    """
    name: Optional[str] = Field(None, max_length=128)
    url: Optional[HttpUrl] = None
    selector: Optional[str] = Field(None, max_length=256)
    title_selector: Optional[str] = Field(None, max_length=256)
    desc_selector: Optional[str] = Field(None, max_length=256)
    link_selector: Optional[str] = Field(None, max_length=256)
    description: Optional[str] = None
    is_active: Optional[bool] = None
    check_interval: Optional[int] = None

class PostBase(BaseModel):
    """
    Базовая схема поста для отображения и создания.
    title: Заголовок поста
    description: Описание поста (опционально)
    url: URL поста
    content_hash: Хеш содержимого (для дедупликации, опционально)
    published_at: Дата публикации (опционально)
    """
    title: str = Field(..., max_length=256)
    description: Optional[str] = None
    url: HttpUrl
    content_hash: Optional[str] = None
    published_at: Optional[datetime] = None

    @field_validator("title")
    @classmethod
    def title_length(cls, v):
        if not (1 <= len(v) <= 256):
            raise ValueError("Title must be 1-256 characters long")
        return v

class Post(PostBase):
    """
    Схема для возврата поста из БД (включает id, site_id, created_at).
    id: Идентификатор поста
    site_id: Идентификатор сайта
    created_at: Дата создания записи
    """
    id: int
    site_id: int
    created_at: datetime

    class Config:
        orm_mode = True

class SiteWithPosts(SiteBase):
    """
    Схема сайта с вложенными постами (для вложенного отображения).
    posts: Список постов, связанных с сайтом
    """
    id: int
    posts: List[Post] = []

    class Config:
        orm_mode = True
