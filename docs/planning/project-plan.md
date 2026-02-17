# Project Plan: Automated CI/CD Pipeline

## Project Information
- **Title:** Automated CI/CD Deployment Pipeline for Containerised Web Applications using AWS
- **Student:** Yonathan
- **Start Date:** 5 February 2025
- **Target Completion:** 22 March 2025
- **Hard Deadline:** 29 March 2025

## Project Objectives

### Primary Objective
Develop an automated CI/CD pipeline that deploys a containerised web application to AWS using infrastructure as code, with built-in testing, security scanning, and performance monitoring.

### Sub-objectives
- Use Docker to package the sample web application
- Create AWS cloud infrastructure using Terraform
- Set up GitHub Actions for automated build, test, and deployment
- Implement security scanning (container vulnerability scanning)
- Configure monitoring with AWS CloudWatch
- Compare manual vs automated deployment approaches

## Novelty and Evaluation Focus
This project provides a **comparative evaluation** between:
- **Manual deployment** (baseline)
- **Automated CI/CD deployment**

### Metrics to Measure
1. Deployment time
2. Deployment failure rate
3. Recovery time after failure
4. Security checks coverage
5. Monitoring visibility
6. Repeatability consistency

## Technology Stack

### Application Layer
- **Language:** Python 3.11
- **Framework:** Flask
- **Purpose:** Simple REST API for deployment testing

### Containerization
- **Tool:** Docker
- **Registry:** AWS ECR

### Cloud Infrastructure
- **Provider:** AWS
- **Services:** ECS Fargate, VPC, IAM, CloudWatch

### Infrastructure as Code
- **Tool:** Terraform

### CI/CD
- **Tool:** GitHub Actions

### Security
- **Scanning:** Trivy, GitHub Dependabot

### Monitoring
- **Tool:** AWS CloudWatch

## 12-Week Timeline

### Week 1: Foundation (13-19 Feb)
- Environment setup
- Background research
- Repository initialization

### Week 2: Application Development (20-26 Feb)
- Build Flask web application
- Local testing

### Week 3: Containerisation (27 Feb-5 Mar)
- Dockerize application
- Test containers locally

### Week 4: AWS Manual Deployment (6-12 Mar)
- Set up AWS infrastructure manually
- Document baseline deployment
- **CRITICAL:** Collect manual deployment metrics

### Week 5: Infrastructure as Code (13-19 Mar)
- Convert manual setup to Terraform
- Test infrastructure provisioning

### Week 6: CI/CD Pipeline (20-26 Mar)
- Implement GitHub Actions workflows
- Automate build and deploy

### Week 7: Testing & Security (27 Mar-2 Apr)
- Add automated tests
- Implement security scanning

### Week 8: Monitoring (3-9 Apr)
- Configure CloudWatch dashboards
- Set up alerts

### Week 9: Evaluation (10-16 Apr)
- Conduct deployment experiments
- Collect comparative data

### Week 10: Analysis (17-23 Apr)
- Analyze results
- Begin dissertation writing

### Week 11: Documentation (24-30 Apr)
- Complete technical documentation
- Draft dissertation chapters

### Week 12: Final Polish (1-7 May)
- Finalize dissertation
- Create demonstration video
- Prepare submission

## Expected Deliverables
1. Working CI/CD pipeline
2. Infrastructure as Code configurations
3. Containerised Flask application
4. Deployment monitoring dashboards
5. Comparative evaluation dataset
6. Dissertation report
7. Demonstration video

## Risks and Mitigation
- **AWS costs:** Set billing alerts, use free tier
- **Time overruns:** Weekly milestones, buffer week
- **Technical complexity:** Incremental development, ask for help early