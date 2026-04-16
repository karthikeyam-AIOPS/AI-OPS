# examples

See the project [README.md](../README.md) for full documentation.

### 1. Anomaly Detection Demo (`anomaly_detection_demo.py`)

**Purpose**: Demonstrates log anomaly detection using TF-IDF vectorization and Random Forest classification.

**Key Features**:
- Text-based log analysis using TF-IDF features
- Binary classification (normal vs anomaly)
- Probability scoring for anomaly likelihood
- Mock system log dataset for training

**Use Cases**:
- Security incident detection
- System failure prediction  
- Unusual pattern identification in logs
- Performance monitoring

**Example Output**:
```
Log: FATAL ERROR: Kernel panic on CPU 0
Result: ⚠️ ANOMALY (Anomaly probability: 87.3%)
```

### 2. Student Performance Prediction (`student_prediction_demo.py`)

**Purpose**: Shows different ML approaches for predicting outcomes based on multiple features.

**Key Features**:
- Pass/fail binary classification with Logistic Regression
- Multi-class grade prediction with Random Forest
- Decision boundary visualization
- Feature importance analysis
- Probability distributions for predictions

**Use Cases**:
- Resource allocation prediction
- Performance forecasting
- Multi-class categorization
- Risk assessment modeling

**Models Demonstrated**:
- **Binary Classification**: Logistic Regression for pass/fail prediction
- **Multi-class Classification**: Random Forest for letter grade prediction  

### 3. Log Sentiment Analysis (`sentiment_analysis_demo.py`)

**Purpose**: Applies sentiment analysis to system logs to detect potential issues through "emotional tone" analysis.

**Key Features**:
- TextBlob-based sentiment scoring
- Batch processing of multiple logs
- Summary statistics and anomaly detection
- Threshold-based alerting
- Detailed sentiment interpretation

**Use Cases**:
- Automated incident detection
- System health trend analysis
- Real-time log monitoring
- Complement to keyword-based monitoring

**Requirements**: `pip install textblob`

### 4. Capacity Forecasting Demo (`../Forecasting/capacity_forecasting_demo.py`)

**Purpose**: Demonstrates predictive capacity planning using linear regression for resource usage forecasting.

**Key Features**:
- Historical usage data simulation
- Linear regression model training and prediction
- Model persistence with joblib
- Time-series forecasting with date-based predictions
- Model metadata capture and analysis
- Capacity inference class for production-ready predictions

**Use Cases**:
- Storage capacity planning
- CPU/Memory usage forecasting
- Infrastructure scaling decisions
- Budget planning for resource expansion
- Proactive capacity management

**Models Demonstrated**:
- **Time Series Forecasting**: Linear Regression for capacity growth prediction
- **Model Persistence**: Save/load trained models for production use
- **Date-based Predictions**: Real-world date interface for forecasting

**Example Output**:
```
Capacity Forecast Results:
==================================================
   Day  GB_Used      Type
    26   139.23    Actual
    27   140.85    Actual
    28   142.41    Actual
    29   143.97    Actual
    30   145.53    Actual
    31   147.09  Forecast
    32   148.65  Forecast
    ...

Model Captured:
- Growth Rate: 1.50 GB per day
- Starting Point: 100.25 GB
- Accuracy Score (R2): 0.9847

Forecast for June 1st, 2026: 254.12 GB
```

**Requirements**: `pip install scikit-learn joblib pandas numpy`

### 5. RAG API — Colab Demo (`ragapi_colab_demo.py`)

**Purpose**: Full RAG API server (FastAPI + SQLite + Redis + ChromaDB) written as a Colab-friendly Python script.

**Key Features**:
- Sentiment analysis (`/predict`, `/ask`) via DistilBERT
- Token-by-token streaming endpoint (`/stream-ai`)
- Image classification (`/classify`) via ViT with SHA-256 cache
- Retrieval-Augmented Generation (`/ask-rag`) using GPT-2 + ChromaDB
- Three-tier look-aside cache: Redis → SQLite → model
- Rate limiting (5 req/min) on the RAG endpoint
- All credentials loaded from Colab Secrets / environment variables

**Required secrets** (`NGROK_AUTH_TOKEN`):
```bash
export NGROK_AUTH_TOKEN=<token>   # https://dashboard.ngrok.com
```

**Requirements**: `pip install fastapi uvicorn pyngrok nest_asyncio transformers torch sqlalchemy redis pillow chromadb slowapi`

### 6. AI Agent vs Agentic AI (`ai_agent_vs_agentic_ai.py`)

**Purpose**: Side-by-side demonstration of a simple reactive AI Agent versus an autonomous Agentic AI system using LangGraph.

**Key Features**:
- **Part 1** — Simple AI Agent: single-shot Ollama/Llama 3.2 sentiment call
- **Part 2** — Agentic AI (Ollama): LangGraph Analyzer → Critic retry loop
- **Part 3** — Agentic AI (GPT-4o): full 10-annotation agentic architecture
- **Part 4 & 5** — DeepEval evaluations: infrastructure + movie review domains
- All credentials loaded via `_get_secret()` (Colab Secrets → env var)

**Required secrets**:
```bash
export NGROK_AUTH_TOKEN=<token>   # https://dashboard.ngrok.com
export OPENAI_API_KEY=<key>       # https://platform.openai.com/api-keys
```

**Requirements**: `pip install fastapi uvicorn pyngrok langchain-ollama langchain-openai langgraph deepeval`

**Notebook version**: [`AI_Agent_Vs_Agentic_AI.ipynb`](AI_Agent_Vs_Agentic_AI.ipynb)

## 🚀 Running the Examples

### Run Individual Examples
```bash
# Anomaly detection
python examples/anomaly_detection_demo.py

# Student prediction (showcases general ML patterns)
python examples/student_prediction_demo.py

# Sentiment analysis
python examples/sentiment_analysis_demo.py

# Capacity forecasting
python Forecasting/capacity_forecasting_demo.py
```

### Run All Examples
```bash
python examples/run_all_examples.py
```

### Integration with AI-OPS Package
```python
# Import from the main package (when implemented)
from ai_ops.models import AnomalyDetector
from ai_ops.collectors import LogCollector

# Or run as standalone demonstrations
```

## 📊 Example Data

All examples use mock/synthetic data for demonstration purposes:

- **Log Data**: Realistic system log messages with labeled anomalies
- **Student Data**: Academic performance metrics with various outcomes
- **Sentiment Data**: System logs with different emotional tones

## 🛠️ Dependencies

Core dependencies (automatically installed with AI-OPS):
- `pandas` - Data manipulation
- `scikit-learn` - Machine learning algorithms
- `numpy` - Numerical computing

Optional dependencies:
- `matplotlib` - Visualization (for decision boundaries)
- `textblob` - Sentiment analysis

Install optional dependencies:
```bash
pip install matplotlib textblob
```

## 🎯 Learning Objectives

These examples demonstrate:

1. **Text Analysis**: Converting unstructured log data to ML features
2. **Classification**: Binary and multi-class prediction problems
3. **Feature Engineering**: Creating meaningful features from raw data
4. **Model Evaluation**: Probability scoring and confidence measures
5. **Real-world Application**: Practical use cases in operations

## 🔄 Integration with Main Package

These examples serve as:
- **Proof of concepts** for the main AI-OPS functionality
- **Educational materials** for understanding the approaches
- **Testing grounds** for new ML techniques
- **Templates** for implementing custom solutions

The patterns demonstrated here are implemented in the main `ai_ops` package modules:
- `ai_ops.models` - ML models and algorithms
- `ai_ops.collectors` - Data collection and preprocessing
- `ai_ops.processors` - Data processing pipelines

## 📚 Next Steps

1. Explore the individual example files
2. Modify the examples with your own data
3. Check out the main AI-OPS documentation
4. Implement similar patterns in your own projects

For more information about the AI-OPS project, see the main [README.md](../README.md).