# AI-OPS Examples

This directory contains practical machine learning examples and demonstrations for the AI-OPS toolkit. Each example showcases different approaches to applying AI and ML in operations and system management contexts.

## 📁 Available Examples

### 1. Anomaly Detection Demo (`anomaly_detection_demo.py`)

**Purpose**: Demonstrates log anomaly detection using TF-IDF vectorization and Random Forest classification.

**Key Features**:
- Text-based log analysis using TF-IDF features
- Binary classification (normal vs anomaly)
- Probability scoring for anomaly likelihood
- Mock system log dataset for training

**Use Cases**:
- Security incident detection
- System failure prediction  
- Unusual pattern identification in logs
- Performance monitoring

**Example Output**:
```
Log: FATAL ERROR: Kernel panic on CPU 0
Result: ⚠️ ANOMALY (Anomaly probability: 87.3%)
```

### 2. Student Performance Prediction (`student_prediction_demo.py`)

**Purpose**: Shows different ML approaches for predicting outcomes based on multiple features.

**Key Features**:
- Pass/fail binary classification with Logistic Regression
- Multi-class grade prediction with Random Forest
- Decision boundary visualization
- Feature importance analysis
- Probability distributions for predictions

**Use Cases**:
- Resource allocation prediction
- Performance forecasting
- Multi-class categorization
- Risk assessment modeling

**Models Demonstrated**:
- **Binary Classification**: Logistic Regression for pass/fail prediction
- **Multi-class Classification**: Random Forest for letter grade prediction  

### 3. Log Sentiment Analysis (`sentiment_analysis_demo.py`)

**Purpose**: Applies sentiment analysis to system logs to detect potential issues through "emotional tone" analysis.

**Key Features**:
- TextBlob-based sentiment scoring
- Batch processing of multiple logs
- Summary statistics and anomaly detection
- Threshold-based alerting
- Detailed sentiment interpretation

**Use Cases**:
- Automated incident detection
- System health trend analysis
- Real-time log monitoring
- Complement to keyword-based monitoring

**Requirements**: `pip install textblob`

## 🚀 Running the Examples

### Run Individual Examples
```bash
# Anomaly detection
python examples/anomaly_detection_demo.py

# Student prediction (showcases general ML patterns)
python examples/student_prediction_demo.py

# Sentiment analysis
python examples/sentiment_analysis_demo.py
```

### Run All Examples
```bash
python examples/run_all_examples.py
```

### Integration with AI-OPS Package
```python
# Import from the main package (when implemented)
from ai_ops.models import AnomalyDetector
from ai_ops.collectors import LogCollector

# Or run as standalone demonstrations
```

## 📊 Example Data

All examples use mock/synthetic data for demonstration purposes:

- **Log Data**: Realistic system log messages with labeled anomalies
- **Student Data**: Academic performance metrics with various outcomes
- **Sentiment Data**: System logs with different emotional tones

## 🛠️ Dependencies

Core dependencies (automatically installed with AI-OPS):
- `pandas` - Data manipulation
- `scikit-learn` - Machine learning algorithms
- `numpy` - Numerical computing

Optional dependencies:
- `matplotlib` - Visualization (for decision boundaries)
- `textblob` - Sentiment analysis

Install optional dependencies:
```bash
pip install matplotlib textblob
```

## 🎯 Learning Objectives

These examples demonstrate:

1. **Text Analysis**: Converting unstructured log data to ML features
2. **Classification**: Binary and multi-class prediction problems
3. **Feature Engineering**: Creating meaningful features from raw data
4. **Model Evaluation**: Probability scoring and confidence measures
5. **Real-world Application**: Practical use cases in operations

## 🔄 Integration with Main Package

These examples serve as:
- **Proof of concepts** for the main AI-OPS functionality
- **Educational materials** for understanding the approaches
- **Testing grounds** for new ML techniques
- **Templates** for implementing custom solutions

The patterns demonstrated here are implemented in the main `ai_ops` package modules:
- `ai_ops.models` - ML models and algorithms
- `ai_ops.collectors` - Data collection and preprocessing
- `ai_ops.processors` - Data processing pipelines

## 📚 Next Steps

1. Explore the individual example files
2. Modify the examples with your own data
3. Check out the main AI-OPS documentation
4. Implement similar patterns in your own projects

For more information about the AI-OPS project, see the main [README.md](../README.md).