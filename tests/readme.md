# tests

See the project [README.md](../README.md) for full documentation.

### Test Categories
- **Unit Tests** (`@pytest.mark.unit`): Test individual components and functions
- **Integration Tests** (`@pytest.mark.integration`): Test module interactions
- **Smoke Tests** (`@pytest.mark.smoke`): Critical functionality verification
- **Performance Tests** (`@pytest.mark.performance`): Performance benchmarks

### Test Files
- **[test_basic.py](test_basic.py)** - Basic functionality and package structure tests
- Add more test files as modules are developed

## 🚀 Running Tests

### Quick Test Run
```bash
# Smart test runner (adapts to available plugins)
python scripts/run_tests.py

# Manual pytest commands
pytest                           # Basic test run
pytest --cov=ai_ops             # With coverage
pytest -m unit                  # Run specific test marks
pytest -m "smoke or integration" # Multiple marks
```

### With Allure Reports (if plugin available)
```bash
# Run tests and generate Allure results
pytest --alluredir=allure-results

# Generate and view HTML report (requires Allure CLI)
allure generate allure-results --clean --output allure-report
allure serve allure-results  # Opens browser automatically
```

### Using the Report Generator Script
```bash
# Generate all reports (tests + quality) - handles missing dependencies
python scripts/generate_reports.py --allure

# Serve reports locally
python scripts/generate_reports.py --serve
```

## 📊 Allure Features Used

- **@allure.feature()** - High-level feature grouping
- **@allure.story()** - User story within features  
- **@allure.step()** - Detailed test steps
- **allure.attach()** - Attach screenshots, logs, data
- **Parametrized tests** - Data-driven testing
- **Test markers** - Category and filter tests

## 📈 Coverage Reports

- **XML Report**: `coverage.xml` (for SonarQube/CI)
- **HTML Report**: `htmlcov/index.html` (for developers)

## 🎯 Best Practices

1. **Use descriptive test names** - Explain what is being tested
2. **Add Allure decorators** - Organize tests for better reporting
3. **Use allure.step()** - Break complex tests into steps
4. **Attach relevant data** - Screenshots, logs, input/output data
5. **Use appropriate markers** - Help with test categorization
6. **Write docstrings** - Document test purpose and approach