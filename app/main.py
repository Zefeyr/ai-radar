from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.articles import router as articles_router
from app.api.v1.digests import router as digests_router

app = FastAPI(
    title="AI Radar API",
    version="1.0.0",
    description="Automated Tech Intelligence & Daily News Aggregator with Ollama",
)

# Allow cross-origin requests (for any local frontend development)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routes
app.include_router(articles_router, prefix="/api/v1")
app.include_router(digests_router, prefix="/api/v1")


@app.get("/health", tags=["Health"])
def health_check():
    """Liveness probe for monitoring and container health checks."""
    return {"status": "ok", "service": "ai-radar"}
