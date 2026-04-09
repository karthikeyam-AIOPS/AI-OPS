"""
Basic smoke tests for AI-OPS package.
These tests work with or without Allure reporting.
"""

import pytest
import sys
from pathlib import Path

# Add the project root to Python path for imports
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Try to import Allure, but continue without it if not available
try:
    import allure
    ALLURE_AVAILABLE = True
    
    def allure_feature(name):
        return allure.feature(name)
    
    def allure_story(name):
        return allure.story(name)
        
    def allure_step(name):
        return allure.step(name)
        
except ImportError:
    ALLURE_AVAILABLE = False
    
    # Create no-op decorators if Allure is not available
    def allure_feature(name):
        def decorator(func):
            return func
        return decorator
    
    def allure_story(name):
        def decorator(func):
            return func
        return decorator
    
    class allure_step:
        def __init__(self, name):
            self.name = name
        
        def __enter__(self):
            print(f"Step: {self.name}")
            return self
        
        def __exit__(self, *args):
            pass


@allure_feature("Package Structure")
@allure_story("Import Tests")
@pytest.mark.unit
def test_package_imports():
    """Test that core packages can be imported successfully."""
    with allure_step("Import ai_ops package"):
        try:
            import ai_ops
            assert hasattr(ai_ops, '__file__'), "ai_ops package should be importable"
        except ImportError as e:
            pytest.fail(f"Failed to import ai_ops: {e}")
    
    with allure_step("Check package exists"):
        assert ai_ops is not None


@allure_feature("Forecasting Module")
@allure_story("Module Structure")
@pytest.mark.unit  
def test_forecasting_module_exists():
    """Test that the Forecasting module structure is correct."""
    with allure_step("Check Forecasting directory exists"):
        forecasting_dir = project_root / "Forecasting"
        assert forecasting_dir.exists(), "Forecasting directory should exist"
        
    with allure_step("Check __init__.py exists"):
        init_file = forecasting_dir / "__init__.py"
        assert init_file.exists(), "Forecasting/__init__.py should exist"
        
    with allure_step("Check capacity forecasting demo exists"):
        demo_file = forecasting_dir / "capacity_forecasting_demo.py"
        assert demo_file.exists(), "capacity_forecasting_demo.py should exist"


@allure_feature("Examples Module")
@allure_story("Demo Scripts")
@pytest.mark.integration
def test_examples_structure():
    """Test that example scripts are properly structured."""
    examples_dir = project_root / "examples"
    
    with allure_step("Verify examples directory"):
        assert examples_dir.exists(), "Examples directory should exist"
    
    with allure_step("Check for demo files"):
        expected_demos = [
            "anomaly_detection_demo.py",
            "sentiment_analysis_demo.py", 
            "student_prediction_demo.py",
            "run_all_examples.py"
        ]
        
        for demo in expected_demos:
            demo_path = examples_dir / demo
            assert demo_path.exists(), f"{demo} should exist in examples/"


@allure_feature("Configuration")
@allure_story("Project Setup")
@pytest.mark.unit
def test_project_configuration():
    """Test project configuration files exist and are valid."""
    
    with allure_step("Check pyproject.toml exists"):
        pyproject = project_root / "pyproject.toml"
        assert pyproject.exists(), "pyproject.toml should exist"
    
    with allure_step("Check README exists"):
        readme = project_root / "README.md"
        assert readme.exists(), "README.md should exist"


@allure_feature("Dependencies")
@allure_story("Critical Libraries")
@pytest.mark.smoke
def test_critical_dependencies():
    """Test that critical dependencies are available.""" 
    # Only test dependencies that are absolutely required
    base_deps = ["sys", "os", "pathlib"]
    
    for dep in base_deps:
        with allure_step(f"Import {dep}"):
            try:
                __import__(dep)
            except ImportError:
                pytest.fail(f"Critical dependency {dep} not available")


def test_basic_functionality():
    """Test basic Python functionality to ensure the test environment works."""
    # Simple computation test
    assert 2 + 2 == 4, "Basic math should work"
    assert "hello".upper() == "HELLO", "String methods should work"
    assert [1, 2, 3][1] == 2, "List indexing should work"


if __name__ == "__main__":
    # Allow running this file directly for quick testing
    pytest.main([__file__, "-v"])