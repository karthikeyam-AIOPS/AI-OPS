#!/usr/bin/env python3
"""
Smart pytest runner that adapts to available plugins.
This script runs pytest with the best available configuration.
"""

import subprocess
import sys
import os


def check_plugin_available(plugin_name):
    """Check if a pytest plugin is available."""
    try:
        __import__(plugin_name.replace('-', '_'))
        return True
    except ImportError:
        return False


def build_pytest_command():
    """Build pytest command based on available plugins."""
    cmd = ["pytest"]
    
    # Base options
    cmd.extend([
        "--strict-markers",
        "-v",
        "--tb=short"
    ])
    
    # Coverage if available
    if check_plugin_available("pytest-cov"):
        cmd.extend([
            "--cov=ai_ops",
            "--cov=Forecasting", 
            "--cov-report=xml",
            "--cov-report=html",
            "--cov-report=term-missing"
        ])
        print("✅ Coverage reporting enabled")
    
    # JUnit XML output
    cmd.extend(["--junitxml=test-results.xml"])
    
    # Allure if available
    if check_plugin_available("allure-pytest"):
        cmd.extend(["--alluredir=allure-results"])
        print("✅ Allure reporting enabled")
    else:
        print("ℹ️  Allure plugin not available, skipping Allure reporting")
    
    # HTML report if available
    if check_plugin_available("pytest-html"):
        cmd.extend(["--html=pytest-report.html", "--self-contained-html"])
        print("✅ HTML reporting enabled")
    
    return cmd


def main():
    """Run pytest with optimal configuration."""
    print("🚀 Smart pytest runner")
    print("=" * 40)
    
    # Check if we have tests
    if not os.path.exists("tests"):
        print("❌ No tests directory found")
        return 1
    
    # Build command
    cmd = build_pytest_command()
    
    print(f"🧪 Running: {' '.join(cmd)}")
    print("=" * 40)
    
    # Run pytest
    try:
        result = subprocess.run(cmd, check=False)
        return result.returncode
    except KeyboardInterrupt:
        print("\n🛑 Test run interrupted")
        return 130
    except Exception as e:
        print(f"❌ Error running tests: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())