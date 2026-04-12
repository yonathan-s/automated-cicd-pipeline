# Automated CI/CD Pipeline for Containerised Web Applications

This project implements and evaluates an automated CI/CD deployment pipeline for containerised web applications on AWS. It also includes a custom deployment metrics platform used to analyse deployment performance and compare automated deployment against a manual deployment baseline.

## Project Outputs

This project contains three main outputs:

1. **Demo web application**  
   A Flask task manager application used as the demo deployment webapp to prove the pipeline

2. **Automated CI/CD deployment pipeline**  
   A GitHub Actions + Docker + Terraform + AWS deployment workflow.

3. **Deployment metrics platform**  
   A Flask + React platform for collecting, visualising, and statistically analysing deployment metrics.

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
src/platform/start-platform.ps1 # Backend startup helper
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

### src/platform/backend

This is the backend API for the deployment metrics platform.


### src/platform/frontend

This is the React dashboard for visualising deployment data and statistical analysis.


## Local Run Summary

Detailed instructions are in SUBMISSION_GUIDE.md.


### Demo web app
```bash 
cd src/webapp
python -m venv venv
source venv/Scripts/activate  
pip install -r requirements.txt
python app.py
```

### Platform backend
```bash 
cd src/platform/backend
python -m venv venv
pip install -r requirements.txt
python app.py
```

### Platform frontend
```bash 
cd src/platform/frontend
npm install
npm start
```
### Terraform Notes
Terraform commands are run from 
```bash 
cd infrastructure/terraform 
```

Typical commands:

```bash
terraform init
terraform validate
terraform plan
```

## Important Submission Notes
The metrics platform frontend expects a backend API URL.

Some cloud deployment features require AWS credentials and GitHub secrets, which are not included in the code submission.

The code submission is intended to document and reproduce the implemented system as far as possible without exposing secrets.

## Final Submission

For marker guidance, use:

SUBMISSION_GUIDE.md