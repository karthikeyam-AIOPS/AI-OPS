"""
AI-OPS Toolkit
==============

A modular, AI-driven framework for infrastructure management, anomaly detection,
and automated remediation designed for AI-Native operations.

Core Modules:
- collectors: Data gathering from various sources (Prometheus, ELK, AWS)
- models: ML algorithms for anomaly detection, forecasting, and RCA
- processors: Data cleaning and preprocessing pipelines
- remediation: Automated healing and response actions

CLI Usage:
    aiops --help

Package Usage:
    from ai_ops import collectors, models, processors

Examples:
    See examples/ directory for practical demonstrations
"""

__version__ = "0.1.0"
__author__ = "Karthikeya Raja M"
__description__ = (
    "AI-Native Operations toolkit for infrastructure automation and ML insights"
)

# Package metadata
__all__ = ["__version__", "__author__", "__description__"]