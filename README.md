# Automated CI/CD Deployment Pipeline

An automated CI/CD pipeline for deploying containerised Flask web applications to AWS using infrastructure as code.

## Project Overview

This project demonstrates a complete DevOps workflow including:
- Containerised Python/Flask web application
- Infrastructure as Code using Terraform
- Automated CI/CD pipeline with GitHub Actions
- Container security scanning
- AWS deployment (ECS Fargate)
- Monitoring and logging with CloudWatch
- Comparative evaluation: Manual vs Automated deployment

## Technology Stack

- **Application:** Python 3.11 + Flask
- **Containerization:** Docker
- **Container Registry:** AWS ECR
- **Cloud Provider:** AWS (ECS, VPC, IAM, CloudWatch)
- **IaC:** Terraform
- **CI/CD:** GitHub Actions
- **Security:** Trivy, Dependabot
- **Monitoring:** AWS CloudWatch

## Project Structure
```
automated-cicd-pipeline/
├── .github/workflows/       # GitHub Actions CI/CD workflows
├── docs/                    # Project documentation
│   ├── architecture/        # Architecture diagrams
│   ├── evaluation/          # Evaluation metrics and data
│   └── planning/            # Project planning documents
├── infrastructure/          # Terraform configurations
│   └── terraform/
│       ├── modules/         # Reusable Terraform modules
│       └── environments/    # Environment-specific configs
├── src/webapp/              # Flask application source code
├── tests/                   # Automated tests
│   ├── unit/               # Unit tests
│   └── integration/        # Integration tests
└── scripts/                 # Utility scripts
```

## Getting Started

### Prerequisites

- Python 3.11+
- Docker Desktop
- AWS CLI configured
- Terraform
- Git

### Local Development
```bash
# Clone repository
git clone https://github.com/yonathan-s/automated-cicd-pipeline.git
cd automated-cicd-pipeline

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies (coming in Week 2)
pip install -r src/webapp/requirements.txt

# Run application locally (coming in Week 2)
python src/webapp/app.py
```

## Deployment

(Deployment instructions will be added as the project develops)

## Evaluation

This project includes a comparative evaluation measuring:
1. Deployment time
2. Failure rate
3. Recovery time
4. Security coverage
5. Monitoring visibility
6. Repeatability


## Development Progress

### ✅ Week 1: Foundation (Complete)
- Development environment configured
- AWS account set up
- GitHub repository initialized
- Research and planning completed

### ✅ Week 2: Flask Application (Complete)
- Task Manager API built
- 6 REST endpoints implemented
- Web interface created
- Unit tests written (11 tests, all passing)
- Local testing successful

### 🔜 Week 3: Containerization (Next)
- Docker configuration
- Container build and testing

## Quick Start

### Run the Application
```bash
# Navigate to webapp directory
cd src/webapp

# Create virtual environment
python -m venv venv

# Activate virtual environment (Windows PowerShell)
.\venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Run the application
python app.py
```

Access at: http://localhost:5000

### Run Tests
```bash
# From project root with venv activated
pytest tests/unit/test_app.py -v
```

## API Documentation

See [src/webapp/README.md](src/webapp/README.md) for detailed API documentation.



