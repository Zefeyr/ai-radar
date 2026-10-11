from datetime import datetime
from enum import StrEnum

from sqlalchemy import (
    JSON,
    Column,
    DateTime,
    Float,
    Integer,
    String,
    Text,
)
from sqlalchemy import (
    Enum as SQLEnum,
)

from app.core.database import Base


class ArticleStatus(StrEnum):
    PENDING = "PENDING"  # Collected, but not yet analyzed by LLM
    PROCESSED = "PROCESSED"  # Successfully summarized and scored
    FAILED = "FAILED"  # Error encountered during scraping/LLM call


class Article(Base):
    __tablename__ = "articles"

    id = Column(Integer, primary_key=True, index=True)

    # Ingestion & Deduplication
    url = Column(String(2048), nullable=False)
    # SHA-256 hash of normalized URL (64 hex characters)
    # unique=True guarantees the database rejects identical links automatically
    url_hash = Column(String(64), unique=True, index=True, nullable=False)
    title = Column(String(512), nullable=False)
    source = Column(String(100), nullable=False, index=True)  # e.g. "OpenAI Blog", "Hacker News"
    published_at = Column(DateTime, nullable=True)
    raw_content = Column(Text, nullable=True)  # Scraped full text / snippet

    # Enrichment from Ollama
    summary = Column(Text, nullable=True)
    key_takeaways = Column(JSON, nullable=True)  # Stored as a JSON array of strings
    category = Column(String(100), nullable=True, index=True)  # e.g. "AI Models", "DevOps"
    impact_score = Column(Float, nullable=True, index=True)  # e.g. 8.5 / 10.0

    # Lifecycle & Metadata
    status = Column(
        SQLEnum(ArticleStatus),
        default=ArticleStatus.PENDING,
        nullable=False,
        index=True,
    )
    error_message = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )
