from datetime import datetime

from sqlalchemy.orm import Session

from app.db.models.article import Article, ArticleStatus
from app.db.models.digest import Digest


class DigestRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_top_articles_for_digest(self, min_score: float = 7.0, limit: int = 10) -> list[Article]:
        """Fetches the highest-impact processed articles that have not yet been assigned to a digest."""
        return (
            self.db.query(Article)
            .filter(
                Article.status == ArticleStatus.PROCESSED,
                Article.impact_score >= min_score,
            )
            .order_by(Article.impact_score.desc(), Article.published_at.desc())
            .limit(limit)
            .all()
        )

    def create_digest(
        self, title: str, articles: list[Article], intro: str | None = None
    ) -> Digest:
        """Creates a new Digest and associates the selected high-impact articles."""
        digest = Digest(
            title=title,
            digest_date=datetime.utcnow(),
            intro=intro,
        )
        digest.articles.extend(articles)
        self.db.add(digest)
        self.db.commit()
        self.db.refresh(digest)
        return digest

    def get_latest_digest(self) -> Digest | None:
        """Retrieves the most recent digest."""
        return self.db.query(Digest).order_by(Digest.digest_date.desc()).first()
