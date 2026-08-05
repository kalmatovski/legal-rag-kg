# Legal RAG — Kyrgyz Republic Civil Code

A Retrieval-Augmented Generation (RAG) system that answers questions about the Civil Code of the Kyrgyz Republic (Part I) in natural language, grounded strictly in the actual text of the law.

Ask a question like:

> "Какой общий срок исковой давности?"

and get a plain-language answer with citations to the specific articles it's based on — not a hallucinated guess.

---

# How it works

## 1. Ingestion

Fetches the Civil Code's full text from the Kyrgyz Ministry of Justice's public API and collects metadata:

- document status
- keywords
- edition history

---

## 2. Parsing

Splits the raw HTML into **433 individual articles**, handling three different article-numbering formats found in the source:

```
244
82-1
233¹
```

The parser:

- strips amendment annotations from indexed text
- removes repealed clause text
- attaches chapter metadata to every article

---

## 3. Embedding

Indexes each article as a vector using:

```
gemini-embedding-001
```

Each document is stored in ChromaDB together with structured metadata:

- chapter
- article number
- repealed-clause flag

The system uses asymmetric retrieval:

```
RETRIEVAL_QUERY
```

for user questions and:

```
RETRIEVAL_DOCUMENT
```

for legal documents.

---

## 4. Retrieval

The user's question is embedded and used to search the vector database.

The system finds the most semantically relevant legal articles from ChromaDB.

---

## 5. Generation

Retrieved articles are passed to Gemini with a grounding prompt:

- answer only from the provided text
- cite article numbers
- do not hallucinate
- explicitly say when the answer is not present in the Code

---

# Tech stack

## Backend

- Python
- FastAPI
- Pydantic

## AI / LLM

- Gemini API
- `gemini-embedding-001` for embeddings
- `gemini-2.5-flash` for generation

## Vector store

- ChromaDB

## Data source

- Kyrgyz Republic Ministry of Justice public API

`cbd.minjust.gov.kg`

## Testing

- pytest
- mocked LLM calls
- mocked HTTP requests

No real API calls or costs during tests.

## Deployment

- Docker
- Docker Compose

---

# Project structure

```
legal-rag-kg/
│
├── app/
│   ├── main.py                    # FastAPI entrypoint (/ask endpoint)
│   ├── config.py                  # env-based config (API keys, headers)
│   │
│   ├── models/
│   │   └── schemas.py              # Pydantic request/response models
│   │
│   ├── ingestion/
│   │   ├── minjust_client.py       # Ministry of Justice API client
│   │   └── parser.py               # HTML → structured articles
│   │
│   ├── embeddings/
│   │   └── embedder.py             # Gemini embedding wrapper
│   │
│   ├── vectorstore/
│   │   └── chroma_store.py         # ChromaDB integration
│   │
│   └── retrieval/
│       ├── search.py               # semantic search
│       └── generation.py            # RAG answer generation
│
├── scripts/
│   ├── ingest.py                   # fetch + parse → processed JSON
│   └── embed_and_store.py          # embed articles → ChromaDB
│
├── data/                           # generated at runtime, not in git
├── tests/
└── docker-compose.yml
```

---

# Running locally (without Docker)

Clone repository:

```bash
git clone https://github.com/kalmatovski/legal-rag-kg.git

cd legal-rag-kg
```

Create virtual environment:

```bash
python -m venv .venv
```

Activate environment:

Linux/macOS:

```bash
source .venv/bin/activate
```

Windows:

```bash
.venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

# Environment variables

Create `.env` file in the project root:

```env
GEMINI_API_KEY=your_key_here
```

---

# Build knowledge base

The knowledge base needs to be generated before running the API.

Run:

```bash
python -m scripts.ingest
```

Then:

```bash
python -m scripts.embed_and_store
```

This only needs to be executed once, or whenever the Civil Code is updated.

---

# Run API

Start FastAPI:

```bash
uvicorn app.main:app --reload
```

Open:

```
http://127.0.0.1:8000/docs
```

for interactive API documentation.

---

# Running with Docker

The data pipeline (ingestion + embedding) runs on the host first.

The container mounts:

```
./data
```

instead of baking the knowledge base into the Docker image.

Advantages:

- update legal documents without rebuilding the image
- easier maintenance
- faster deployments

Build knowledge base:

```bash
python -m scripts.ingest

python -m scripts.embed_and_store
```

Start application:

```bash
docker compose up --build
```

---

# API Example

Request:

```bash
curl -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "Какой общий срок исковой давности?"}'
```

Response:

```json
{
  "answer": "Общий срок исковой давности в Кыргызской Республике устанавливается в три года...",
  "sources": [
    {
      "number": "212",
      "title": "Общий срок исковой давности",
      "chapter_title": "Сроки. Исковая давность"
    }
  ]
}
```

---

# Running tests

Run:

```bash
python -m pytest -v
```

All external calls are mocked:

- Ministry of Justice API
- Gemini API

Tests run offline without API costs.

---

# Notes on the data

Source:

```
Civil Code of the Kyrgyz Republic, Part I
```

Document:

```
documentCode=4
edition=52160
```

Edition:

```
06.04.2026
```

Statistics:

- 433 articles
- 22 chapters

The dataset includes two chapters inserted later with hyphenated numbering:

```
Глава 10-1
```

Articles with partially repealed clauses are flagged:

```json
{
  "has_repealed_clauses": true
}
```

The repealed clause text itself is removed from the indexed content together with legislative amendment annotations.

---

# License

This project is intended for educational and research purposes.
