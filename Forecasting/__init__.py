"""
AI-OPS Forecasting Module
========================

This module contains forecasting capabilities for AI-OPS including:
- Capacity forecasting using linear regression
- Time series prediction models
- Resource usage forecasting

Examples:
    Basic usage:
        from Forecasting.capacity_forecasting_demo import CapacityInference
        
        # Load a trained model
        inference = CapacityInference('model.pkl')
        prediction = inference.predict_for_date('2026-06-01')
"""

__version__ = "0.1.0"
__author__ = "AI-OPS Team"

# Import main classes for easier access
try:
    from .capacity_forecasting_demo import (
        CapacityInference,
        generate_and_train_model,
        save_model_and_metadata
    )
except ImportError:
    # Handle cases where dependencies might not be installed
    pass