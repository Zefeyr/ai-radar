from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.db.repositories.digest_repo import DigestRepository
from app.schemas.article import ArticleResponse
from pydantic import BaseModel
from datetime import datetime

router = APIRouter(prefix="/digests", tags=["Digests"])


class DigestDetailResponse(BaseModel):
    id: int
    title: str
    digest_date: datetime
    intro: str | None = None
    articles: List[ArticleResponse]

    class Config:
        from_attributes = True


@router.get("/latest", response_model=DigestDetailResponse)
def get_latest_digest(db: Session = Depends(get_db)):
    """Retrieves the most recent daily digest with all its top articles."""
    repo = DigestRepository(db)
    digest = repo.get_latest_digest()
    if not digest:
        raise HTTPException(status_code=404, detail="No digest generated yet")
    return digest
