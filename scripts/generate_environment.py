#!/usr/bin/env python3
"""
Generate environment.properties for Allure reports.
This script creates environment information for Allure test reports.
"""

import platform
import sys
from datetime import datetime
from pathlib import Path


def generate_environment_properties():
    """Generate environment.properties file for Allure reports."""
    
    env_content = f"""# Environment Information for Allure Reports
# Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

# System Information
OS={platform.system()}
OS_Version={platform.release()}
Architecture={platform.architecture()[0]}
Machine={platform.machine()}
Processor={platform.processor()}

# Python Information  
Python_Version={sys.version.split()[0]}
Python_Implementation={platform.python_implementation()}

# Project Information
Project=AI-OPS Toolkit
Version=0.1.0
Environment=Development

# Test Configuration
Test_Framework=pytest
Reporting=Allure
Coverage_Tool=coverage.py

# CI/CD Information (will be overridden in CI)
CI=false
Build_URL=local
Branch=local
Commit=local
"""
    
    # Create allure-results directory if it doesn't exist
    results_dir = Path("allure-results")
    results_dir.mkdir(exist_ok=True)
    
    # Write environment.properties
    env_file = results_dir / "environment.properties"
    with open(env_file, "w") as f:
        f.write(env_content)
    
    print(f"✅ Generated {env_file}")


if __name__ == "__main__":
    generate_environment_properties()