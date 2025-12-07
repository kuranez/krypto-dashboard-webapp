# Testing

This directory contains pytest tests for the krypto-dashboard-web project.

## Setup

1. Install test dependencies:
```bash
pip install -r requirements.txt
```

Or install from the project's virtual environment:
```bash
cd testing
../web/.venv/bin/python -m pip install -r requirements.txt
```

## Running Tests

Run all tests:
```bash
pytest
```

Run with verbose output and print statements:
```bash
pytest -v -s
```

Run a specific test file:
```bash
pytest test_correlation.py -v -s
```

Run a specific test:
```bash
pytest test_correlation.py::TestCorrelationBeta::test_rolling_correlation -v -s
```

Run with coverage:
```bash
pytest --cov=../web/app --cov-report=html
```

## Test Files

- `test_correlation.py` - Tests for correlation and beta calculations
- `conftest.py` - Pytest configuration and fixtures

## Writing New Tests

When adding new tests:
1. Create a new file starting with `test_`
2. Import necessary modules from the app directory (path is configured in `conftest.py`)
3. Use pytest fixtures for setup/teardown
4. Follow the naming convention: `test_<feature_name>`
