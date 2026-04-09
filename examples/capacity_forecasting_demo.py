import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
import joblib
import json
from datetime import datetime


def generate_and_train_model():
    """Generate historical data and train a linear regression model for capacity forecasting."""
    # 1. Existing Historical Data (Day 1 to 30)
    days_hist = np.array(range(1, 31)).reshape(-1, 1)
    gb_hist = np.array([100 + 1.5 * i + np.random.normal(0, 2) for i in range(30)]).reshape(-1, 1)

    # 2. Train the Model
    model = LinearRegression().fit(days_hist, gb_hist)

    # 3. Generate Future Data (Day 31 to 40)
    days_future = np.array(range(31, 41)).reshape(-1, 1)
    gb_future = np.array(model.predict(days_future))

    # 4. Combine them using NumPy
    all_days = np.vstack((days_hist, days_future))
    all_gb = np.vstack((gb_hist, gb_future))

    # 5. Create a labeled DataFrame for clear printing
    df = pd.DataFrame({
        'Day': all_days.flatten(),
        'GB_Used': all_gb.flatten(),
        'Type': ['Actual'] * 30 + ['Forecast'] * 10
    })

    # Print the transition (last 5 actuals and all 10 forecasts)
    print("Capacity Forecast Results:")
    print("=" * 50)
    print(df.tail(15).to_string(index=False))
    
    return model, days_hist, gb_hist, gb_future


def save_model_and_metadata(model, days_hist, gb_hist, gb_future):
    """Save the model and capture metadata."""
    # Save the model to a file
    joblib.dump(model, 'cpu_forecast_model.pkl')
    print(f"\nModel saved to: cpu_forecast_model.pkl")

    # Capture the mathematical attributes
    slope = model.coef_[0][0]
    intercept = model.intercept_[0]
    r_squared = model.score(days_hist, gb_hist)

    print(f"\nModel Captured:")
    print(f"- Growth Rate: {slope:.2f} GB per day")
    print(f"- Starting Point: {intercept:.2f} GB")
    print(f"- Accuracy Score (R2): {r_squared:.4f}")

    model_metadata = {
        "model_type": "LinearRegression",
        "last_trained": "2026-04-09",
        "parameters": {
            "slope": slope,
            "intercept": intercept
        },
        "performance": {
            "r_squared": r_squared
        },
        "forecast_summary": {
            "next_7_days_avg": np.mean(gb_future[:7])
        }
    }

    # Save metadata to JSON file
    with open('model_metadata.json', 'w') as f:
        json.dump(model_metadata, f, indent=4)
    
    print(f"\nModel Metadata:")
    print(json.dumps(model_metadata, indent=4))
    
    return model_metadata


class CapacityInference:
    """Class for making capacity predictions using a trained model."""
    
    def __init__(self, model_path):
        # Load the saved model logic
        self.model = joblib.load(model_path)
        # In a real app, you'd store the 'Start Date' of your training
        self.training_start_date = datetime(2026, 1, 1) 

    def get_days_since_start(self, target_date):
        """Calculate days since training start date."""
        delta = target_date - self.training_start_date
        return delta.days

    def predict_for_date(self, target_date_str):
        """Predict capacity usage for a specific date."""
        target_date = datetime.strptime(target_date_str, '%Y-%m-%d')
        day_index = self.get_days_since_start(target_date)
        
        # Reshape for scikit-learn [[value]]
        prediction = self.model.predict([[day_index]])[0][0]
        return round(prediction, 2)

    def predict_range(self, start_date_str, end_date_str):
        """Predict capacity usage for a date range."""
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d')
        
        predictions = []
        current_date = start_date
        while current_date <= end_date:
            day_index = self.get_days_since_start(current_date)
            prediction = self.model.predict([[day_index]])[0][0]
            predictions.append({
                'date': current_date.strftime('%Y-%m-%d'),
                'predicted_gb': round(prediction, 2)
            })
            current_date = datetime(current_date.year, current_date.month, current_date.day + 1)
        
        return predictions


def main():
    """Main function to demonstrate capacity forecasting."""
    print("AI-OPS Capacity Forecasting Demo")
    print("=" * 40)
    
    # Generate data and train model
    model, days_hist, gb_hist, gb_future = generate_and_train_model()
    
    # Save model and metadata
    metadata = save_model_and_metadata(model, days_hist, gb_hist, gb_future)
    
    # Demonstrate inference
    print(f"\n{'='*50}")
    print("Capacity Inference Demo")
    print("=" * 50)
    
    try:
        # Create inference object
        inference = CapacityInference('cpu_forecast_model.pkl')
        
        # Single date prediction
        future_val = inference.predict_for_date('2026-06-01')
        print(f"Forecast for June 1st, 2026: {future_val} GB")
        
        # Range prediction
        print(f"\nForecast for next week:")
        weekly_forecast = inference.predict_range('2026-04-10', '2026-04-16')
        for pred in weekly_forecast:
            print(f"  {pred['date']}: {pred['predicted_gb']} GB")
            
    except FileNotFoundError:
        print("Model file not found. Please run the training section first.")
    except Exception as e:
        print(f"Error during inference: {str(e)}")


if __name__ == "__main__":
    main()