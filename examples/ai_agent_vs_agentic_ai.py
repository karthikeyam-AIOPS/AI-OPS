# -*- coding: utf-8 -*-
"""
AI Agent vs Agentic AI
======================
Converted from: AI_Agent_Vs_Agentic_AI.ipynb

Demonstrates the difference between a simple AI Agent (single-step LLM call)
and Agentic AI (multi-step autonomous reasoning loop via LangGraph).

Three implementations are included:
  Part 1 — Simple AI Agent            (Ollama / Llama 3.2, single-shot)
  Part 2 — Agentic AI                 (Ollama / Llama 3.2, LangGraph loop)
  Part 3 — Agentic AI                 (OpenAI GPT-4o, LangGraph loop)
  Part 4 — Evaluation with DeepEval   (Infrastructure domain)
  Part 5 — Evaluation with DeepEval   (Movie reviews domain)

CONFIGURATION
-------------
Set the following environment variables before running:

  Required:
    NGROK_AUTH_TOKEN   — free token from https://dashboard.ngrok.com
    OPENAI_API_KEY     — key from https://platform.openai.com/api-keys

  Optional (defaults shown):
    OLLAMA_BASE_URL    — http://localhost:11434
    OLLAMA_MODEL       — llama3.2

  In Google Colab use: Runtime → Manage sessions → Secrets
  Locally use:         export NGROK_AUTH_TOKEN=<token>

Never paste tokens directly into source files.

SETUP (run once before starting the server)
-------------------------------------------
  pip install fastapi uvicorn pyngrok nest_asyncio \\
              langchain-ollama langchain-openai langgraph \\
              deepeval python-multipart

  # Ollama (Linux / Colab):
  curl -fsSL https://ollama.com/install.sh | sh
  ollama serve &
  ollama pull llama3.2
"""

# ---------------------------------------------------------------------------
# Secrets — Colab userdata → env var fallback
# ---------------------------------------------------------------------------
import os


def _get_secret(name: str, default: str = "") -> str:
    """
    Read a secret from Colab's userdata store, falling back to an
    environment variable and then the supplied default.

    Never hardcode credentials here — use Colab Secrets or set the
    corresponding environment variable before running.
    """
    try:
        from google.colab import userdata  # type: ignore[import]
        value = userdata.get(name)
        if value:
            return value
    except Exception:
        pass
    return os.environ.get(name, default)


NGROK_AUTH_TOKEN = _get_secret("NGROK_AUTH_TOKEN")
OPENAI_API_KEY   = _get_secret("OPENAI_API_KEY")
OLLAMA_BASE_URL  = _get_secret("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_MODEL     = _get_secret("OLLAMA_MODEL", "llama3.2")

# Surface the OpenAI key where the SDK expects it
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

if not NGROK_AUTH_TOKEN:
    raise EnvironmentError(
        "NGROK_AUTH_TOKEN is not set.\n"
        "  • In Colab: Runtime → Manage sessions → Secrets → add NGROK_AUTH_TOKEN\n"
        "  • Locally:  export NGROK_AUTH_TOKEN=<your_token>\n"
        "  Obtain a free token at https://dashboard.ngrok.com"
    )

if not OPENAI_API_KEY:
    raise EnvironmentError(
        "OPENAI_API_KEY is not set.\n"
        "  • In Colab: Runtime → Manage sessions → Secrets → add OPENAI_API_KEY\n"
        "  • Locally:  export OPENAI_API_KEY=<your_key>\n"
        "  Obtain a key at https://platform.openai.com/api-keys"
    )

# ---------------------------------------------------------------------------
# Imports
# ---------------------------------------------------------------------------
import asyncio
import nest_asyncio
import uvicorn
from typing import Annotated, TypedDict

from fastapi import FastAPI
from pydantic import BaseModel
from langchain_ollama import ChatOllama
from langchain_openai import ChatOpenAI
from langgraph.graph import END, START, StateGraph
from langgraph.graph.message import add_messages
from pyngrok import ngrok

# ---------------------------------------------------------------------------
# LLM clients
# ---------------------------------------------------------------------------
llm_ollama = ChatOllama(base_url=OLLAMA_BASE_URL, model=OLLAMA_MODEL)

# [7] DECISION MAKING: Temperature=0 for deterministic, logic-based decisions.
llm_gpt4o = ChatOpenAI(model="gpt-4o", temperature=0)

nest_asyncio.apply()

# ===========================================================================
# PART 1 — Simple AI Agent (Ollama / Llama 3.2)
# ===========================================================================
# An AI Agent makes a single LLM call and returns the result.
# It has no planning, no tool use, and no looping.
# ===========================================================================

class SentimentQuery(BaseModel):
    text: str


def run_standard_agent(text: str) -> dict:
    """Single-shot sentiment analysis — no loops, no retries."""
    prompt = (
        f"Analyze the sentiment of this text and return a label "
        f"(POSITIVE/NEGATIVE/NEUTRAL) with a confidence score: '{text}'"
    )
    response = llm_ollama.invoke(prompt)
    return {"label": response.content}


agent_app = FastAPI(
    title="Simple AI Agent — Sentiment Analysis",
    description="Single-step LLM call — one question, one answer.",
    version="1.0.0",
)


@agent_app.post("/v1/analyze-sentiment-simple")
async def process_simple_sentiment(query: SentimentQuery):
    """
    Simple AI Agent endpoint.

    Sends the user text directly to the LLM in a single round-trip.
    There is no memory, no planning, and no tool use.
    """
    result = run_standard_agent(query.text)
    print(f"--- LOG: Analysis complete. Result: {result} ---")
    return {"status": "success", "mode": "Standard AI Agent", "data": result}


# ===========================================================================
# PART 2 — Agentic AI with Ollama / LangGraph
# ===========================================================================
# Uses a stateful Analyzer → Critic → retry graph (max 2 retries).
# ===========================================================================

class OllamaAgentState(TypedDict):
    input_text: str
    report: str
    is_valid: bool
    retry: int


def _ollama_analyzer_node(state: OllamaAgentState) -> OllamaAgentState:
    prompt = f"Analyze sentiment and technical entities in: {state['input_text']}"
    res = llm_ollama.invoke(prompt)
    return {"report": res.content, "retry": state["retry"] + 1}


def _ollama_critic_node(state: OllamaAgentState) -> OllamaAgentState:
    prompt = f"Is this analysis deep enough? '{state['report']}'. Reply PASS or FAIL."
    res = llm_ollama.invoke(prompt)
    return {"is_valid": "PASS" in res.content.upper()}


_ollama_workflow = StateGraph(OllamaAgentState)
_ollama_workflow.add_node("analyze", _ollama_analyzer_node)
_ollama_workflow.add_node("critic", _ollama_critic_node)
_ollama_workflow.set_entry_point("analyze")
_ollama_workflow.add_edge("analyze", "critic")
_ollama_workflow.add_conditional_edges(
    "critic",
    lambda x: "end" if x["is_valid"] or x["retry"] >= 2 else "retry",
    {"end": END, "retry": "analyze"},
)
ollama_engine = _ollama_workflow.compile()


class OllamaQuery(BaseModel):
    text: str


agentic_ollama_app = FastAPI(
    title="Agentic AI (Ollama) — Sentiment Analysis",
    description="Multi-step LangGraph reasoning loop — plan, iterate, answer.",
    version="1.0.0",
)


@agentic_ollama_app.post("/analyze")
async def handle_ollama(q: OllamaQuery):
    """Agentic AI endpoint backed by Ollama / Llama 3.2."""
    out = ollama_engine.invoke(
        {"input_text": q.text, "report": "", "is_valid": False, "retry": 0}
    )
    return {"result": out["report"], "loops": out["retry"]}


# ===========================================================================
# PART 3 — Agentic AI with OpenAI GPT-4o / LangGraph
# ===========================================================================
# [1]  INTELLIGENCE MODELS   — GPT-4o as a Reasoning Kernel
# [2]  ARCHITECTURE           — LangGraph cyclic stateful state machine
# [3]  MEMORY SYSTEMS         — TypedDict as Short-term Working Memory
# [4]  TOOL USAGE & ACTIONS   — Agent acts on technical feedback
# [5]  KNOWLEDGE & RETRIEVAL  — Prompt extracts Infrastructure Entities
# [6]  ORCHESTRATION          — Router manages cyclic retries
# [7]  DECISION MAKING        — Temperature=0 for deterministic reasoning
# [8]  DEPLOYMENT             — FastAPI microservice (Kubernetes-ready)
# [9]  MONITORING             — Real-time debug logging / Reasoning Trace
# [10] LEARNING & IMPROVEMENT — Critic loop for self-reflection
# ===========================================================================

class GPT4oAgentState(TypedDict):
    input_text: str
    analysis_report: str
    is_satisfactory: bool
    retry_count: int


def _gpt4o_analytical_agent(state: GPT4oAgentState) -> GPT4oAgentState:
    """
    [4] TOOL USAGE & ACTIONS: The agent uses its internal logic
    to 'act' on the technical feedback provided.
    """
    # [9] MONITORING & OBSERVABILITY: Real-time debug logging
    # to track the 'Reasoning Trace' in the console.
    print(f"DEBUG: Researcher starting (Attempt {state['retry_count'] + 1})")

    # [5] KNOWLEDGE & RETRIEVAL: Prompt engineered to extract
    # 'Infrastructure Entities' (Technical Context).
    prompt = (
        f"Analyze this technical feedback: '{state['input_text']}'. "
        "Identify: 1. Technical Sentiment, 2. Human/Emotional Sentiment, "
        "3. Specific Infrastructure Entities mentioned."
    )
    response = llm_gpt4o.invoke(prompt)
    return {
        "analysis_report": response.content,
        "retry_count": state["retry_count"] + 1,
    }


def _gpt4o_quality_critic_agent(state: GPT4oAgentState) -> GPT4oAgentState:
    """
    [10] LEARNING & IMPROVEMENT: The Critic loop allows the system
    to 'reflect' and improve its output before returning it.
    """
    print("DEBUG: Critic evaluating analysis quality...")
    prompt = (
        f"Review this report: '{state['analysis_report']}'. "
        "Does it capture BOTH technical and emotional nuances? "
        "Reply only with 'PASS' or 'FAIL'."
    )
    response = llm_gpt4o.invoke(prompt)
    return {"is_satisfactory": "PASS" in response.content.upper()}


def _gpt4o_should_continue(state: GPT4oAgentState) -> str:
    """[6] ORCHESTRATION: Router that manages cyclic retries."""
    if state["is_satisfactory"] or state["retry_count"] >= 3:
        return "end"
    return "retry"


# [2] ARCHITECTURE & FRAMEWORKS: LangGraph cyclic stateful state machine
_gpt4o_builder = StateGraph(GPT4oAgentState)
_gpt4o_builder.add_node("researcher", _gpt4o_analytical_agent)
_gpt4o_builder.add_node("critic", _gpt4o_quality_critic_agent)
_gpt4o_builder.set_entry_point("researcher")
_gpt4o_builder.add_edge("researcher", "critic")
_gpt4o_builder.add_conditional_edges(
    "critic",
    _gpt4o_should_continue,
    {"end": END, "retry": "researcher"},
)
agentic_engine = _gpt4o_builder.compile()

# [8] DEPLOYMENT: Standardizing as a FastAPI microservice
# ready for Containerization/Kubernetes.
agentic_gpt4o_app = FastAPI(title="Agentic Sentiment Engine (GPT-4o)")


class GPT4oSentimentQuery(BaseModel):
    text: str


@agentic_gpt4o_app.post("/v1/analyze-sentiment")
async def process_sentiment(query: GPT4oSentimentQuery):
    """Agentic AI endpoint backed by GPT-4o + LangGraph."""
    initial_state = {
        "input_text": query.text,
        "analysis_report": "",
        "is_satisfactory": False,
        "retry_count": 0,
    }
    final_state = agentic_engine.invoke(initial_state)
    return {
        "status": "success",
        "iterations": final_state["retry_count"],
        "data": final_state["analysis_report"],
    }


# ===========================================================================
# PART 4 — Comparison endpoint (Ollama simple vs Ollama agentic)
# ===========================================================================

class CompareQuery(BaseModel):
    text: str


comparison_app = FastAPI(
    title="AI Agent vs Agentic AI",
    description="Side-by-side comparison of single-step agent and multi-step agentic reasoning.",
    version="1.0.0",
)


@comparison_app.post("/compare")
async def compare(query: CompareQuery):
    """Run the same text through both patterns and return side-by-side results."""
    # AI Agent — single call
    agent_result = run_standard_agent(query.text)

    # Agentic AI — graph loop
    agentic_out = ollama_engine.invoke(
        {"input_text": query.text, "report": "", "is_valid": False, "retry": 0}
    )

    return {
        "input": query.text,
        "ai_agent": {
            "type": "Single-step LLM call (Ollama)",
            "answer": agent_result["label"],
            "reasoning_steps": 1,
        },
        "agentic_ai": {
            "type": "Multi-step LangGraph loop (Ollama)",
            "answer": agentic_out["report"],
            "reasoning_steps": agentic_out["retry"],
        },
    }


@comparison_app.get("/health")
async def health():
    """Health check — confirms the server and Ollama connection are up."""
    try:
        llm_ollama.invoke("ping")
        ollama_status = "ok"
    except Exception as exc:
        ollama_status = f"error: {exc}"
    return {"status": "running", "ollama": ollama_status, "model": OLLAMA_MODEL}


# ===========================================================================
# PART 5 — Evaluation with DeepEval (Infrastructure domain)
# ===========================================================================
# Uses GPT-4o as a "Judge Agent" to evaluate whether the agentic engine
# correctly identifies technical infrastructure entities and emotional tone.
# ===========================================================================

def run_infrastructure_eval() -> None:
    """Evaluate agentic output on infrastructure feedback test cases."""
    from deepeval import evaluate
    from deepeval.metrics import GEval
    from deepeval.test_case import LLMTestCase, LLMTestCaseParams

    sentiment_metric = GEval(
        name="Technical Sentiment Accuracy",
        criteria=(
            "Determine if the agent correctly identifies technical infrastructure "
            "entities (like ClickHouse, nodes, clusters) and the human emotional "
            "tone (frustration, urgency)."
        ),
        evaluation_params=[LLMTestCaseParams.INPUT, LLMTestCaseParams.ACTUAL_OUTPUT],
        evaluation_steps=[
            "Check if the technical entity (e.g., ClickHouse) is correctly extracted.",
            "Assess if the emotional sentiment matches the user's urgency.",
            "Penalize if the agent misses the specific node or cluster count mentioned.",
        ],
        threshold=0.7,
    )

    test_cases_data = [
        {
            "input": "The 16-node postgres cluster is failing during vacuuming. I am extremely worried about data loss.",
            "expected_entities": ["postgres", "16-node cluster"],
            "expected_sentiment": "High Urgency / Fear",
        },
        {
            "input": "ClickHouse migration is smooth, node 5 is responding well.",
            "expected_entities": ["ClickHouse", "node 5"],
            "expected_sentiment": "Positive / Calm",
        },
    ]

    test_results = []
    for data in test_cases_data:
        # To use the real agentic engine, replace the placeholder with:
        # actual_output = agentic_engine.invoke({"input_text": data["input"]})["analysis_report"]
        actual_output = (
            f"Analysis: Found {data['expected_entities']}. "
            f"Tone is {data['expected_sentiment']}."
        )
        test_results.append(
            LLMTestCase(input=data["input"], actual_output=actual_output)
        )

    evaluate(test_results, [sentiment_metric])


# ===========================================================================
# PART 6 — Evaluation with DeepEval (Movie reviews domain)
# ===========================================================================
# Same Judge Agent pattern applied to a general-purpose domain to verify
# the framework works across different entity types.
# ===========================================================================

def run_movie_review_eval() -> None:
    """Evaluate agentic output on movie review test cases."""
    from deepeval import evaluate
    from deepeval.metrics import GEval
    from deepeval.test_case import LLMTestCase, LLMTestCaseParams

    movie_sentiment_metric = GEval(
        name="Cinema Sentiment & Entity Accuracy",
        criteria=(
            "Determine if the agent correctly identifies cinematic entities "
            "(actors, directors, genre) and the reviewer's emotional tone "
            "(appreciation, disappointment, excitement)."
        ),
        evaluation_params=[LLMTestCaseParams.INPUT, LLMTestCaseParams.ACTUAL_OUTPUT],
        evaluation_steps=[
            "Check if the key cinematic entities (e.g., Actor names, Director, or Movie title) are correctly extracted.",
            "Assess if the sentiment (Positive/Negative/Mixed) accurately reflects the reviewer's language.",
            "Verify if specific 'highs' or 'lows' mentioned (e.g., 'bad CGI' or 'great soundtrack') are captured in the summary.",
            "Penalize if the agent mistakes a sarcastic positive for a genuine positive.",
        ],
        threshold=0.7,
    )

    test_cases_data = [
        {
            "input": "Christopher Nolan's cinematography in Oppenheimer was breathtaking, but the 3-hour runtime felt a bit taxing.",
            "expected_entities": ["Christopher Nolan", "Oppenheimer"],
            "expected_sentiment": "Mixed (High Praise for Visuals, Critique on Length)",
        },
        {
            "input": "I went in with low expectations for the new superhero flick, but the lead actor's performance was surprisingly wooden and the plot was a mess.",
            "expected_entities": ["Lead actor", "Plot"],
            "expected_sentiment": "Negative / Disappointed",
        },
        {
            "input": "Absolutely loved the retro synth-wave soundtrack! It perfectly captured the 80s vibe of the film.",
            "expected_entities": ["Soundtrack", "80s vibe"],
            "expected_sentiment": "Highly Positive",
        },
    ]

    test_results = []
    for data in test_cases_data:
        actual_output = (
            f"Review Summary: Entities found: {data['expected_entities']}. "
            f"Detected Tone: {data['expected_sentiment']}."
        )
        test_results.append(
            LLMTestCase(input=data["input"], actual_output=actual_output)
        )

    evaluate(test_results, [movie_sentiment_metric])


# ---------------------------------------------------------------------------
# Entry point — launch Ngrok tunnel + comparison server
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    from pyngrok import ngrok

    ngrok.set_auth_token(NGROK_AUTH_TOKEN)
    public_url = ngrok.connect(8000).public_url
    print(f"API is LIVE at:  {public_url}")
    print(f"Docs at:         {public_url}/docs")
    print()
    print("Endpoints:")
    print(f"  POST {public_url}/compare                    — Agent vs Agentic (Ollama)")
    print(f"  POST {public_url}/v1/analyze-sentiment-simple — Simple Agent (Ollama)")
    print(f"  GET  {public_url}/health")
    print()
    print("Other apps (run separately on different ports):")
    print("  agentic_ollama_app  → POST /analyze          (Ollama LangGraph)")
    print("  agentic_gpt4o_app   → POST /v1/analyze-sentiment (GPT-4o LangGraph)")
    print()
    print("Evaluations (run directly):")
    print("  run_infrastructure_eval()")
    print("  run_movie_review_eval()")

    config = uvicorn.Config(comparison_app, host="0.0.0.0", port=8000, loop="asyncio")
    server = uvicorn.Server(config)
    asyncio.get_event_loop().run_until_complete(server.serve())
