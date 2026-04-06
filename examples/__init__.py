"""
AI-OPS Examples Package
=======================

This package contains demonstration examples for the AI-OPS toolkit,
showcasing various machine learning approaches for operations and system management.

Available Examples:
- anomaly_detection_demo: Log anomaly detection using ML
- student_prediction_demo: Multi-class and binary classification examples  
- sentiment_analysis_demo: Sentiment-based log analysis
- run_all_examples: Runner script for all demonstrations

Usage:
    python -m examples.run_all_examples
    
    # Or run individual examples:
    python -m examples.anomaly_detection_demo
    python -m examples.student_prediction_demo
    python -m examples.sentiment_analysis_demo
"""

__version__ = "0.1.0"
__author__ = "Karthikeya Raja M"

# Make key classes available at package level
try:
    from .anomaly_detection_demo import LogAnomalyDetector
except ImportError:
    pass

try:
    from .student_prediction_demo import PassFailPredictor, GradePredictor
except ImportError:
    pass

try:
    from .sentiment_analysis_demo import LogSentimentAnalyzer
except ImportError:
    pass

__all__ = [
    'LogAnomalyDetector',
    'PassFailPredictor', 
    'GradePredictor',
    'LogSentimentAnalyzer'
]