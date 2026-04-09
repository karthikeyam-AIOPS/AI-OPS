#!/usr/bin/env python3
"""
AI-OPS Report Generator
======================

This script helps generate and manage SonarQube and Allure reports locally.
Run this script to generate comprehensive quality and test reports.

Usage:
    python scripts/generate_reports.py [--allure] [--sonar] [--serve]
"""

import subprocess
import sys
import argparse
import os
import shutil
from pathlib import Path


def run_command(command, description="", check=True):
    """Run a shell command with error handling."""
    print(f"{'='*50}")
    print(f"📋 {description}")
    print(f"🔧 Command: {command}")
    print(f"{'='*50}")
    
    try:
        result = subprocess.run(command, shell=True, check=check, capture_output=False)
        if result.returncode == 0:
            print(f"✅ {description} - SUCCESS")
        else:
            print(f"❌ {description} - FAILED (exit code: {result.returncode})")
        return result.returncode == 0
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} - FAILED: {e}")
        return False


def clean_reports():
    """Clean existing report directories."""
    print("🧹 Cleaning existing reports...")
    
    dirs_to_clean = [
        "allure-results",
        "allure-report", 
        "htmlcov",
        ".sonar",
        "coverage.xml",
        "test-results.xml"
    ]
    
    for dir_path in dirs_to_clean:
        if os.path.exists(dir_path):
            if os.path.isdir(dir_path):
                shutil.rmtree(dir_path)
                print(f"🗑️  Removed directory: {dir_path}")
            else:
                os.remove(dir_path)
                print(f"🗑️  Removed file: {dir_path}")


def run_tests_with_allure():
    """Run tests and generate Allure report."""
    print("🧪 Running tests with Allure reporting...")
    
    # Install dependencies
    run_command("pip install -e \".[dev]\"", "Installing development dependencies")
    
    # Check if allure-pytest is available
    try:
        import allure_pytest
        allure_available = True
        print("✅ Allure plugin detected")
    except ImportError:
        allure_available = False
        print("⚠️  Allure plugin not available, running tests without Allure")
    
    # Run tests with or without Allure
    if allure_available:
        success = run_command(
            "pytest --cov=ai_ops --cov-report=xml --cov-report=html --alluredir=allure-results --junitxml=test-results.xml",
            "Running tests with coverage and Allure"
        )
    else:
        success = run_command(
            "pytest --cov=ai_ops --cov-report=xml --cov-report=html --junitxml=test-results.xml",
            "Running tests with coverage (no Allure)"
        )
    
    # Generate Allure report if results exist and CLI is available
    if success and allure_available and os.path.exists("allure-results"):
        if shutil.which("allure"):
            # Generate Allure report
            run_command(
                "allure generate allure-results --clean --output allure-report",
                "Generating Allure HTML report"
            )
            print("📊 Allure report generated at: allure-report/index.html")
        else:
            print("⚠️  Allure CLI not found. Install it to generate HTML reports.")
            print("   Install: https://docs.qameta.io/allure/#_installing_a_commandline")
    else:
        print("📊 Tests completed. Coverage report available at: htmlcov/index.html")


def run_sonar_scan():
    """Run SonarQube scan."""
    print("🔍 Running SonarQube analysis...")
    
    if not shutil.which("sonar-scanner"):
        print("⚠️  SonarQube Scanner not found.")
        print("   Please install SonarQube Scanner CLI:")
        print("   https://docs.sonarqube.org/latest/analysis/scan/sonarscanner/")
        return False
        
    # Check if sonar-project.properties exists
    if not os.path.exists("sonar-project.properties"):
        print("❌ sonar-project.properties not found!")
        return False
    
    # Run SonarQube scan
    return run_command(
        "sonar-scanner",
        "Running SonarQube analysis"
    )


def serve_reports(port=8080):
    """Serve reports locally."""
    print(f"🌐 Starting local server on port {port}...")
    
    if os.path.exists("allure-report"):
        try:
            run_command(
                f"python -m http.server {port} --directory allure-report",
                f"Serving Allure report at http://localhost:{port}",
                check=False
            )
        except KeyboardInterrupt:
            print("\n🛑 Server stopped.")
    else:
        print("❌ No Allure report found. Run with --allure first.")


def main():
    """Main function."""
    parser = argparse.ArgumentParser(description="Generate AI-OPS quality reports")
    parser.add_argument("--allure", action="store_true", help="Generate Allure test reports")
    parser.add_argument("--sonar", action="store_true", help="Run SonarQube analysis")
    parser.add_argument("--serve", action="store_true", help="Serve reports locally")
    parser.add_argument("--clean", action="store_true", help="Clean existing reports")
    parser.add_argument("--all", action="store_true", help="Run all report generation")
    parser.add_argument("--port", type=int, default=8080, help="Port for local server")
    
    args = parser.parse_args()
    
    if not any([args.allure, args.sonar, args.serve, args.clean, args.all]):
        args.all = True  # Default to all if no specific option
    
    print("🚀 AI-OPS Report Generator")
    print("=" * 50)
    
    if args.clean or args.all:
        clean_reports()
    
    if args.allure or args.all:
        run_tests_with_allure()
    
    if args.sonar or args.all:
        run_sonar_scan()
    
    if args.serve:
        serve_reports(args.port)
    
    print("\n🎉 Report generation completed!")
    print(f"\n📊 View reports:")
    if os.path.exists("allure-report"):
        print(f"   📈 Allure Report: allure-report/index.html")
    if os.path.exists("htmlcov"):
        print(f"   📋 Coverage Report: htmlcov/index.html")


if __name__ == "__main__":
    main()