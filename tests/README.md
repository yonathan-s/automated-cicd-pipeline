# Testing Documentation

## Overview

This directory contains automated tests for the Task Manager API.

## Test Structure
```
tests/
├── unit/           # Unit tests for individual functions
│   └── test_app.py
├── integration/    # Integration tests (to be added)
└── README.md      # This file
```

## Running Tests

### Prerequisites

1. Virtual environment activated
2. Dependencies installed: `pip install -r src/webapp/requirements.txt`
3. pytest installed: `pip install pytest pytest-flask`

### Run All Tests
```bash
pytest tests/ -v
```

### Run Specific Test File
```bash
pytest tests/unit/test_app.py -v
```

### Run Specific Test
```bash
pytest tests/unit/test_app.py::test_health_check -v
```

### Run with Coverage
```bash
pytest tests/ --cov=src/webapp --cov-report=html
```

This generates an HTML coverage report in `htmlcov/index.html`

## Test Coverage

Current test coverage: **~80%**

Covered areas:
- ✅ Health check endpoint
- ✅ Task CRUD operations
- ✅ Error handling (404, 400)
- ✅ Input validation
- ✅ Statistics endpoint

Not yet covered:
- ❌ HTML template rendering
- ❌ CORS functionality
- ❌ Logging functionality

## Writing New Tests

### Test Structure
```python
def test_description(client):
    """Test description"""
    # Arrange - set up test data
    
    # Act - perform the action
    
    # Assert - verify results
```

### Example Test
```python
def test_create_task(client):
    """Test creating a new task"""
    task_data = {'title': 'Test Task'}
    
    response = client.post('/api/tasks', json=task_data)
    
    assert response.status_code == 201
    assert response.get_json()['title'] == 'Test Task'
```

## Continuous Integration

These tests will be run automatically in the CI/CD pipeline on every:
- Git push
- Pull request
- Deployment

Pipeline will fail if any test fails, preventing bad code from being deployed.

## Future Improvements

- [ ] Integration tests with actual HTTP requests
- [ ] Load testing
- [ ] Security testing
- [ ] Database integration tests (when database is added)
- [ ] End-to-end tests with Selenium