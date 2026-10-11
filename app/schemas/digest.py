from datetime import datetime

from pydantic import BaseModel, Field


class LLMSummaryOutput(BaseModel):
    """Strict schema that Ollama must return for each analyzed article."""

    summary: str = Field(description="A concise 2 to 3 sentence summary of the article.")
    key_takeaways: list[str] = Field(
        description="2 to 4 bullet points highlighting the core technical takeaways or facts."
    )
    category: str = Field(
        description="The primary domain category (e.g., 'Artificial Intelligence', 'Cloud & Infrastructure', 'DevOps', 'Cybersecurity', 'Software Engineering')."
    )
    impact_score: float = Field(
        ge=1.0,
        le=10.0,
        description="Relevance and importance score from 1.0 (trivial) to 10.0 (groundbreaking/critical).",
    )


class DigestResponse(BaseModel):
    """Schema returned by API endpoints when users view a curated digest."""

    id: int
    title: str
    digest_date: datetime
    intro: str | None
    articles: list[dict]

    class Config:
        from_attributes = True
