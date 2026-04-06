#!/usr/bin/env python3
"""
Anomaly Detection Demo for AI-OPS
=================================

This module demonstrates log anomaly detection using TF-IDF vectorization
and Random Forest classification. It's designed to identify unusual patterns
in system logs that might indicate issues or security threats.

Example Usage:
    python examples/anomaly_detection_demo.py
"""

import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report


def create_mock_log_data():
    """Create a mock dataset of system logs for demonstration."""
    data = {
        'log_message': [
            "User login successful for user_123",
            "Connection established to database_prod",
            "GET /home HTTP/1.1 200",
            "Backup started at 02:00 AM",
            "File uploaded successfully: image.png",
            "CRITICAL: Disk space low on /dev/sda1",  # Anomaly
            "User login failed: Invalid password",
            "POST /api/v1/update HTTP/1.1 200",
            "Connection timeout after 30s",          # Anomaly
            "Memory usage exceeded 95% threshold",   # Anomaly
            "User logout successful",
            "GET /assets/style.css HTTP/1.1 200",
            "FATAL ERROR: Kernel panic detected"     # Anomaly
        ],
        'is_anomaly': [0, 0, 0, 0, 0, 1, 0, 0, 1, 1, 0, 0, 1]  # 0 = Normal, 1 = Anomaly
    }
    
    return pd.DataFrame(data)


class LogAnomalyDetector:
    """
    A simple log anomaly detector using TF-IDF and Random Forest.
    """
    
    def __init__(self, n_estimators=100):
        """
        Initialize the detector.
        
        Args:
            n_estimators (int): Number of trees in the Random Forest
        """
        self.vectorizer = TfidfVectorizer(lowercase=True, stop_words='english')
        self.model = RandomForestClassifier(n_estimators=n_estimators, random_state=42)
        self.is_trained = False
    
    def train(self, log_messages, labels):
        """
        Train the anomaly detector.
        
        Args:
            log_messages (list): List of log message strings
            labels (list): List of binary labels (0=normal, 1=anomaly)
        """
        # Convert text to TF-IDF features
        X = self.vectorizer.fit_transform(log_messages)
        
        # Train the model
        self.model.fit(X, labels)
        self.is_trained = True
        
        print(f"Model trained on {len(log_messages)} log entries")
        print(f"Feature matrix shape: {X.shape}")
    
    def predict(self, log_messages):
        """
        Predict anomalies in new log messages.
        
        Args:
            log_messages (list): List of log message strings to analyze
            
        Returns:
            list: Predictions (0=normal, 1=anomaly)
        """
        if not self.is_trained:
            raise ValueError("Model must be trained before making predictions")
        
        # Transform new messages using the fitted vectorizer
        X = self.vectorizer.transform(log_messages)
        
        return self.model.predict(X)
    
    def predict_proba(self, log_messages):
        """
        Get prediction probabilities for log messages.
        
        Args:
            log_messages (list): List of log message strings to analyze
            
        Returns:
            array: Probability scores for each class
        """
        if not self.is_trained:
            raise ValueError("Model must be trained before making predictions")
        
        X = self.vectorizer.transform(log_messages)
        return self.model.predict_proba(X)


def main():
    """Run the anomaly detection demo."""
    print("=" * 50)
    print("AI-OPS: Log Anomaly Detection Demo")
    print("=" * 50)
    
    # 1. Create mock dataset
    df = create_mock_log_data()
    print(f"Dataset Size: {df.shape[0]} logs")
    print(f"Normal logs: {(df['is_anomaly'] == 0).sum()}")
    print(f"Anomaly logs: {(df['is_anomaly'] == 1).sum()}")
    
    # 2. Initialize and train detector
    detector = LogAnomalyDetector()
    detector.train(df['log_message'], df['is_anomaly'])
    
    # 3. Test on new logs
    print("\n" + "=" * 30)
    print("Testing on New Logs")  
    print("=" * 30)
    
    test_logs = [
        "User login successful for user_456",
        "FATAL ERROR: Kernel panic on CPU 0",
        "Connection established to backup_server",
        "CRITICAL: Memory leak detected in process_xyz"
    ]
    
    predictions = detector.predict(test_logs)
    probabilities = detector.predict_proba(test_logs)
    
    for i, (log, pred) in enumerate(zip(test_logs, predictions)):
        anomaly_prob = probabilities[i][1]  # Probability of being an anomaly
        status = "⚠️ ANOMALY" if pred == 1 else "✅ NORMAL"
        print(f"\nLog: {log}")
        print(f"Result: {status} (Anomaly probability: {anomaly_prob:.2%})")


if __name__ == "__main__":
    main()