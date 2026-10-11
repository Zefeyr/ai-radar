from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.db.models.article import Article, ArticleStatus
from app.pipeline.runner import PipelineRunner
from app.schemas.article import ArticleResponse

router = APIRouter(prefix="/articles", tags=["Articles"])


def execute_full_pipeline(batch_size: int = 5) -> None:
    """Helper executed by FastAPI background workers."""
    runner = PipelineRunner()
    runner.run_ingestion()
    runner.run_ai_enrichment(batch_size=batch_size)
    runner.run_digest_generation()


@router.get("", response_model=list[ArticleResponse])
def list_articles(
    category: str | None = Query(None, description="Filter by AI category"),
    status: ArticleStatus | None = Query(
        None, description="Filter by status (PENDING, PROCESSED, FAILED)"
    ),
    min_score: float | None = Query(None, ge=1.0, le=10.0, description="Minimum impact score"),
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
):
    """Retrieves paginated list of ingested and processed articles."""
    query = db.query(Article)

    if category:
        query = query.filter(Article.category == category)
    if status:
        query = query.filter(Article.status == status)
    if min_score is not None:
        query = query.filter(Article.impact_score >= min_score)

    articles = query.order_by(Article.created_at.desc()).offset(offset).limit(limit).all()
    return articles


@router.get("/{article_id}", response_model=ArticleResponse)
def get_article(article_id: int, db: Session = Depends(get_db)):
    """Fetches a single article by ID."""
    article = db.query(Article).filter(Article.id == article_id).first()
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    return article


@router.post("/trigger-pipeline", status_code=202)
def trigger_pipeline(background_tasks: BackgroundTasks):
    """Triggers scraping, Ollama enrichment, and digest generation in the background."""
    background_tasks.add_task(execute_full_pipeline, batch_size=5)
    return {"message": "Pipeline run triggered in background."}
