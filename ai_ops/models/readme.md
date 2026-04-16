# ai_ops / models

See the project [README.md](../../README.md) for full documentation.

## Planned Models

| Model | File | Task |
|-------|------|------|
| Anomaly Detector | `anomaly_detector.py` | Binary classification — normal vs anomaly |
| Capacity Forecaster | `capacity_forecaster.py` | Time-series regression for resource usage |
| Root Cause Analyser | `rca.py` | Multi-class classification — failure root cause |
| Sentiment Analyser | `sentiment.py` | Log sentiment scoring (urgency / tone) |
| RAG Pipeline | `rag.py` | Retrieval-Augmented Generation for Q&A |

## Interface Convention

Every model should implement the following interface:

```python
class BaseModel:
    def train(self, df: pd.DataFrame) -> None: ...
    def predict(self, df: pd.DataFrame) -> pd.DataFrame: ...
    def save(self, path: str) -> None: ...
    def load(self, path: str) -> None: ...
```

The returned `DataFrame` should contain at minimum:

| Column | Type | Description |
|--------|------|-------------|
| `timestamp` | `datetime` | Event time from input |
| `prediction` | `str \| float` | Model output (label or value) |
| `confidence` | `float` | Confidence score in `[0, 1]` |

## Usage (example)

```python
from ai_ops.models.anomaly_detector import AnomalyDetector
import pandas as pd

detector = AnomalyDetector()
detector.train(training_df)

results = detector.predict(live_df)
anomalies = results[results["prediction"] == "anomaly"]
print(f"Detected {len(anomalies)} anomalies")

detector.save("models/anomaly_detector_v1.pkl")
```

## Model Persistence

Trained models are stored as `joblib` pickle files under `models/` (git-ignored).
Use `save()` / `load()` for production deployments and CI artifact caching.

## Contributing

1. Add a new file `<model_name>.py` in this directory.
2. Inherit from `BaseModel`.
3. Add tests under `tests/models/`.
4. Update this readme with the new entry in the table above.
