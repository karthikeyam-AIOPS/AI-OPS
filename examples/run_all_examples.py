#!/usr/bin/env python3
"""
AI-OPS Examples Runner
=====================

This script runs all the AI-OPS demonstration examples in sequence.
Each example showcases different machine learning approaches for
operations and system management.

Usage:
    python examples/run_all_examples.py
"""

import sys
from pathlib import Path

# Add the project root to the path
sys.path.insert(0, str(Path(__file__).parent.parent))


def main():
    """Run all examples in sequence."""
    print("🤖 AI-OPS Machine Learning Examples")
    print("=" * 60)
    print()
    
    examples = [
        ("Anomaly Detection", "anomaly_detection_demo"),
        ("Student Performance Prediction", "student_prediction_demo"), 
        ("Log Sentiment Analysis", "sentiment_analysis_demo")
    ]
    
    for i, (name, module_name) in enumerate(examples, 1):
        print(f"📊 Example {i}: {name}")
        print("=" * 40)
        
        try:
            module = __import__(f"examples.{module_name}", fromlist=[module_name])
            module.main()
        except ImportError as e:
            print(f"❌ Could not import {module_name}: {e}")
        except Exception as e:
            print(f"❌ Error running {module_name}: {e}")
        
        if i < len(examples):
            print("\n" + "🔹" * 60 + "\n")
    
    print("\n🎉 All examples completed!")
    print("\nFor more information about AI-OPS, see the main README.md")


if __name__ == "__main__":
    main()