#!/usr/bin/env python3
"""
Student Performance Prediction Demo
==================================

This module demonstrates various machine learning approaches for predicting
student performance, including pass/fail prediction and multi-class grading.

Example Usage:
    python examples/student_prediction_demo.py
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split


def create_pass_fail_data():
    """Create mock pass/fail student data."""
    data = {
        'hours_studied': [2, 8, 3, 7, 5, 1, 9, 4, 6, 2],
        'attendance_pct': [50, 90, 60, 85, 75, 40, 95, 65, 80, 55],
        'result': [0, 1, 0, 1, 1, 0, 1, 0, 1, 0]  # 0=Fail, 1=Pass
    }
    return pd.DataFrame(data)


def create_detailed_grading_data():
    """Create mock detailed grading data."""
    data = {
        'internals': [38, 25, 30, 15, 35, 20, 10, 39, 28, 5],
        'externals': [58, 45, 40, 30, 52, 35, 20, 59, 42, 10],
        'attendance': [95, 80, 85, 70, 92, 75, 60, 98, 88, 40],
        'grade': ['S', 'B', 'B', 'C', 'A', 'C', 'F', 'S', 'B', 'F']
    }
    return pd.DataFrame(data)


class PassFailPredictor:
    """Binary classifier for student pass/fail prediction."""
    
    def __init__(self):
        """Initialize the predictor."""
        self.model = LogisticRegression(random_state=42)
        self.is_trained = False
    
    def train(self, features, labels):
        """
        Train the pass/fail model.
        
        Args:
            features (DataFrame): Student features (hours_studied, attendance_pct)
            labels (Series): Binary labels (0=Fail, 1=Pass)
        """
        self.model.fit(features, labels)
        self.is_trained = True
        print("Pass/Fail model training complete")
    
    def predict(self, features):
        """Predict pass/fail for new students."""
        if not self.is_trained:
            raise ValueError("Model must be trained before making predictions")
        
        return self.model.predict(features)
    
    def predict_proba(self, features):
        """Get probability of passing for new students."""
        if not self.is_trained:
            raise ValueError("Model must be trained before making predictions")
        
        return self.model.predict_proba(features)[:, 1]
    
    def plot_decision_boundary(self, df):
        """Plot the decision boundary for visualization."""
        if not self.is_trained:
            raise ValueError("Model must be trained before plotting")
        
        # Get model parameters
        b = self.model.intercept_[0]
        w1, w2 = self.model.coef_[0]
        
        # Calculate decision boundary
        hours_range = np.linspace(0, 10, 100)
        boundary_attendance = -(w1 * hours_range + b) / w2
        
        # Create plot
        plt.figure(figsize=(10, 6))
        
        # Plot data points
        fail_students = df[df['result'] == 0]
        pass_students = df[df['result'] == 1]
        
        plt.scatter(fail_students['hours_studied'], fail_students['attendance_pct'], 
                   color='red', label='Fail', s=100, alpha=0.7)
        plt.scatter(pass_students['hours_studied'], pass_students['attendance_pct'], 
                   color='green', label='Pass', s=100, alpha=0.7)
        
        # Plot decision boundary
        plt.plot(hours_range, boundary_attendance, 'b--', 
                label='Decision Boundary (50% Pass Probability)', linewidth=2)
        
        plt.xlabel('Hours Studied')
        plt.ylabel('Attendance %')
        plt.title('Pass/Fail Decision Boundary')
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.xlim(0, 10)
        plt.ylim(30, 100)
        
        return plt


class GradePredictor:
    """Multi-class classifier for detailed grade prediction."""
    
    def __init__(self, n_estimators=100):
        """Initialize the grade predictor."""
        self.model = RandomForestClassifier(n_estimators=n_estimators, random_state=42)
        self.is_trained = False
    
    def train(self, features, grades):
        """
        Train the grading model.
        
        Args:
            features (DataFrame): Student features
            grades (Series): Letter grades
        """
        self.model.fit(features, grades)
        self.is_trained = True
        print("Grade prediction model training complete")
    
    def predict(self, features):
        """Predict grades for new students."""
        if not self.is_trained:
            raise ValueError("Model must be trained before making predictions")
        
        return self.model.predict(features)
    
    def predict_proba(self, features):
        """Get probability distribution over all grades."""
        if not self.is_trained:
            raise ValueError("Model must be trained before making predictions")
        
        return self.model.predict_proba(features)
    
    def get_feature_importance(self, feature_names):
        """Get feature importance rankings."""
        if not self.is_trained:
            raise ValueError("Model must be trained before checking importance")
        
        importances = self.model.feature_importances_
        importance_df = pd.DataFrame({
            'feature': feature_names,
            'importance': importances
        }).sort_values('importance', ascending=False)
        
        return importance_df


def run_pass_fail_demo():
    """Run the pass/fail prediction demo."""
    print("=" * 40)
    print("Pass/Fail Prediction Demo")
    print("=" * 40)
    
    # Create and show data
    df = create_pass_fail_data()
    print("Student Pass/Fail Data:")
    print(df)
    
    # Prepare features
    X = df[['hours_studied', 'attendance_pct']]
    y = df['result']
    
    # Train model
    predictor = PassFailPredictor()
    predictor.train(X, y)
    
    # Test on new students
    print("\n" + "=" * 30)
    print("Predicting for New Students")
    print("=" * 30)
    
    new_students = pd.DataFrame({
        'hours_studied': [7, 2, 5],
        'attendance_pct': [82, 45, 70]
    })
    
    predictions = predictor.predict(new_students)
    probabilities = predictor.predict_proba(new_students)
    
    for i, pred in enumerate(predictions):
        status = "PASS ✅" if pred == 1 else "FAIL ❌"
        hours = new_students.iloc[i]['hours_studied']
        attendance = new_students.iloc[i]['attendance_pct']
        prob = probabilities[i]
        
        print(f"Student {i+1}: {hours}h studied, {attendance}% attendance")
        print(f"Result: {status} (Pass probability: {prob:.2%})")
        print()
    
    # Plot decision boundary
    try:
        predictor.plot_decision_boundary(df)
        print("Decision boundary plot created (if matplotlib is available)")
    except ImportError:
        print("Matplotlib not available for plotting")


def run_grading_demo():
    """Run the detailed grading demo."""
    print("=" * 40)
    print("Detailed Grade Prediction Demo")
    print("=" * 40)
    
    # Create and show data
    df = create_detailed_grading_data()
    print("Detailed Student Records:")
    print(df.head())
    
    # Prepare data
    X = df[['internals', 'externals', 'attendance']]
    y = df['grade']
    
    # Train model
    predictor = GradePredictor()
    predictor.train(X, y)
    
    # Show feature importance
    importance = predictor.get_feature_importance(X.columns)
    print(f"\nFeature Importance:")
    for _, row in importance.iterrows():
        print(f"{row['feature']}: {row['importance']:.3f}")
    
    # Test on new student
    print("\n" + "=" * 30)
    print("Predicting Grade for New Student")
    print("=" * 30)
    
    new_student = pd.DataFrame([[32, 48, 76]], 
                              columns=['internals', 'externals', 'attendance'])
    
    predicted_grade = predictor.predict(new_student)[0]
    probabilities = predictor.predict_proba(new_student)[0]
    
    print("Student Profile: 32/40 internals, 48/60 externals, 76% attendance")
    print(f"Predicted Grade: {predicted_grade}")
    print(f"\nGrade Probabilities:")
    
    for grade, prob in zip(predictor.model.classes_, probabilities):
        print(f"  Grade {grade}: {prob:.2%}")


def main():
    """Run both demos."""
    print("AI-OPS: Student Performance Prediction Demos\n")
    
    run_pass_fail_demo()
    print("\n" + "="*60 + "\n")
    run_grading_demo()


if __name__ == "__main__":
    main()