# ai_ops / collectors

See the project [README.md](../../README.md) for full documentation.

## Planned Collectors

| Collector | Source | Description |
|-----------|--------|-------------|
| `prometheus.py` | Prometheus / VictoriaMetrics | Scrapes metrics via the HTTP API |
| `elk.py` | Elasticsearch / OpenSearch | Queries logs from ELK/OpenSearch stacks |
| `aws.py` | AWS CloudWatch | Pulls CloudWatch metrics and log groups |
| `k8s.py` | Kubernetes API | Reads pod/node events and resource usage |
| `syslog.py` | Syslog / journald | Tails system logs from Linux hosts |

## Interface Convention

Every collector should implement the following interface:

```python
class BaseCollector:
    def connect(self) -> None: ...
    def collect(self, start: datetime, end: datetime) -> pd.DataFrame: ...
    def close(self) -> None: ...
```

The returned `DataFrame` should contain at minimum:

| Column | Type | Description |
|--------|------|-------------|
| `timestamp` | `datetime` | UTC event time |
| `source` | `str` | Originating host or service |
| `metric` | `str` | Metric or log field name |
| `value` | `float \| str` | Observed value |

## Usage (example)

```python
from ai_ops.collectors.prometheus import PrometheusCollector
from datetime import datetime, timedelta

collector = PrometheusCollector(base_url="http://prometheus:9090")
collector.connect()

df = collector.collect(
    start=datetime.utcnow() - timedelta(hours=1),
    end=datetime.utcnow(),
)
print(df.head())
collector.close()
```

## Contributing

1. Add a new file `<source>.py` in this directory.
2. Inherit from `BaseCollector`.
3. Add tests under `tests/collectors/`.
4. Update this readme with the new entry in the table above.
