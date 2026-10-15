# 📡 AI Radar

[![CI Pipeline](https://github.com/Zefeyr/ai-radar/actions/workflows/ci.yml/badge.svg)](https://github.com/Zefeyr/ai-radar/actions)
[![Python Version](https://img.shields.io/badge/python-3.11%2B-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100%2B-009688.svg?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![Docker](https://img.shields.io/badge/Docker-Enabled-2496ED.svg?logo=docker&logoColor=white)](https://www.docker.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

An automated AI-powered news radar and intelligence curation service. **AI Radar** aggregates tech articles, processes and categorizes content using locally hosted LLM inference via Ollama, and serves structured intelligence digests through an asynchronous REST API backed by PostgreSQL.

---

## 🎯 Architecture Overview

```text
                      +-----------------------------+
                      |   Sources (HN, Feeds, etc.) |
                      +--------------+--------------+
                                     |
                                     v
                           [ Ingestion Engine ]
                                     |
           +-------------------------+-------------------------+
           |                                                   |
           v                                                   v
+-----------------------+                           +--------------------+
| Local LLM (Ollama)    |                           | PostgreSQL DB      |
| Summarization / Tags  |                           | SQLAlchemy/Alembic |
+-----------+-----------+                           +---------+----------+
            |                                                 |
            +------------------------+------------------------+
                                     |
                                     v
                        +-------------------------+
                        |   FastAPI REST Engine   |
                        +------------+------------+
                                     |
                                     v
                          Client / API Consumer
```

### Key Technical Capabilities
* **Asynchronous Web API:** High-throughput endpoints built with FastAPI and Pydantic validation schemas.
* **Database & Migrations:** PostgreSQL persistence with SQLAlchemy ORM and structured Alembic database migrations.
* **Local Inference Pipeline:** Isolated containerized Ollama integration for on-premise/local LLM summarization without recurring third-party API costs.
* **Automated CI/CD:** Continuous Integration workflow leveraging GitHub Actions, automated service containers, migration runs, and Pytest coverage checks.

---

## 🛠 Tech Stack

| Domain | Technology / Tool |
| :--- | :--- |
| **Backend Framework** | Python 3.11+, FastAPI, Pydantic (v2) |
| **Database & ORM** | PostgreSQL 15+, SQLAlchemy, Alembic |
| **LLM Inference** | Ollama (Local LLM Execution) |
| **Testing & Mocking** | Pytest, Pytest-Asyncio, HTTPX, Mockito / Unittest Mock |
| **Containerization** | Docker, Docker Compose |
| **CI / Automation** | GitHub Actions |

---

## 🚀 Getting Started

### Prerequisites
* [Docker Desktop](https://www.docker.com/) & Docker Compose
* [Python 3.11+](https://www.python.org/)
* [Git](https://git-scm.com/)

### 1. Clone the Repository
```bash
git clone https://github.com/Zefeyr/ai-radar.git
cd ai-radar
```

### 2. Environment Configuration
Copy the template `.env.example` file to create your local `.env`:

```bash
cp .env.example .env
```

Configure your local credentials in `.env`:
```ini
# Application
ENVIRONMENT=development
PORT=8000

# Database
DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/ai_radar_db

# Ollama LLM
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=mistral
```

### 3. Run with Docker Compose (Recommended)
Boot the entire system including the FastAPI application, PostgreSQL database, and Ollama:

```bash
docker compose up --build -d
```

Pull your target model inside the Ollama container:
```bash
docker compose exec ollama ollama pull mistral
```

Access the interactive API documentation at `http://localhost:8000/docs`.

---

## 🧪 Local Development & Database Migrations

### Virtual Environment Setup
```bash
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate
pip install -r requirements.txt
```

### Database Migrations
Run database schema upgrades using Alembic:
```bash
# Apply pending migrations
alembic upgrade head

# Generate a new migration revision
alembic revision --autogenerate -m "describe_schema_change"
```

---

## 🔄 Continuous Integration (CI) Workflow

The project implements a zero-trust automated CI pipeline configured in `.github/workflows/ci.yml`. On every Pull Request and Push to `main`, the CI runner executes:

1. **Linting & Code Quality:** Formats and checks code standards with `ruff` and `black`.
2. **Service Spin-Up:** Spins up an ephemeral PostgreSQL database container directly in the GitHub Actions runner environment.
3. **Migration Verification:** Executes `alembic upgrade head` against the live test database to prevent schema drift and migration rollback errors.
4. **Automated Testing:**
   * Runs the full `pytest` suite with `pytest-asyncio`.
   * Leverages mock fixtures to simulate Ollama HTTP responses and external API endpoints to ensure deterministic, network-free test execution.
   * Generates test coverage reports.

```yaml
# Sample .github/workflows/ci.yml structure
name: CI Pipeline

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:15-alpine
        env:
          POSTGRES_DB: ai_radar_test
          POSTGRES_USER: test_user
          POSTGRES_PASSWORD: test_password
        ports:
          - 5432:5432
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5

    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"
          cache: "pip"

      - name: Install Dependencies
        run: |
          pip install --upgrade pip
          pip install -r requirements.txt
          pip install -r requirements-dev.txt

      - name: Run Schema Migrations
        env:
          DATABASE_URL: postgresql+asyncpg://test_user:test_password@localhost:5432/ai_radar_test
        run: |
          alembic upgrade head

      - name: Execute Tests with Pytest
        env:
          DATABASE_URL: postgresql+asyncpg://test_user:test_password@localhost:5432/ai_radar_test
          OLLAMA_BASE_URL: http://mock-ollama:11434
        run: |
          pytest -v --cov=app --cov-report=term-missing
```

---

## 📂 Project Structure

```text
ai-radar/
├── .github/
│   └── workflows/
│       └── ci.yml               # Automated CI pipeline (lint, test, migration)
├── alembic/                     # Database migrations
│   ├── versions/
│   └── env.py
├── app/
│   ├── api/                     # Route controllers & endpoints
│   ├── core/                    # App configuration, logging, and security
│   ├── models/                  # SQLAlchemy ORM database models
│   ├── schemas/                 # Pydantic schemas (request/response)
│   ├── services/                # Business logic (Ollama, scrapers, analyzers)
│   └── main.py                  # FastAPI application entrypoint
├── tests/                       # Pytest test suite & mock fixtures
│   ├── conftest.py
│   └── test_api.py
├── Dockerfile                   # App container specification
├── docker-compose.yml           # Multi-container orchestration (App, DB, Ollama)
├── alembic.ini                  # Alembic CLI config
└── requirements.txt             # Python dependencies
```

---

## 📄 License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
