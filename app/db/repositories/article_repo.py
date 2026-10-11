from typing import Optional, List
from sqlalchemy.orm import Session
from app.db.models.article import Article, ArticleStatus
from app.schemas.article import ArticleIngest
from app.ingestion.normalizer import normalize_url, generate_url_hash


class ArticleRepository:
    def __init__(self, db: Session):
        self.db = db

    def exists_by_hash(self, url_hash: str) -> bool:
        """Fast index lookup to check if an article URL has already been saved."""
        return self.db.query(Article.id).filter(Article.url_hash == url_hash).first() is not None

    def create_if_not_exists(self, item: ArticleIngest) -> Optional[Article]:
        """
        Calculates the normalized hash, checks for duplicates,
        and saves the new article if unique.
        """
        normalized_url = normalize_url(item.url)
        url_hash = generate_url_hash(normalized_url)

        if self.exists_by_hash(url_hash):
            return None  # Duplicate detected; skip insertion

        article = Article(
            url=normalized_url,
            url_hash=url_hash,
            title=item.title.strip(),
            source=item.source.strip(),
            published_at=item.published_at,
            raw_content=item.raw_content,
            status=ArticleStatus.PENDING,
        )

        self.db.add(article)
        self.db.commit()
        self.db.refresh(article)
        return article

    def get_pending_articles(self, limit: int = 10) -> List[Article]:
        """Fetches articles awaiting AI summarization."""
        return (
            self.db.query(Article)
            .filter(Article.status == ArticleStatus.PENDING)
            .order_by(Article.created_at.asc())
            .limit(limit)
            .all()
        )

    def update_with_ai_results(
        self,
        article_id: int,
        summary: str,
        key_takeaways: List[str],
        category: str,
        impact_score: float,
    ) -> Optional[Article]:
        """Updates an article with Ollama's structured enrichment output."""
        article = self.db.query(Article).filter(Article.id == article_id).first()
        if not article:
            return None

        article.summary = summary
        article.key_takeaways = key_takeaways
        article.category = category
        article.impact_score = impact_score
        article.status = ArticleStatus.PROCESSED
        self.db.commit()
        self.db.refresh(article)
        return article

    def mark_as_failed(self, article_id: int, error_message: str) -> Optional[Article]:
        """Marks an article as failed if LLM or scraping encounters an unrecoverable error."""
        article = self.db.query(Article).filter(Article.id == article_id).first()
        if not article:
            return None

        article.status = ArticleStatus.FAILED
        article.error_message = error_message
        self.db.commit()
        self.db.refresh(article)
        return article
