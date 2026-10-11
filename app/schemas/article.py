from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, HttpUrl, Field
from app.db.models.article import ArticleStatus


class ArticleIngest(BaseModel):
    """Schema representing raw data coming in from RSS or Web scrapers."""

    url: str
    title: str = Field(..., min_length=1, max_length=512)
    source: str = Field(..., min_length=1, max_length=100)
    published_at: Optional[datetime] = None
    raw_content: Optional[str] = None


class ArticleResponse(BaseModel):
    """Schema returned by FastAPI endpoints to API consumers."""

    id: int
    url: str
    title: str
    source: str
    published_at: Optional[datetime]
    summary: Optional[str]
    key_takeaways: Optional[List[str]]
    category: Optional[str]
    impact_score: Optional[float]
    status: ArticleStatus
    created_at: datetime

    class Config:
        from_attributes = True  # Allows Pydantic to read SQLAlchemy ORM objects
