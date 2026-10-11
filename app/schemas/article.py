from datetime import datetime

from pydantic import BaseModel, Field

from app.db.models.article import ArticleStatus


class ArticleIngest(BaseModel):
    """Schema representing raw data coming in from RSS or Web scrapers."""

    url: str
    title: str = Field(..., min_length=1, max_length=512)
    source: str = Field(..., min_length=1, max_length=100)
    published_at: datetime | None = None
    raw_content: str | None = None


class ArticleResponse(BaseModel):
    """Schema returned by FastAPI endpoints to API consumers."""

    id: int
    url: str
    title: str
    source: str
    published_at: datetime | None
    summary: str | None
    key_takeaways: list[str] | None
    category: str | None
    impact_score: float | None
    status: ArticleStatus
    created_at: datetime

    class Config:
        from_attributes = True  # Allows Pydantic to read SQLAlchemy ORM objects
