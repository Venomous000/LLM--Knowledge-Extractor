
# Jouster — LLM Knowledge Extractor (FastAPI + SQLite)

A small, production‑ready prototype that ingests unstructured text and returns:
- a **1–2 sentence summary** (via LLM or a robust local fallback),
- **structured metadata** (JSON): `title`, `topics` (3), `sentiment` (positive/neutral/negative),
- **keywords** (the 3 most frequent nouns — implemented locally, *not via the LLM*),
- **confidence score** (naive heuristic).

It exposes a clean API:
- `POST /analyze` → analyze & persist a text
- `POST /analyze/batch` → analyze multiple texts at once (bonus)
- `GET /search?topic=xyz` → search by topic/keyword

The system is modular, readable, and resilient to edge cases (empty input, LLM failures).

## Demo
- Once running, open: `http://127.0.0.1:8000/docs` for an interactive Swagger UI.

## Features
- Summary via OpenAI (if key present) or local fallback.
- NLTK noun-frequency keywords (not via LLM).
- Sentiment via lexicon heuristic.
- SQLite persistence via SQLAlchemy.
- Batch endpoint and tests.

## Local Setup
```bash
unzip jouster-llm-knowledge-extractor.zip
cd jouster-llm-knowledge-extractor
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env  # optionally set OPENAI_API_KEY
uvicorn app.main:app --reload
```
Open http://127.0.0.1:8000/docs

## Tests
```bash
pytest -q
```

## Docker
```bash
docker build -t jouster-llm-extractor .
docker run -p 8000:8000 --env-file .env -v $(pwd)/data:/app/data jouster-llm-extractor
```

## Design Choices
FastAPI+SQLite for speed and reliability; layered modules for clarity; LLM wrapper with graceful fallback; NLTK for nouns; simple confidence heuristic.

## SOPs Mapping (Selected)
- Readme features & assumptions, demo via Swagger, local setup, tests, env file.
- Git: incremental commits, branch naming, squash merge suggested.
- Code quality: modular, validations, readability, extensibility.
