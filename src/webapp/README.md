# Task Manager Demo Web Application

This is the demonstration web application used as the deployment target for the automated CI/CD pipeline. It is a Flask-based task manager API with a simple browser interface.

## Purpose in the Project

This component was not the main research contribution of the project. Its role was to act as a controlled deployment target so that the CI/CD pipeline, AWS infrastructure, and deployment metrics platform could be tested and evaluated consistently.

## Features

- Flask REST API
- Browser-based task interface
- Health check endpoint for deployment verification
- In-memory task storage
- CRUD operations for tasks
- Simple task statistics endpoint

## Main Endpoints

### Browser interface
- `GET /`

### Health check
- `GET /health`

### Task API
- `GET /api/tasks`
- `GET /api/tasks/<task_id>`
- `POST /api/tasks`
- `PUT /api/tasks/<task_id>`
- `DELETE /api/tasks/<task_id>`

### Statistics
- `GET /api/stats`

## Local Run Instructions

### 1. Open a terminal in this folder
```bash
cd src/webapp

```
### 2. Create a virtual environment
```bash
python -m venv venv

```

### 3. Activate it
```bash
# Windows PowerShell
.\venv\Scripts\Activate.ps1
# macOS/Linux
source venv/bin/activate
```

### 4. Install dependencies
```bash
pip install -r requirements.txt
```

### 5. Run the app
```bash
python app.py
```

### 6. Open in browser
Web interface: http://localhost:5000
Health check: http://localhost:5000/health

Run Tests

```bash

#From inside src/webapp:
pytest tests/test_app.py -v

#Run with Docker
#From inside src/webapp:
docker build -t task-manager-demo .
docker run -p 5000:5000 task-manager-demo
```

Then open:
http://localhost:5000

### Limitations
Uses in-memory storage only
Data resets when the app restarts
No authentication
Not intended as a production business application
Used only as a deployment target for the project evaluation
Project Role

### This component supported the following project outputs

Automated deployment through GitHub Actions
Container deployment to AWS ECS/Fargate
Collection of deployment metrics for comparative evaluation