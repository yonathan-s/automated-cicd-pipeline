# Submission Guide

This file explains how to run the main parts of the submitted codebase.

## 1. Main Project Components

### A. Demo Web Application
Folder:
```text
src/webapp
```

Purpose:

deployable target application for the CI/CD pipeline

### B. Deployment Metrics Platform Backend

Folder:

src/platform/backend

Purpose:

receives and stores deployment records
performs statistics and comparison analysis

### C. Deployment Metrics Platform Frontend

Folder:

src/platform/frontend

Purpose:

displays dashboard, deployment history, and analysis charts

### D. Infrastructure as Code

Folder:

infrastructure/terraform

Purpose:

provisions AWS infrastructure

## 2. Run the Demo Web Application (If and once deployed)

Open a terminal in src/webapp:

```bash
cd src/webapp
python -m venv venv

# Activate the virtual environment.

# Windows PowerShell
.\venv\Scripts\Activate.ps1

# macOS/Linux
source venv/bin/activate

# Install dependencies:

pip install -r requirements.txt

# Run the application:

python app.py

# Open: http://localhost:5000 and http://localhost:5000/health

# Run tests:

pytest tests/test_app.py -v
```

## 3. Run the Platform Backend

Open a terminal in src/platform/backend:

```bash
cd src/platform/backend
python -m venv venv

# Activate the virtual environment and install dependencies:

pip install -r requirements.txt

# Run backend:

python app.py

# Backend runs on: http://localhost:5001

# Health endpoint: http://localhost:5001/api/health
```

## 4. Run the Platform Frontend

Open a terminal in src/platform/frontend:

```bash
cd src/platform/frontend
npm install

# Create .env from the example if required:

copy .env.example .env

# Start the frontend:

npm start

# Frontend runs on: http://localhost:3000

```

## 5. Terraform

Terraform files are located in:

cd infrastructure/terraform

Typical commands:

terraform init
terraform validate
terraform plan

### Note:

Cloud deployment requires valid AWS credentials
Secrets are not included in the code submission

## 6. GitHub Actions Note

The workflow file is:

.github/workflows/deploy.yml

It expects GitHub secrets for AWS credentials and for the metrics platform URL.

Because secrets are not included in the submission, the workflow is documented but not fully executable by default.

## 7. Important Limitation Notes
The demo application uses in-memory task storage only.
The metrics platform frontend requires the backend to be running.
The cloud deployment workflow requires AWS credentials and GitHub secrets.
The platform contains both real deployment data handling and manually simulated comparison data.