# AI Radar

An automated intelligence system that monitors technology news, deduplicates and extracts article content, enriches it via a local LLM (Ollama), and serves concise, high-impact digests via FastAPI.

## Tech Stack
- **Language:** Python 3.11+
- **Scraping / Ingestion:** BeautifulSoup4, Feedparser, HTTPX
- **Database:** PostgreSQL via SQLAlchemy ORM
- **AI / LLM:** Ollama (Local LLM)
- **API:** FastAPI
- **Tooling:** Docker, Docker Compose, Ruff, Pytest
