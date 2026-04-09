# AI-OPS Toolkit 🚀

[![Basic CI](https://github.com/karthikeyam-AIOPS/AI-OPS/actions/workflows/basic-ci.yml/badge.svg)](https://github.com/karthikeyam-AIOPS/AI-OPS/actions/workflows/basic-ci.yml)
[![Code Quality](https://github.com/karthikeyam-AIOPS/AI-OPS/actions/workflows/code-quality.yml/badge.svg)](https://github.com/karthikeyam-AIOPS/AI-OPS/actions/workflows/code-quality.yml)

A modular, AI-driven framework for infrastructure management, anomaly detection, and automated remediation. This tool is designed to move our operations toward an **AI-Native** standard.

    AI-OPS/
    ├── ai_ops/                  # Primary Package Source
    │   ├── __init__.py          # Makes this a Python package
    │   ├── main.py              # CLI Entry point (Typer/Click logic)
    │   ├── collectors/          # Data fetching (Prometheus, ELK, S3)
    │   ├── models/              # ML Logic (#1 Log Parsing, #2 Forecasting, #3 RCA)
    │   ├── processors/          # Data cleaning & Log parsing
    │   ├── remediation/         # Self-healing (Ansible, Boto3, Terraform)
    │   └── utils.py             # Shared helpers (Config, Logging)
    ├── tests/                   # Unit tests for the team
    ├── pyproject.toml           # Package metadata & Dependencies
    └── README.md                # Documentation for the team

## 🏗 Architecture
- **CLI (`main.py`):** The primary interface for engineers.
- **Collectors:** Modules to pull data from Prometheus, ELK, and AWS.
- **Models:** Scikit-learn based anomaly detection and forecasting.
- **Remediation:** Automated Boto3 and Ansible scripts for self-healing.

## 🛠 Installation

Clone the repository:
```bash
git clone https://github.com/karthikeyam-AIOPS/AI-OPS.git
cd AI-OPS

# Package Installation
pip install -e .

# Install with development dependencies (for testing and reporting)
pip install -e ".[dev]"

# Verify Installation
aiops --help
aiops status
```

## 🚀 Quick Start

```bash
# Check system status
aiops status

# Run examples
aiops examples
aiops forecast

# Run tests
aiops test
# OR
python scripts/run_tests.py
```

## 📚 Examples & Demos

The `examples/` directory contains practical demonstrations of AI-OPS capabilities:

- **Anomaly Detection**: Log analysis using ML for incident detection
- **Performance Prediction**: Multi-class classification examples  
- **Sentiment Analysis**: System health monitoring through log sentiment

Run all examples:
```bash
python examples/run_all_examples.py
```

Or install with example dependencies:
```bash
pip install -e ".[examples]"
```

See [examples/README.md](examples/README.md) for detailed documentation.

## 🤝 Contributing

1. Create a feature branch: git checkout -b feature/your-feature-name
2. Ensure your logic is placed in the correct directory (models/, collectors/, etc.)
3. Add a new @app.command() in ai_ops/main.py.
4. Open a Pull Request.


## Next Steps for You:
1. **Initialize the `__init__.py` files:** Keep them empty for now; they just tell Python to treat those folders as packages.
2. **Move your scripts:** Place your existing logic into the subfolders (e.g., put your Vertica or Redshift migration scripts into `remediation/` or `processors/`).
3. **Internal Launch:** you can now share this repo and have everyone run `pip install -e . 
