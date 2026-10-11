from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Table
from sqlalchemy.orm import relationship
from app.core.database import Base

# Association table: Many-to-Many relationship between Digests and Articles
digest_articles = Table(
    "digest_articles",
    Base.metadata,
    Column("digest_id", Integer, ForeignKey("digests.id", ondelete="CASCADE"), primary_key=True),
    Column("article_id", Integer, ForeignKey("articles.id", ondelete="CASCADE"), primary_key=True),
)


class Digest(Base):
    __tablename__ = "digests"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)  # e.g. "AI Radar Daily - 2026-10-09"
    digest_date = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    intro = Column(Text, nullable=True)  # Optional editorial intro or LLM-generated macro summary
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationship to fetch all articles included in this digest
    articles = relationship("Article", secondary=digest_articles, backref="digests")
