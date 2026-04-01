# GitHub Actions CI/CD Setup for AI-OPS

This document explains the GitHub Actions workflows that have been set up for your AI-OPS project.

## 📋 Overview

Two GitHub Actions workflows have been created:

1. **`build.yml`** - Main build, test, and deployment pipeline
2. **`code-quality.yml`** - Quick code quality checks for pull requests

## 🔧 Workflows Explained

### Main Build Workflow (`.github/workflows/build.yml`)

**Triggers:**
- Push to `main` or `develop` branches
- Pull requests to `main` or `develop` branches
- Manual dispatch via GitHub UI

**What it does:**
- **Multi-Python Testing**: Tests against Python 3.9, 3.10, 3.11, and 3.12
- **Dependency Caching**: Caches pip dependencies for faster builds
- **Code Quality**: Runs flake8, black, and isort checks
- **Package Validation**: Installs package and validates imports
- **Build Testing**: Creates distribution packages
- **CLI Testing**: Tests CLI functionality (when `main.py` exists)
- **Test Execution**: Runs pytest with coverage (when tests exist)
- **Security Scanning**: Runs safety and bandit security checks
- **Docker Build**: Creates and tests Docker container
- **Coverage Reporting**: Uploads coverage to Codecov

### Code Quality Workflow (`.github/workflows/code-quality.yml`)

**Triggers:**
- Pull requests that modify Python files
- Manual dispatch

**What it does:**
- **Black**: Code formatting validation
- **isort**: Import sorting validation  
- **Flake8**: PEP 8 compliance and error checking
- **MyPy**: Type checking (continues on error)

## 🚀 Getting Started

### 1. Enable GitHub Actions
Your workflows are ready to run! Just push to your repository and they'll trigger automatically.

### 2. Set up Codecov (Optional)
For coverage reporting:
1. Go to [codecov.io](https://codecov.io)
2. Connect your GitHub repository
3. Copy the upload token (if needed)

### 3. Create Missing Files
The workflows are designed to handle missing components gracefully, but to get full functionality:

**Create `ai_ops/main.py`:**
```python
import typer
from rich.console import Console

app = typer.Typer(
    name="ai-ops",
    help="AI-Native Operations toolkit for infrastructure automation"
)
console = Console()

@app.command()
def version():
    """Show version information"""
    console.print("AI-OPS v0.1.0", style="bold green")

@app.command() 
def health():
    """Check system health"""
    console.print("✅ AI-OPS is running!", style="bold green")

if __name__ == "__main__":
    app()
```

**Create test files in `tests/`:**
```python
# tests/test_basic.py
import pytest
from ai_ops import __version__

def test_version():
    assert __version__ is not None

def test_import():
    import ai_ops
    assert ai_ops is not None
```

### 4. Local Development Setup

**Install development dependencies:**
```bash
pip install -e .[dev]
pip install pytest black isort flake8 mypy
```

**Run quality checks locally:**
```bash
# Format code
black ai_ops tests

# Sort imports
isort ai_ops tests

# Check linting
flake8 ai_ops

# Type checking  
mypy ai_ops

# Run tests
pytest tests/ --cov=ai_ops
```

## 📊 Status Badges

Add these to your README.md to show build status:

```markdown
![Build Status](https://github.com/karthikeyam-AIOPS/AI-OPS/workflows/Build%20and%20Test%20AI-OPS/badge.svg)
![Code Quality](https://github.com/karthikeyam-AIOPS/AI-OPS/workflows/Code%20Quality%20Check/badge.svg)
[![codecov](https://codecov.io/gh/karthikeyam-AIOPS/AI-OPS/branch/main/graph/badge.svg)](https://codecov.io/gh/karthikeyam-AIOPS/AI-OPS)
```

## 🔧 Configuration Files

The following configuration has been added to your `project.toml`:

- **Black**: Code formatting (88 char line length)
- **isort**: Import sorting (compatible with Black)
- **pytest**: Test configuration
- **coverage**: Coverage reporting configuration  
- **mypy**: Type checking configuration

## 🐳 Docker Support

A Dockerfile is automatically generated if one doesn't exist. To build locally:

```bash
docker build -t ai-ops .
docker run --rm ai-ops
```

## 📝 Next Steps

1. **Create `ai_ops/main.py`** to enable CLI testing
2. **Add test files** in the `tests/` directory
3. **Set up branch protection** rules in GitHub requiring CI to pass
4. **Configure Codecov** for coverage reporting
5. **Add status badges** to your README

## 🔍 Troubleshooting

**Workflow fails on missing dependencies:**
- Check that all dependencies in `project.toml` are correctly specified
- Ensure Python version compatibility

**CLI tests fail:**
- Make sure `ai_ops/main.py` exists with proper Typer setup
- Verify the entry point in `project.toml` is correct

**Security scans report issues:**
- Review the safety and bandit reports
- Update dependencies with known vulnerabilities
- Add security exceptions if needed

The workflows are designed to be robust and will continue running even if some components (like tests or CLI) aren't ready yet. This allows you to iterate and improve your codebase while maintaining CI/CD functionality.