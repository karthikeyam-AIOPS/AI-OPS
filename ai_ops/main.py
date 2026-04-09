#!/usr/bin/env python3
"""
AI-OPS CLI Entry Point
=====================

Command-line interface for the AI-OPS toolkit.
"""

import sys
from pathlib import Path

try:
    import typer
    from rich.console import Console
    from rich.table import Table
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False

# Initialize the Typer app
app = typer.Typer(
    name="aiops",
    help="AI-OPS: AI-Native Operations Toolkit",
    add_completion=False
)

console = None
if RICH_AVAILABLE:
    console = Console()


def print_info(message: str, style: str = "info"):
    """Print formatted messages."""
    if console and RICH_AVAILABLE:
        console.print(message, style=style)
    else:
        print(message)


@app.command()
def version():
    """Show AI-OPS version information."""
    try:
        from . import __version__, __description__
        print_info(f"AI-OPS Version: {__version__}")
        print_info(f"Description: {__description__}")
    except ImportError:
        print_info("AI-OPS Toolkit (version information unavailable)")


@app.command()
def status():
    """Check AI-OPS installation and dependencies."""
    print_info("🔍 AI-OPS Status Check", "bold blue")
    
    # Check core package
    try:
        import ai_ops
        print_info("✅ Core package: Available", "green")
    except ImportError:
        print_info("❌ Core package: Not available", "red")
    
    # Check Forecasting module
    try:
        from Forecasting import capacity_forecasting_demo
        print_info("✅ Forecasting module: Available", "green")
    except ImportError:
        print_info("⚠️  Forecasting module: Not available", "yellow")
    
    # Check examples
    examples_dir = Path("examples")
    if examples_dir.exists():
        print_info("✅ Examples directory: Available", "green")
    else:
        print_info("⚠️  Examples directory: Not found", "yellow")
    
    # Check optional dependencies
    optional_deps = {
        "numpy": "Data processing",
        "pandas": "Data analysis", 
        "sklearn": "Machine learning",
        "joblib": "Model persistence"
    }
    
    for dep, description in optional_deps.items():
        try:
            __import__(dep)
            print_info(f"✅ {dep}: Available ({description})", "green")
        except ImportError:
            print_info(f"⚠️  {dep}: Not available ({description})", "yellow")


@app.command()
def examples():
    """List available examples."""
    print_info("📚 AI-OPS Examples", "bold blue")
    
    examples_dir = Path("examples")
    if not examples_dir.exists():
        print_info("❌ Examples directory not found", "red")
        return
    
    example_files = list(examples_dir.glob("*_demo.py"))
    
    if example_files:
        print_info("\nAvailable examples:")
        for example in sorted(example_files):
            name = example.stem.replace('_demo', '').replace('_', ' ').title()
            print_info(f"  • {name}: python {example}")
    else:
        print_info("No example files found", "yellow")


@app.command()
def test():
    """Run basic tests."""
    print_info("🧪 Running AI-OPS Tests", "bold blue")
    
    tests_dir = Path("tests")
    if not tests_dir.exists():
        print_info("❌ Tests directory not found", "red") 
        return
    
    try:
        import subprocess
        result = subprocess.run([
            sys.executable, "-m", "pytest", "tests/", "-v"
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print_info("✅ All tests passed", "green")
        else:
            print_info("⚠️  Some tests failed", "yellow")
            if result.stdout:
                print(result.stdout)
                
    except Exception as e:
        print_info(f"❌ Error running tests: {e}", "red")


@app.command()
def forecast():
    """Run capacity forecasting demo."""
    print_info("📈 Running Capacity Forecasting Demo", "bold blue")
    
    try:
        import subprocess
        forecast_script = Path("Forecasting/capacity_forecasting_demo.py")
        
        if forecast_script.exists():
            result = subprocess.run([sys.executable, str(forecast_script)])
            if result.returncode == 0:
                print_info("✅ Forecasting demo completed", "green")
            else:
                print_info("⚠️  Forecasting demo completed with issues", "yellow")
        else:
            print_info("❌ Forecasting demo not found", "red")
            
    except Exception as e:
        print_info(f"❌ Error running forecast: {e}", "red")


def main():
    """Entry point for the CLI."""
    app()


if __name__ == "__main__":
    main()