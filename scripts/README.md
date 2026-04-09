# AI-OPS Scripts

Utility scripts for managing AI-OPS development, testing, and reporting.

## 📜 Available Scripts

### [generate_reports.py](generate_reports.py)

**Purpose**: Generate comprehensive quality and test reports including SonarQube analysis and Allure test reports.

**Features**:
- 🧪 **Test Execution**: Run pytest with coverage and Allure reporting
- 📊 **Report Generation**: Create HTML reports for tests and coverage
- 🔍 **SonarQube Integration**: Run code quality analysis
- 🌐 **Local Server**: Serve reports via HTTP server
- 🧹 **Cleanup**: Remove old reports before generation

**Usage**:
```bash
# Generate all reports
python scripts/generate_reports.py

# Specific report types
python scripts/generate_reports.py --allure     # Only Allure reports
python scripts/generate_reports.py --sonar      # Only SonarQube scan
python scripts/generate_reports.py --clean      # Clean old reports

# Serve reports locally
python scripts/generate_reports.py --serve --port 8080
```

**Output Directories**:
- `allure-results/` - Raw Allure test data
- `allure-report/` - Generated HTML Allure report
- `htmlcov/` - Coverage HTML report
- `coverage.xml` - Coverage data for SonarQube

## 🔧 Prerequisites

### Required Tools

1. **Allure CLI** (for HTML report generation):
   ```bash
   # macOS
   brew install allure
   
   # Linux/Windows
   # Download from: https://github.com/allure-framework/allure2/releases
   ```

2. **SonarQube Scanner** (for code analysis):
   ```bash
   # Download from: https://docs.sonarqube.org/latest/analysis/scan/sonarscanner/
   ```

3. **Python Dependencies**:
   ```bash
   pip install -e ".[dev]"
   ```

### Environment Setup

**For SonarQube** (optional):
```bash
export SONAR_HOST_URL="https://your-sonarqube-server.com"
export SONAR_TOKEN="your-sonarqube-token"
```

## 📊 Report Types

### Allure Test Reports
- **Interactive HTML reports** with test results, trends, and history
- **Test categorization** by features, stories, and severity
- **Step-by-step execution** details
- **Attachments** (screenshots, logs, data)
- **Test execution trends** over time

### SonarQube Analysis
- **Code quality metrics** (bugs, vulnerabilities, code smells)
- **Coverage analysis** integration
- **Technical debt** assessment
- **Security hotspots** identification
- **Maintainability ratings**

### Coverage Reports
- **Line-by-line coverage** visualization
- **Branch coverage** analysis
- **Missing coverage** highlighting
- **Coverage trends** tracking

## 🚀 CI/CD Integration

These scripts are designed to work with the GitHub Actions workflows:
- **[test-and-reports.yml](../.github/workflows/test-and-reports.yml)** - Automated testing and report generation
- **[code-quality.yml](../.github/workflows/code-quality.yml)** - Code quality checks

## 🛠 Development

To add new scripts:
1. Create the script in this directory
2. Make it executable: `chmod +x script_name.py`
3. Add documentation here
4. Consider adding to CI/CD workflows if appropriate

## 📚 Resources

- [Allure Documentation](https://docs.qameta.io/allure/)
- [SonarQube Documentation](https://docs.sonarqube.org/)
- [pytest Documentation](https://docs.pytest.org/)
- [Coverage.py Documentation](https://coverage.readthedocs.io/)