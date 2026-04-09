# Forecasting Module

This module contains predictive forecasting capabilities for AI-OPS operations.

## 📊 Components

### Core Forecasting
- **[capacity_forecasting_demo.py](capacity_forecasting_demo.py)** - Complete capacity forecasting implementation with linear regression
  
### Supporting Modules
- **[processors/](processors/)** - Data processing utilities for forecasting models
- **[remediation/](remediation/)** - Automated remediation actions based on forecasts

## 🚀 Quick Start

### Run Capacity Forecasting Demo
```bash
# From project root
python Forecasting/capacity_forecasting_demo.py
```

### Use in Your Code
```python
from Forecasting import CapacityInference

# Load a trained model
inference = CapacityInference('cpu_forecast_model.pkl')

# Make predictions
prediction = inference.predict_for_date('2026-06-01')
print(f"Expected usage: {prediction} GB")

# Range predictions
weekly_forecast = inference.predict_range('2026-04-10', '2026-04-16')
for pred in weekly_forecast:
    print(f"{pred['date']}: {pred['predicted_gb']} GB")
```

## 📈 Features

- **Time Series Forecasting**: Linear regression models for capacity growth
- **Model Persistence**: Save and load trained models with joblib
- **Date-based Interface**: Real-world date input for business-friendly forecasting
- **Metadata Tracking**: Capture model performance and parameters
- **Range Predictions**: Forecast across multiple dates efficiently

## 🔧 Dependencies

- numpy
- pandas  
- scikit-learn
- joblib

## 📋 Use Cases

- Storage capacity planning
- CPU/Memory usage forecasting
- Infrastructure scaling decisions
- Budget planning for resource expansion
- Proactive capacity management