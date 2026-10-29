# ResearchFlow AI — Personal Research-to-Action Agent

> **Turn research into action.**  
> An autonomous full-stack AI research workspace that transforms complex inquiries into verified, empirical research reports and structured, milestone-driven execution roadmaps.

---

## 1. Architecture Overview

ResearchFlow AI is designed as a production-grade multi-stage state machine using **LangGraph**, **FastAPI**, **Next.js 15 (App Router)**, **Pydantic V2**, and **FAISS Vector RAG**.

```
  +-------------------------------------------------------------+
  |              Next.js 15 + Tailwind CSS Frontend             |
  |    (SaaS Workspace, SSE Timeline, Tabs, Checkable Tasks)    |
  +------------------------------+------------------------------+
                                 | HTTP / SSE Stream
                                 v
  +-------------------------------------------------------------+
  |                   FastAPI Async API Gateway                 |
  |        (/api/research, /api/documents, /api/settings)       |
  +------------------------------+------------------------------+
                                 |
                                 v
  +-------------------------------------------------------------+
  |             LangGraph 9-Node Research Pipeline              |
  |                                                             |
  |  1. Goal Understanding   --> 2. Research Planning           |
  |  3. Source Collection    --> 4. Information Extraction      |
  |  5. Evidence Comparison  --> 6. Source Verification         |
  |  7. Knowledge Synthesis  --> 8. Action Roadmap              |
  |  9. Report Generation & Persistence                         |
  +--------------+-------------------------------+--------------+
                 |                               |
                 v                               v
    +-------------------------+     +-------------------------+
    |   Search & LLM Engine   |     |    Vector Store (RAG)   |
    | (DuckDuckGo, Gemini/OAI,|     | (FAISS Index, PDF, TXT, |
    |   Demo Fallback Mode)   |     |   MD Chunk Overlap)     |
    +-------------------------+     +-------------------------+
```

---

## 2. Core 9-Stage LangGraph Workflow

1. **Goal Understanding**: Parses user inquiry into structured objectives, scope boundaries, target audience, and operational constraints using Pydantic.
2. **Research Planning**: Breaks down the objective into 4 focused sub-questions, targeted keywords, source preferences, and refutation criteria.
3. **Source Collection**: Crawls web search engines (DuckDuckGo / Tavily) and personal knowledge base (FAISS), strictly deduplicating canonical URLs.
4. **Information Extraction**: Isolates atomic empirical claims, statistics, and trends linked directly to source URLs.
5. **Evidence Comparison**: Evaluates cross-source consensus, distinguishing independent corroboration from circular media replication.
6. **Source Verification**: Tests citations against retrieved excerpts to eliminate unverified or hallucinated assertions.
7. **Knowledge Synthesis**: Clusters thematic findings with confidence indicators (High / Medium / Emerging) and explicit caveats.
8. **Action Roadmap**: Builds milestone-driven execution phases with prerequisites, required deliverables, completion criteria, and checkable tasks.
9. **Report Generation**: Compiles a standardized 10-section report, persisted to SQLite repository for export (Markdown & PDF).

---

## 3. Technology Stack

- **Frontend**: Next.js 15, React 18, TypeScript, Tailwind CSS, Lucide Icons
- **Backend**: Python 3.14, FastAPI, Uvicorn, SQLAlchemy (Async + Sync)
- **Agent Orchestration**: LangGraph, LangChain-Core
- **Validation**: Pydantic V2 & Pydantic-Settings
- **RAG Subsystem**: FAISS-CPU, PyPDF, sliding window chunking with overlap
- **Search Providers**: DuckDuckGo Search (`ddgs`), Tavily API support, and built-in Demo synthesis mode
- **Export Formats**: ReportLab PDF Generation, GitHub-Flavored Markdown

---

## 4. Quickstart & Installation

### Prerequisites
- Python 3.10+ (tested on Python 3.14)
- Node.js 18+ and npm

### 1. Backend Setup

```bash
cd backend
pip install -r requirements.txt
```

*(Optional)* Configure API keys in `.env` (or copy from `.env.example`):
```bash
cp .env.example .env
# Set GEMINI_API_KEY=your_key or OPENAI_API_KEY=your_key
```
*Note: If no API key is provided, ResearchFlow AI operates in **Demo Mode**, synthesizing realistic structured research with zero crashes.*

### 2. Frontend Setup

```bash
cd frontend
npm install
npm run build
```

### 3. Running Locally

**Option A: One-click launcher (Windows)**
```cmd
run_dev.bat
```

**Option B: Manual Terminal Execution**

*Terminal 1 (Backend):*
```bash
cd backend
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

*Terminal 2 (Frontend):*
```bash
cd frontend
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) in your browser. API interactive documentation is available at [http://localhost:8000/docs](http://localhost:8000/docs).

---

## 5. API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/health` | Healthcheck and service version |
| `POST` | `/api/research` | Submit research inquiry and trigger LangGraph |
| `GET` | `/api/research/{id}` | Retrieve research status, stages, and outputs |
| `GET` | `/api/research/{id}/events` | Server-Sent Events (SSE) live progress stream |
| `GET` | `/api/research/{id}/report` | Fetch finalized 10-section research report |
| `GET` | `/api/research/{id}/export/markdown` | Download report as `.md` file |
| `GET` | `/api/research/{id}/export/pdf` | Download report as formatted `.pdf` |
| `PATCH` | `/api/research/{id}/tasks/{task_id}` | Toggle and persist roadmap task completion |
| `GET` | `/api/research` | List previous research sessions |
| `DELETE` | `/api/research/{id}` | Remove a research session |
| `POST` | `/api/documents/upload` | Upload and index PDF, TXT, or MD in FAISS |
| `GET` | `/api/documents` | List indexed personal knowledge documents |
| `DELETE` | `/api/documents/{id}` | Delete document and vector index chunks |
| `POST` | `/api/documents/search` | Test semantic vector retrieval |
| `GET` | `/api/settings` | Read runtime settings and detected API keys |
| `POST` | `/api/settings` | Update active providers and toggle demo mode |

---

## 6. Running Automated Tests

Run the complete test suite with pytest:

```bash
python -m pytest backend/tests -v
```

Tests verify:
- Goal parsing, constraints, and scope boundaries
- Research plan decomposition
- Canonical URL deduplication and publisher classification
- RAG text extraction, chunk overlap, and FAISS indexing
- FastAPI endpoint lifecycle and task completion persistence
- Report validation and export formatting

---

## 7. Transparent Limitations & Notes

- **Live Web Scraping**: DuckDuckGo search provides live search snippets and URLs without requiring an API key. For full deep-page parsing behind strict Cloudflare challenges, Tavily API or authenticated search proxies are recommended.
- **Demo Mode**: When no LLM API keys are provided in `.env`, the system automatically runs in clearly labeled Demo Mode, providing realistic evidence synthesis for UI exploration and automated testing without unexpected external API failures.
