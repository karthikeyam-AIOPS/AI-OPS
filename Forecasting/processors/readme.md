# Forecasting / processors

See the project [README.md](../../README.md) for full documentation.

## Planned Processors

| Processor | File | Responsibility |
|-----------|------|----------------|
| Cleaner | `cleaner.py` | Remove nulls, outliers, and duplicate timestamps |
| Resampler | `resampler.py` | Align time-series to a uniform frequency (1 h, 1 d, etc.) |
| Feature Engineer | `feature_engineer.py` | Create lag, rolling-mean, and calendar features |
| Scaler | `scaler.py` | MinMax / StandardScaler wrapper with inverse-transform |
| Splitter | `splitter.py` | Chronological train/validation/test split |

## Interface Convention

```python
class BaseProcessor:
    def fit(self, df: pd.DataFrame) -> "BaseProcessor": ...
    def transform(self, df: pd.DataFrame) -> pd.DataFrame: ...
    def fit_transform(self, df: pd.DataFrame) -> pd.DataFrame: ...
```

Processors can be chained into a `Pipeline`:

```python
from Forecasting.processors.cleaner import Cleaner
from Forecasting.processors.resampler import Resampler
from Forecasting.processors.feature_engineer import FeatureEngineer

pipeline = [Cleaner(), Resampler(freq="1D"), FeatureEngineer(lags=[1, 7])]

df_processed = df.copy()
for step in pipeline:
    df_processed = step.fit_transform(df_processed)
```

## Input / Output Schema

All processors expect and return a `DataFrame` with at minimum:

| Column | Type | Description |
|--------|------|-------------|
| `timestamp` | `datetime` | UTC event time (index or column) |
| `value` | `float` | Metric value |

## Contributing

1. Add a new file `<processor_name>.py` in this directory.
2. Inherit from `BaseProcessor`.
3. Add tests under `tests/forecasting/`.
4. Update this readme with the new entry in the table above.
