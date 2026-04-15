# -*- coding: utf-8 -*-
"""
RAG API — AI-OPS
================
A FastAPI application that exposes four AI-powered endpoints, backed by
SQLite persistence, Redis caching, a ChromaDB vector store, and an Ngrok
tunnel for public access.

Endpoints
---------
POST /predict
    Sentiment analysis on a text string using DistilBERT.

GET  /stream-ai
    Streaming token-by-token AI response simulation.

GET  /ask
    Cached sentiment analysis with SQLite + Redis look-aside cache.

POST /classify
    Image classification using Vision Transformer (ViT), cached by image hash.

GET  /ask-rag
    Retrieval-Augmented Generation using GPT-2 + ChromaDB, rate-limited to
    5 requests per minute per client IP.

Setup
-----
1. Install dependencies::

       pip install -r requirements.txt

2. Start a local Redis server::

       redis-server

3. Set your Ngrok auth token as an environment variable::

       export NGROK_AUTH_TOKEN=<your_token>

   Obtain a free token at https://dashboard.ngrok.com

4. Run the server::

       python -m ai_ops.ragapi
"""

# ---------------------------------------------------------------------------
# Imports
# ---------------------------------------------------------------------------
import asyncio
import hashlib
import io
import json
import os
import time

import chromadb
import nest_asyncio
import redis
import uvicorn
from fastapi import Depends, FastAPI, File, Request, UploadFile
from fastapi.responses import StreamingResponse
from PIL import Image
from pyngrok import ngrok
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address
from sqlalchemy import String, Text, create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column, sessionmaker
from transformers import pipeline

# ---------------------------------------------------------------------------
# Database setup
# ---------------------------------------------------------------------------
DATABASE_URL = "sqlite:///./ragapi.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    """SQLAlchemy declarative base for all ORM models."""


class Prediction(Base):
    """Persists every unique prompt/response pair so repeated queries skip inference."""

    __tablename__ = "predictions"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    prompt: Mapped[str] = mapped_column(String, index=True)
    response: Mapped[str] = mapped_column(Text)


Base.metadata.create_all(bind=engine)

# ---------------------------------------------------------------------------
# Redis cache
# ---------------------------------------------------------------------------
cache = redis.Redis(
    host=os.environ.get("REDIS_HOST", "localhost"),
    port=int(os.environ.get("REDIS_PORT", 6379)),
    decode_responses=True,
)

# ---------------------------------------------------------------------------
# AI models
# ---------------------------------------------------------------------------
# Sentiment analysis — used by /predict and /ask
sentiment_pipeline = pipeline(
    "sentiment-analysis",
    model="distilbert-base-uncased-finetuned-sst-2-english",
)

# Image classification — used by /classify
vision_pipeline = pipeline(
    "image-classification",
    model="google/vit-base-patch16-224",
)

# Text generation — used by /ask-rag
rag_pipeline = pipeline("text-generation", model="gpt2")

# ---------------------------------------------------------------------------
# Vector database (ChromaDB) — used by /ask-rag
# ---------------------------------------------------------------------------
chroma_client = chromadb.Client()
knowledge_base = chroma_client.get_or_create_collection(name="knowledge_base")

# Seed with sample company knowledge (replace with real document ingestion in production)
knowledge_base.add(
    documents=[
        "The company policy allows 20 days of remote work per year.",
        "The IT department is located on the 4th floor.",
        "Gym memberships are reimbursed up to $50 monthly.",
    ],
    ids=["doc1", "doc2", "doc3"],
)

# ---------------------------------------------------------------------------
# FastAPI application
# ---------------------------------------------------------------------------
limiter = Limiter(key_func=get_remote_address)
nest_asyncio.apply()

app = FastAPI(
    title="RAG API",
    description="AI-powered REST API with sentiment analysis, image classification, and RAG.",
    version="1.0.0",
)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


# ---------------------------------------------------------------------------
# Dependency
# ---------------------------------------------------------------------------
def get_db():
    """Yield a database session and ensure it is closed after each request."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------
@app.post("/predict")
async def predict_sentiment(text: str):
    """
    Run sentiment analysis on the supplied text.

    Parameters
    ----------
    text : str
        The input string to classify.

    Returns
    -------
    dict
        ``input`` — original text, ``analysis`` — label and score from DistilBERT.
    """
    result = sentiment_pipeline(text)
    return {"input": text, "analysis": result}


async def _stream_tokens(prompt: str):
    """Async generator that yields words with a short delay to simulate streaming."""
    words = (
        f"AI Response to '{prompt}': "
        "This is a simulated stream of tokens coming from your model..."
    ).split()
    for word in words:
        yield f"{word} "
        await asyncio.sleep(0.3)


@app.get("/stream-ai")
async def stream_ai(prompt: str):
    """
    Stream an AI-generated response token by token.

    Parameters
    ----------
    prompt : str
        The question or context to respond to.

    Returns
    -------
    StreamingResponse
        Plain-text token stream.
    """
    return StreamingResponse(_stream_tokens(prompt), media_type="text/plain")


@app.get("/ask")
async def ask_ai(prompt: str, db: Session = Depends(get_db)):
    """
    Cached sentiment analysis with three-tier look-aside: Redis → SQLite → model.

    Parameters
    ----------
    prompt : str
        Text to analyse.

    Returns
    -------
    dict
        ``source`` — where the answer came from, ``elapsed`` — wall-clock time,
        ``data`` — the result string.
    """
    start_time = time.time()

    # Tier 1: Redis
    cached_res = cache.get(prompt)
    if cached_res:
        return {
            "source": "Redis Cache",
            "elapsed": f"{time.time() - start_time:.4f}s",
            "data": json.loads(cached_res),
        }

    # Tier 2: SQLite
    db_record = db.query(Prediction).filter(Prediction.prompt == prompt).first()
    if db_record:
        cache.setex(prompt, 60, json.dumps(db_record.response))
        return {
            "source": "SQLite Database",
            "elapsed": f"{time.time() - start_time:.4f}s",
            "data": db_record.response,
        }

    # Tier 3: Model inference
    result = sentiment_pipeline(prompt)[0]
    ai_result = f"AI Analysis: {result['label']} (Score: {result['score']:.2f})"

    db.add(Prediction(prompt=prompt, response=ai_result))
    db.commit()
    cache.setex(prompt, 60, json.dumps(ai_result))

    return {
        "source": "Real AI Model",
        "elapsed": f"{time.time() - start_time:.4f}s",
        "data": ai_result,
    }


@app.post("/classify")
async def classify_image(file: UploadFile = File(...), db: Session = Depends(get_db)):
    """
    Classify the contents of an uploaded image using ViT.

    The image is fingerprinted with SHA-256 so identical uploads are served
    from cache without re-running inference.

    Parameters
    ----------
    file : UploadFile
        The image file to classify (JPEG, PNG, etc.).

    Returns
    -------
    dict
        ``source`` — cache tier used, ``data`` — top label and confidence.
    """
    image_bytes = await file.read()
    img_hash = hashlib.sha256(image_bytes).hexdigest()

    cached_res = cache.get(img_hash)
    if cached_res:
        return {"source": "Redis Cache", "data": json.loads(cached_res)}

    db_record = db.query(Prediction).filter(Prediction.prompt == img_hash).first()
    if db_record:
        cache.setex(img_hash, 60, json.dumps(db_record.response))
        return {"source": "SQLite Database", "data": db_record.response}

    image = Image.open(io.BytesIO(image_bytes))
    results = vision_pipeline(image)
    top = results[0]
    ai_result = f"Detected: {top['label']} ({top['score']:.2%})"

    db.add(Prediction(prompt=img_hash, response=ai_result))
    db.commit()
    cache.setex(img_hash, 60, json.dumps(ai_result))

    return {"source": "Real AI Model", "data": ai_result}


@app.get("/ask-rag")
@limiter.limit("5/minute")
async def ask_rag(request: Request, question: str, db: Session = Depends(get_db)):
    """
    Answer a question using Retrieval-Augmented Generation (RAG).

    The relevant context is retrieved from ChromaDB, injected into the GPT-2
    prompt, and the response is persisted for future cache hits.
    Rate-limited to 5 requests per minute per IP.

    Parameters
    ----------
    request : Request
        FastAPI request object (required by slowapi for rate limiting).
    question : str
        The natural-language question to answer.

    Returns
    -------
    dict
        ``source``, ``data`` — the answer, ``context_used`` — retrieved chunk,
        ``elapsed`` — wall-clock time.
    """
    start_time = time.time()

    cached_res = cache.get(question)
    if cached_res:
        return {"source": "Redis Cache", "data": json.loads(cached_res)}

    db_record = db.query(Prediction).filter(Prediction.prompt == question).first()
    if db_record:
        return {"source": "SQLite Database", "data": db_record.response}

    results = knowledge_base.query(query_texts=[question], n_results=1)
    context = (
        results["documents"][0][0] if results["documents"] else "No context found."
    )

    input_text = (
        f"Answer the question based only on the context.\n"
        f"Context: {context}\nQuestion: {question}\nAnswer:"
    )

    ai_response_list = rag_pipeline(
        input_text,
        max_new_tokens=30,
        temperature=0.7,
        do_sample=True,
        pad_token_id=50256,
    )
    full_text = ai_response_list[0]["generated_text"]

    if "Answer:" in full_text:
        ai_response = full_text.split("Answer:")[-1].strip().split("\n")[0]
    else:
        ai_response = full_text.replace(input_text, "").strip().split("\n")[0]

    db.add(Prediction(prompt=question, response=ai_response))
    db.commit()
    cache.setex(question, 60, json.dumps(ai_response))

    return {
        "source": "Real AI Model (RAG)",
        "data": ai_response,
        "context_used": context,
        "elapsed": f"{time.time() - start_time:.4f}s",
    }


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    auth_token = os.environ.get("NGROK_AUTH_TOKEN")
    if auth_token:
        ngrok.set_auth_token(auth_token)

    public_url = ngrok.connect(8000).public_url
    print(f"API is LIVE at: {public_url}")
    print(f"Docs at:        {public_url}/docs")

    uvicorn.run(app, host="0.0.0.0", port=8000)
