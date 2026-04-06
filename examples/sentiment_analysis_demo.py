#!/usr/bin/env python3
"""
Log Sentiment Analysis Demo
==========================

This module demonstrates sentiment analysis for system log analysis.
It uses TextBlob to analyze the "mood" or sentiment of log messages,
which can help identify potentially problematic system states.

Note: Requires textblob package: pip install textblob

Example Usage:
    python examples/sentiment_analysis_demo.py
"""

try:
    from textblob import TextBlob
    TEXTBLOB_AVAILABLE = True
except ImportError:
    TEXTBLOB_AVAILABLE = False
    print("Warning: TextBlob not available. Install with: pip install textblob")


class LogSentimentAnalyzer:
    """
    Analyze system logs using sentiment analysis to detect potential issues.
    
    This approach treats system logs like sentences and analyzes their "emotional tone"
    to identify potentially problematic situations. Negative sentiment often correlates
    with error messages, warnings, and system failures.
    """
    
    def __init__(self, anomaly_threshold=-0.1):
        """
        Initialize the sentiment analyzer.
        
        Args:
            anomaly_threshold (float): Sentiment score below which logs are flagged as anomalies
        """
        self.anomaly_threshold = anomaly_threshold
        
        if not TEXTBLOB_AVAILABLE:
            raise ImportError("TextBlob is required for sentiment analysis. Install with: pip install textblob")
    
    def analyze_sentiment(self, log_message):
        """
        Analyze the sentiment of a single log message.
        
        Args:
            log_message (str): The log message to analyze
            
        Returns:
            dict: Contains polarity, subjectivity, and anomaly flag
        """
        blob = TextBlob(log_message)
        
        return {
            'message': log_message,
            'polarity': blob.sentiment.polarity,
            'subjectivity': blob.sentiment.subjectivity,
            'is_anomaly': blob.sentiment.polarity < self.anomaly_threshold
        }
    
    def analyze_batch(self, log_messages):
        """
        Analyze sentiment for multiple log messages.
        
        Args:
            log_messages (list): List of log messages to analyze
            
        Returns:
            list: List of analysis results for each message
        """
        return [self.analyze_sentiment(msg) for msg in log_messages]
    
    def get_summary_stats(self, results):
        """
        Get summary statistics for a batch analysis.
        
        Args:
            results (list): Results from analyze_batch()
            
        Returns:
            dict: Summary statistics
        """
        polarities = [r['polarity'] for r in results]
        anomalies = [r for r in results if r['is_anomaly']]
        
        return {
            'total_messages': len(results),
            'anomaly_count': len(anomalies),
            'anomaly_rate': len(anomalies) / len(results) if results else 0,
            'avg_polarity': sum(polarities) / len(polarities) if polarities else 0,
            'min_polarity': min(polarities) if polarities else 0,
            'max_polarity': max(polarities) if polarities else 0
        }
    
    def format_result(self, result):
        """
        Format a single analysis result for display.
        
        Args:
            result (dict): Single analysis result
            
        Returns:
            str: Formatted string for display
        """
        status = "⚠️ ANOMALY" if result['is_anomaly'] else "✅ NORMAL"
        polarity = result['polarity']
        
        # Add polarity interpretation
        if polarity > 0.3:
            mood = "Very Positive"
        elif polarity > 0.1:
            mood = "Positive"
        elif polarity > -0.1:
            mood = "Neutral"
        elif polarity > -0.3:
            mood = "Negative"
        else:
            mood = "Very Negative"
        
        return f"{status} | Sentiment: {polarity:.3f} ({mood})"


def create_mock_log_data():
    """Create mock system log data for demonstration."""
    return [
        "System boot completed successfully",
        "CRITICAL: User connection failed and database is down",
        "Info: User logged out normally",
        "WARNING: Connection timeout, system under heavy load",
        "Backup process completed without errors",
        "FATAL ERROR: Memory allocation failed",
        "User authentication successful",
        "ERROR: Failed to connect to remote server",
        "Service started successfully on port 8080",
        "ALERT: Disk usage exceeded 90% threshold",
        "Configuration updated successfully",
        "PANIC: Kernel fault detected, system unstable"
    ]


def run_sentiment_analysis_demo():
    """Run the sentiment analysis demonstration."""
    if not TEXTBLOB_AVAILABLE:
        print("Cannot run demo: TextBlob not installed")
        print("Install with: pip install textblob")
        return
    
    print("=" * 50)
    print("AI-OPS: Log Sentiment Analysis Demo")
    print("=" * 50)
    
    # Initialize analyzer
    analyzer = LogSentimentAnalyzer(anomaly_threshold=-0.1)
    
    # Get mock data
    logs = create_mock_log_data()
    
    print(f"Analyzing {len(logs)} system log messages...")
    print(f"Anomaly threshold: {analyzer.anomaly_threshold}")
    print("\n" + "=" * 60)
    
    # Analyze each log message
    results = analyzer.analyze_batch(logs)
    
    # Display individual results
    for i, result in enumerate(results, 1):
        print(f"Log {i:2d}: {result['message']}")
        print(f"        {analyzer.format_result(result)}")
        print()
    
    # Display summary statistics
    stats = analyzer.get_summary_stats(results)
    
    print("=" * 60)
    print("SUMMARY STATISTICS")
    print("=" * 60)
    print(f"Total Messages: {stats['total_messages']}")
    print(f"Anomalies Detected: {stats['anomaly_count']}")
    print(f"Anomaly Rate: {stats['anomaly_rate']:.1%}")
    print(f"Average Sentiment: {stats['avg_polarity']:.3f}")
    print(f"Sentiment Range: {stats['min_polarity']:.3f} to {stats['max_polarity']:.3f}")
    
    # Show detected anomalies
    anomalies = [r for r in results if r['is_anomaly']]
    if anomalies:
        print(f"\n" + "=" * 60)
        print("DETECTED ANOMALIES")
        print("=" * 60)
        for i, anomaly in enumerate(anomalies, 1):
            print(f"{i}. {anomaly['message']}")
            print(f"   Sentiment Score: {anomaly['polarity']:.3f}")
            print()


def explain_sentiment_analysis():
    """Explain how sentiment analysis works for log analysis."""
    print("=" * 60)
    print("HOW LOG SENTIMENT ANALYSIS WORKS")
    print("=" * 60)
    print()
    print("Architecture:")
    print("1. Input: System log message (string)")
    print("2. Processing: TextBlob uses pre-trained sentiment lexicon")
    print("3. Analysis: Words get sentiment scores, averaged for final polarity")
    print("4. Output: Polarity score from -1.0 (very negative) to +1.0 (very positive)")
    print()
    print("Logic:")
    print("• System logs are treated like sentences")
    print("• System health correlates with sentiment 'mood'")
    print("• Error keywords ('CRITICAL', 'FAILED') have negative sentiment")
    print("• Success keywords ('COMPLETED', 'SUCCESS') have positive sentiment")
    print("• Negative sentiment often indicates system problems")
    print()
    print("Use Cases:")
    print("• Real-time log monitoring and alerting")
    print("• Automated incident detection")
    print("• System health trend analysis")
    print("• Complement to traditional keyword-based monitoring")
    print()


def main():
    """Run the complete sentiment analysis demo."""
    explain_sentiment_analysis()
    print()
    run_sentiment_analysis_demo()


if __name__ == "__main__":
    main()