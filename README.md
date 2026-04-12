# Automated CI/CD Pipeline for Containerised Web Applications

This project implements and evaluates an automated CI/CD deployment pipeline for containerised web applications on AWS. It also includes a custom deployment metrics platform used to analyse deployment performance and compare automated deployment against a manual deployment baseline.

This is a readme file with a submission guide for markers located halfway down this file

## Project Outputs

This project contains three main outputs:

1. **Demo web application**  
   A Flask task manager application used as the demo deployment webapp to prove the pipeline

2. **Automated CI/CD deployment pipeline**  
   A GitHub Actions + Docker + Terraform + AWS deployment workflow.

3. **Deployment metrics platform**  
   A Flask + React platform for collecting, visualising, and statistically analysing deployment metrics of my Automated CI/CD deployment pipeline

## Technology Stack

### Languages
- Python
- JavaScript
- HTML
- CSS
- YAML
- Terraform HCL

### Application and Platform
- Flask
- Flask-CORS
- Flask-SQLAlchemy
- React
- Axios
- Chart.js
- NumPy
- SciPy

### DevOps / Infrastructure
- Docker
- GitHub Actions
- Terraform
- AWS ECS
- AWS Fargate
- AWS ECR
- AWS Application Load Balancer
- AWS VPC
- AWS IAM
- AWS CloudWatch

## Project Structure

```text
.
.github/workflows/              # GitHub Actions workflows
docs/                           # Supporting documentation and screenshots of manual deployment and build stage
infrastructure/terraform/       # Terraform IaC
src/webapp/                     # Demo deployable web application
src/platform/backend/           # Metrics platform backend API
src/platform/frontend/          # Metrics platform frontend UI
src/platform/start-platform.ps1 # Windows PowerShell script that starts the platform backend. Alternative way to running manually
SUBMISSION_GUIDE.md             # Markers run guide

```

## What Each Component Does

### src/webapp
This is the deployable demo application. It is the application built into a Docker image and deployed to AWS.

### infrastructure/terraform
This defines the AWS infrastructure used for deployment:

- VPC
- Subnets
- Internet gateway
- NAT gateway
- Security groups
- Load balancer
- ECS cluster/service
- ECR repository

### .github/workflows
This contains the CI/CD workflow that:

- Builds the Docker image
- Scans it
- Runs tests
- Pushes the image to ECR
- Redeploys the ECS service
- Sends deployment metrics to the metrics platform (This has not been implemented yet. For now all automated deployment metrics are manually inputted to the platform)

### src/platform

The metrics platform is a separate full-stack application built to measure and evaluate the CI/CD pipeline. It has two parts: a Flask backend API and a React frontend dashboard.

**What it does:**

The platform collects deployment records and uses them to statistically compare automated deployments against a manual deployment baseline. It produces:

- A dashboard showing deployment history, success rates, and timing
- Descriptive statistics (mean duration, standard deviation, error counts) for both deployment types
-Includes an independent samples t-test on deployment duration, a chi-square test on success rates, and Cohen's d effect size
- A simulator that generates realistic manual deployment data based on a real manual deployment I conducted, used to produce a large enough dataset for statistical analysis

**How it works:**

The backend (Flask + SQLAlchemy + SQLite) exposes a REST API for storing deployment records, running statistical calculations using NumPy and SciPy, and serving simulation results. The frontend (React + Chart.js) fetches data from the backend and displays it across three views: Dashboard, Statistical Analysis, and Simulator.

**Limitations:**

- The platform uses a local SQLite database, so data does not persist between fresh installs
- The manual deployment data is simulated based on a single real deployment, not repeated real measurements
- The GitHub Actions workflow does not automatically send metrics to the platform — automated deployment records were manually entered
- The platform is not deployed and requires both the backend and frontend to be running locally to function

### src/platform/backend

This is the backend API for the deployment metrics platform.


### src/platform/frontend

This is the React dashboard for visualising deployment data and statistical analysis.


## Important Submission Notes
The metrics platform frontend expects a backend API URL.

Some cloud deployment features require AWS credentials and GitHub secrets, which are not included in the code submission.

The code submission is intended to document and reproduce the implemented system as far as possible without exposing secrets.





--------------------------------------------------------------------------------------------------------------------------------





# Submission Guide for markers

This part explains how to run the main parts of the submitted codebase.

## 1. Main Project Components

### A. Demo Web Application

Folder:
src/webapp


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

## 2. Run the Demo Web Application 

Python 3.10 or above recommended. If python doesn't work, try python3

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

Python 3.10 or above recommended. If python doesn't work, try python3

Open a terminal in src/platform/backend:

```bash
cd src/platform/backend
python -m venv venv

# Activate the virtual environment and install dependencies:
./venv/Scripts/activate  

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
```bash
terraform init      # downloads required providers and sets up the working directory
terraform validate  # checks the configuration files for syntax errors
terraform plan      # previews what changes will be made before applying
terraform apply     # provisions the infrastructure on AWS (requires valid AWS credentials)
terraform destroy   # tears down all provisioned infrastructure
```
### Note:

Cloud deployment requires valid AWS credentials
Secrets are not included in the code submission

## 6. GitHub Actions Note

The workflow file is:

.github/workflows/deploy.yml

It expects GitHub secrets for AWS credentials and for the metrics platform URL.

Because secrets are not included in the submission, the workflow is documented but not fully executable by default.

Although the workflow contains prototype support for metrics submission, the automated deployment records used in the final platform evaluation were manually entered based on GitHub Actions run results.

## 7. Important Limitation Notes
The demo application uses in-memory task storage only.
The metrics platform frontend requires the backend to be running.
The cloud deployment workflow requires AWS credentials and GitHub secrets.
The platform contains both real deployment data handling and manually simulated comparison data.
The workflow uses manually inputted and seeded data rather than sending the metrics straight to the platform

## Author

Yonathan Surafel — BSc Computer Science, City St George's, University of London