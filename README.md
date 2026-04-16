# AI-OPS Toolkit

[![CI — Quick Smoke Tests](https://github.com/karthikeyam-AIOPS/AI-OPS/actions/workflows/basic-ci.yml/badge.svg)](https://github.com/karthikeyam-AIOPS/AI-OPS/actions/workflows/basic-ci.yml)
[![CI — Code Quality](https://github.com/karthikeyam-AIOPS/AI-OPS/actions/workflows/code-quality.yml/badge.svg)](https://github.com/karthikeyam-AIOPS/AI-OPS/actions/workflows/code-quality.yml)

A modular, AI-driven framework for infrastructure management, anomaly detection, and automated remediation — designed for **AI-Native** operations.

---

## Table of Contents

1. [Project Structure](#1-project-structure)
2. [Installation](#2-installation)
3. [Quick Start](#3-quick-start)
4. [Package — ai_ops](#4-package--ai_ops)
   - [RAG API](#rag-api-ragapipy)
   - [Collectors](#collectors)
   - [Models](#models)
5. [Forecasting Module](#5-forecasting-module)
   - [Processors](#processors)
   - [Remediation](#remediation)
6. [Examples & Demos](#6-examples--demos)
7. [Tests](#7-tests)
8. [CI/CD Workflows](#8-cicd-workflows)
9. [Docker](#9-docker)
10. [Configuration & Secrets](#10-configuration--secrets)
11. [Contributing](#11-contributing)

---

## 1. Project Structure

```
AI-OPS/
├── ai_ops/                        # Primary package
│   ├── __init__.py
│   ├── main.py                    # CLI entry point (Typer)
│   ├── ragapi.py                  # FastAPI RAG service
│   ├── collectors/                # Data collection layer
│   └── models/                   # ML model layer
├── Forecasting/                   # Capacity forecasting module
│   ├── capacity_forecasting_demo.py
│   ├── processors/                # Time-series preprocessing
│   └── remediation/               # Automated remediation actions
├── examples/                      # Standalone demos
│   ├── anomaly_detection_demo.py
│   ├── sentiment_analysis_demo.py
│   ├── student_prediction_demo.py
│   ├── capacity_forecasting_demo.py
│   ├── ragapi_colab_demo.py
│   ├── ai_agent_vs_agentic_ai.py
│   └── AI_Agent_Vs_Agentic_AI.ipynb
├── tests/                         # Test suite
├── scripts/                       # Dev utilities
├── Dockerfile
├── docker-compose.yml
├── pyproject.toml
└── requirements.txt
```

---

## 2. Installation

```bash
git clone https://github.com/karthikeyam-AIOPS/AI-OPS.git
cd AI-OPS

# Standard install
pip install -e .

# With development dependencies
pip install -e ".[dev]"

# Verify
aiops --help
```

---

## 3. Quick Start

```bash
aiops status      # check system health
aiops examples    # list available demos
aiops forecast    # run capacity forecast
aiops test        # run test suite
```

---

## 4. Package — ai_ops

### RAG API (`ragapi.py`)

A production-ready FastAPI service backed by SQLite, Redis, and ChromaDB.

#### Endpoints

| Method | Path | Description |
|--------|------|-------------|
| `POST` | `/predict` | Sentiment analysis via DistilBERT |
| `GET` | `/stream-ai` | Token-by-token streaming AI response |
| `GET` | `/ask` | Cached sentiment — Redis → SQLite → model |
| `POST` | `/classify` | Image classification via ViT (cached by SHA-256) |
| `GET` | `/ask-rag` | RAG using GPT-2 + ChromaDB (5 req/min rate-limited) |
| `GET` | `/docs` | Swagger UI |

#### Cache Architecture

```
Request
  │
  ▼
Redis (HIT → return immediately)
  │ MISS
  ▼
SQLite (HIT → re-cache in Redis, return)
  │ MISS
  ▼
AI Model → save to SQLite → cache in Redis (60s TTL) → return
```

> For `/ask-rag`, the model step first retrieves context from **ChromaDB** before inference.

#### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `NGROK_AUTH_TOKEN` | — | Public tunnel token (dashboard.ngrok.com) |
| `DATABASE_URL` | `sqlite:///./ragapi.db` | SQLAlchemy database URL |
| `REDIS_HOST` | `localhost` | Redis hostname |
| `REDIS_PORT` | `6379` | Redis port |

---

### Collectors

Data collection layer — pulls telemetry, logs, and metrics from external systems.

#### Planned Collectors

| Collector | Source | Description |
|-----------|--------|-------------|
| `prometheus.py` | Prometheus / VictoriaMetrics | Scrapes metrics via HTTP API |
| `elk.py` | Elasticsearch / OpenSearch | Queries logs from ELK stacks |
| `aws.py` | AWS CloudWatch | Pulls CloudWatch metrics and log groups |
| `k8s.py` | Kubernetes API | Reads pod/node events and resource usage |
| `syslog.py` | Syslog / journald | Tails system logs from Linux hosts |

#### Interface

```python
class BaseCollector:
    def connect(self) -> None: ...
    def collect(self, start: datetime, end: datetime) -> pd.DataFrame: ...
    def close(self) -> None: ...
```

Output `DataFrame` columns: `timestamp`, `source`, `metric`, `value`.

---

### Models

ML model layer — consumes normalised DataFrames and returns structured predictions.

#### Planned Models

| Model | File | Task |
|-------|------|------|
| Anomaly Detector | `anomaly_detector.py` | Binary: normal vs anomaly |
| Capacity Forecaster | `capacity_forecaster.py` | Time-series regression |
| Root Cause Analyser | `rca.py` | Multi-class failure classification |
| Sentiment Analyser | `sentiment.py` | Log urgency / tone scoring |
| RAG Pipeline | `rag.py` | Retrieval-Augmented Generation Q&A |

#### Interface

```python
class BaseModel:
    def train(self, df: pd.DataFrame) -> None: ...
    def predict(self, df: pd.DataFrame) -> pd.DataFrame: ...
    def save(self, path: str) -> None: ...
    def load(self, path: str) -> None: ...
```

Output `DataFrame` columns: `timestamp`, `prediction`, `confidence`.

---

## 5. Forecasting Module

Predictive capacity planning using linear regression for resource usage forecasting.

```python
from Forecasting import CapacityInference

inference = CapacityInference('cpu_forecast_model.pkl')
print(inference.predict_for_date('2026-06-01'))

for pred in inference.predict_range('2026-04-10', '2026-04-16'):
    print(f"{pred['date']}: {pred['predicted_gb']} GB")
```

```bash
python Forecasting/capacity_forecasting_demo.py
```

### Processors

Time-series preprocessing utilities (cleaner, resampler, feature engineer, scaler, splitter).

```python
class BaseProcessor:
    def fit(self, df: pd.DataFrame) -> "BaseProcessor": ...
    def transform(self, df: pd.DataFrame) -> pd.DataFrame: ...
    def fit_transform(self, df: pd.DataFrame) -> pd.DataFrame: ...
```

Processors can be chained:

```python
pipeline = [Cleaner(), Resampler(freq="1D"), FeatureEngineer(lags=[1, 7])]
for step in pipeline:
    df = step.fit_transform(df)
```

### Remediation

Automated actions triggered when a forecast exceeds a threshold.

#### Planned Remediators

| Remediator | Action |
|------------|--------|
| `alerting.py` | PagerDuty / Slack / email alert |
| `autoscaler.py` | Kubernetes HPA or cloud auto-scaling |
| `disk_archiver.py` | Move cold data to S3 / GCS |
| `ticketing.py` | Open Jira / ServiceNow incident |
| `runbook.py` | Run Ansible or shell runbook |

```python
class BaseRemediator:
    def should_trigger(self, forecast: pd.DataFrame) -> bool: ...
    def execute(self, forecast: pd.DataFrame) -> dict: ...
```

---

## 6. Examples & Demos

All examples use synthetic data and are runnable standalone.

### Available Examples

| # | File | Description |
|---|------|-------------|
| 1 | `anomaly_detection_demo.py` | Log anomaly detection — TF-IDF + Random Forest |
| 2 | `student_prediction_demo.py` | Binary & multi-class classification patterns |
| 3 | `sentiment_analysis_demo.py` | TextBlob log sentiment scoring |
| 4 | `capacity_forecasting_demo.py` | Linear regression capacity forecasting |
| 5 | `ragapi_colab_demo.py` | Full RAG API — Colab-friendly, all secrets via env vars |
| 6 | `ai_agent_vs_agentic_ai.py` | AI Agent vs Agentic AI (Ollama + GPT-4o + DeepEval) |
| 6 | `AI_Agent_Vs_Agentic_AI.ipynb` | Notebook version of the agent demo |

### Running Examples

```bash
# Individual
python examples/anomaly_detection_demo.py
python examples/sentiment_analysis_demo.py
python examples/student_prediction_demo.py
python Forecasting/capacity_forecasting_demo.py

# All at once
python examples/run_all_examples.py
```

### RAG API Colab Demo (`ragapi_colab_demo.py`)

Full FastAPI RAG server (DistilBERT, ViT, GPT-2, ChromaDB, Redis, SQLite) as a Colab script.

**Required secret**: `NGROK_AUTH_TOKEN`

### AI Agent vs Agentic AI (`ai_agent_vs_agentic_ai.py`)

| Part | Description |
|------|-------------|
| 1 | Simple AI Agent — Ollama single-shot sentiment |
| 2 | Agentic AI — Ollama + LangGraph Analyzer→Critic loop |
| 3 | Agentic AI — GPT-4o + LangGraph (10-annotation architecture) |
| 4–5 | DeepEval evaluations — infrastructure + movie review domains |

**Required secrets**: `NGROK_AUTH_TOKEN`, `OPENAI_API_KEY`

---

## 7. Tests

```bash
# Smart runner (adapts to installed plugins)
python scripts/run_tests.py

# Direct pytest
pytest tests/test_simple.py -v
pytest --cov=ai_ops --cov-report=term-missing

# With Allure (if plugin installed)
pytest --alluredir=allure-results
allure serve allure-results
```

### Test Categories

| Marker | Description |
|--------|-------------|
| `unit` | Individual component tests |
| `integration` | Module interaction tests |
| `smoke` | Critical path verification |
| `performance` | Benchmark tests |

---

## 8. CI/CD Workflows

| Workflow | Trigger | What it does |
|----------|---------|--------------|
| `CI — Quick Smoke Tests` | push / PR | Python setup, Black formatting, pytest |
| `CI — Build, Lint & Security` | push / PR | Lint, isort, build, coverage, safety, bandit, Docker |
| `CI — Code Quality (Format & Style)` | PR (Python files) | Black, isort, flake8, mypy |
| `CI — Tests & Coverage Reports` | push / PR | pytest + coverage XML/HTML + job summary |

All workflows write a **job summary** to GitHub Actions (`$GITHUB_STEP_SUMMARY`) showing test counts and coverage.

---

## 9. Docker

```bash
# Build and start all services (API + Redis)
docker compose up --build

# Stop
docker compose down

# Stop and remove volumes
docker compose down -v
```

| URL | Description |
|-----|-------------|
| `http://localhost:8000/docs` | Swagger UI |
| `http://localhost:8000/redoc` | ReDoc UI |

The container runs as a non-root `appuser`. Hugging Face model cache is stored at `/app/.cache/huggingface` (writable by `appuser`).

---

## 10. Configuration & Secrets

**Never hardcode credentials.** Use environment variables or Colab Secrets.

| Variable | Used by | Description |
|----------|---------|-------------|
| `NGROK_AUTH_TOKEN` | ragapi, demos | Ngrok tunnel token — dashboard.ngrok.com |
| `OPENAI_API_KEY` | agent demo | OpenAI API key — platform.openai.com/api-keys |
| `DATABASE_URL` | ragapi | SQLAlchemy URL (default: `sqlite:///./ragapi.db`) |
| `REDIS_HOST` | ragapi | Redis hostname (default: `localhost`) |
| `REDIS_PORT` | ragapi | Redis port (default: `6379`) |
| `OLLAMA_BASE_URL` | agent demo | Ollama server (default: `http://localhost:11434`) |
| `OLLAMA_MODEL` | agent demo | Model name (default: `llama3.2`) |

```bash
# Linux / macOS
export NGROK_AUTH_TOKEN=<token>
export OPENAI_API_KEY=<key>

# Windows PowerShell
$env:NGROK_AUTH_TOKEN="<token>"
$env:OPENAI_API_KEY="<key>"
```

---

## 11. Contributing

1. Create a feature branch: `git checkout -b feature/your-feature`
2. Place logic in the correct directory (`models/`, `collectors/`, `processors/`, `remediation/`)
3. Add a `@app.command()` in `ai_ops/main.py` if adding CLI functionality
4. Add tests under `tests/`
5. Open a Pull Request — CI will run automatically
