"""
Basic test for AI-OPS package - DISABLED due to Allure dependency issues.
This test exercises Allure reporting features with various markers and assertions.
"""

# DISABLED - This test file requires Allure which is not installed
# Use test_simple.py instead for basic functionality testing

"""
import pytest
import allure
import sys
from pathlib import Path

# Add the project root to Python path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))


@allure.feature("Package Structure")
@allure.story("Import Tests")
@pytest.mark.unit
def test_package_imports():
    """Test that core packages can be imported successfully."""
    with allure.step("Import ai_ops package"):
        try:
            import ai_ops
            assert hasattr(ai_ops, '__file__'), "ai_ops package should be importable"
        except ImportError as e:
            pytest.fail(f"Failed to import ai_ops: {e}")
    
    with allure.step("Check package version"):
        # This would typically check __version__ if it exists
        assert ai_ops is not None


@allure.feature("Forecasting Module")
@allure.story("Module Structure")
@pytest.mark.unit  
def test_forecasting_module_exists():
    """Test that the Forecasting module structure is correct."""
    with allure.step("Check Forecasting directory exists"):
        forecasting_dir = Path(__file__).parent.parent / "Forecasting"
        assert forecasting_dir.exists(), "Forecasting directory should exist"
        
    with allure.step("Check __init__.py exists"):
        init_file = forecasting_dir / "__init__.py"
        assert init_file.exists(), "Forecasting/__init__.py should exist"
        
    with allure.step("Check capacity forecasting demo exists"):
        demo_file = forecasting_dir / "capacity_forecasting_demo.py"
        assert demo_file.exists(), "capacity_forecasting_demo.py should exist"


@allure.feature("Examples Module")
@allure.story("Demo Scripts")
@pytest.mark.integration
def test_examples_structure():
    """Test that example scripts are properly structured."""
    examples_dir = Path(__file__).parent.parent / "examples"
    
    with allure.step("Verify examples directory"):
        assert examples_dir.exists(), "Examples directory should exist"
    
    with allure.step("Check for demo files"):
        expected_demos = [
            "anomaly_detection_demo.py",
            "sentiment_analysis_demo.py", 
            "student_prediction_demo.py",
            "run_all_examples.py"
        ]
        
        for demo in expected_demos:
            demo_path = examples_dir / demo
            assert demo_path.exists(), f"{demo} should exist in examples/"


@allure.feature("Configuration")
@allure.story("Project Setup")
@pytest.mark.unit
def test_project_configuration():
    """Test project configuration files exist and are valid."""
    project_root = Path(__file__).parent.parent
    
    with allure.step("Check pyproject.toml exists"):
        pyproject = project_root / "pyproject.toml"
        assert pyproject.exists(), "pyproject.toml should exist"
    
    with allure.step("Check README exists"):
        readme = project_root / "README.md"
        assert readme.exists(), "README.md should exist"
    
    with allure.step("Check SonarQube config exists"):
        sonar_config = project_root / "sonar-project.properties"
        assert sonar_config.exists(), "sonar-project.properties should exist"


@allure.feature("Dependencies")
@allure.story("Critical Libraries")
@pytest.mark.smoke
def test_critical_dependencies():
    """Test that critical dependencies are available."""
    critical_deps = [
        "numpy", "pandas", "sklearn", "joblib"
    ]
    
    for dep in critical_deps:
        with allure.step(f"Import {dep}"):
            try:
                __import__(dep)
                allure.attach(f"{dep} imported successfully", name=f"{dep}_status", attachment_type=allure.attachment_type.TEXT)
            except ImportError:
                pytest.fail(f"Critical dependency {dep} not available")


@allure.feature("Performance")
@allure.story("Basic Operations")
@pytest.mark.performance
def test_basic_operations_performance():
    """Test basic operations performance for baseline."""
    import time
    
    with allure.step("Test simple computation"):
        start_time = time.time()
        
        # Simple computation
        result = sum(range(10000))
        
        execution_time = time.time() - start_time
        
        allure.attach(f"Execution time: {execution_time:.4f}s", 
                     name="performance_metric", 
                     attachment_type=allure.attachment_type.TEXT)
        
        # Should complete in reasonable time
        assert execution_time < 1.0, f"Basic computation took too long: {execution_time}s"
        assert result == 49995000, "Computation result should be correct"


# Parameterized test for demonstration
@allure.feature("Data Processing")
@allure.story("Data Validation")
@pytest.mark.parametrize("input_data,expected", [
    ([1, 2, 3], 6),
    ([0], 0),
    ([], 0),
    ([10, -5, 3], 8),
])
def test_data_processing(input_data, expected):
    """Test data processing with various inputs."""
    with allure.step(f"Process data: {input_data}"):
        result = sum(input_data)
        
        allure.attach(f"Input: {input_data}, Result: {result}", 
                     name="processing_result", 
                     attachment_type=allure.attachment_type.TEXT)
        
        assert result == expected, f"Expected {expected}, got {result}"


@allure.feature("Error Handling")  
@allure.story("Exception Cases")
@pytest.mark.unit
def test_error_handling():
    """Test error handling scenarios."""
    with allure.step("Test division by zero"):
        with pytest.raises(ZeroDivisionError):
            _ = 1 / 0
    
    with allure.step("Test type error"):
        with pytest.raises(TypeError):
            _ = "string" + 42