# Forecasting / remediation

See the project [README.md](../../README.md) for full documentation.

## Planned Remediators

| Remediator | File | Action |
|------------|------|--------|
| Alert Sender | `alerting.py` | Send PagerDuty / Slack / email alert |
| Auto-Scaler | `autoscaler.py` | Trigger Kubernetes HPA or cloud auto-scaling |
| Disk Archiver | `disk_archiver.py` | Move cold data to object storage (S3 / GCS) |
| Ticket Creator | `ticketing.py` | Open a Jira / ServiceNow incident ticket |
| Runbook Executor | `runbook.py` | Run a predefined shell or Ansible runbook |

## Interface Convention

```python
class BaseRemediator:
    def should_trigger(self, forecast: pd.DataFrame) -> bool: ...
    def execute(self, forecast: pd.DataFrame) -> dict: ...
```

`execute()` returns an action receipt:

```python
{
    "action": "auto_scale",
    "triggered_at": "2026-04-16T12:00:00Z",
    "details": {"replicas_added": 3, "cluster": "prod-k8s-eu"},
    "status": "success"
}
```

## Usage (example)

```python
from Forecasting.remediation.autoscaler import AutoScaler

scaler = AutoScaler(
    threshold_pct=85,          # trigger when forecast exceeds 85% capacity
    cluster="prod-k8s-eu",
    max_replicas=20,
)

if scaler.should_trigger(forecast_df):
    receipt = scaler.execute(forecast_df)
    print(f"Scaled: {receipt}")
```

## Threshold Configuration

Thresholds can be set per remediator or loaded from a shared config file:

```yaml
# forecasting_config.yaml
remediation:
  alert_threshold_pct: 80
  scale_threshold_pct: 85
  archive_threshold_pct: 90
```

## Contributing

1. Add a new file `<remediator_name>.py` in this directory.
2. Inherit from `BaseRemediator`.
3. Add tests under `tests/forecasting/`.
4. Update this readme with the new entry in the table above.
