

## Executive Summary

This document summarizes the complete manual deployment of the Task Manager application to AWS. This serves as the baseline for comparing against automated CI/CD deployment.

---

## Deployment Steps Overview

| Step | Component | Duration | Difficulty (1-5) | Errors |
|------|-----------|----------|------------------|--------|
| 1 | ECR Repository | 15 min | 2 | 0 |
| 2 | Docker Image Push | 35 min | 3 | 1 |
| 3 | VPC Creation | 30 min | 2 | 0 |
| 4 | Subnet Creation | 40 min | 4 | 2 |
| 5 | Internet Gateway | 15 min | 2 | 0 |
| 6 | NAT Gateway | 20 min | 3 | 0 |
| 7 | Route Tables | 30 min | 4 | 1 |
| 8 | ALB Security Group | 25 min | 3 | 1 |
| 9 | ECS Security Group | 30 min | 4 | 1 |
| 10 | IAM Task Execution Role | 30 min | 4 | 1 |
| 11 | IAM Task Role | 20 min | 3 | 0 |
| 12 | ECS Cluster | 20 min | 2 | 0 |
| 13 | CloudWatch Log Group | 15 min | 2 | 0 |
| 14 | ECS Task Definition | 45 min | 5 | 3 |
| 15 | Target Group | 30 min | 3 | 1 |
| 16 | Application Load Balancer | 45 min | 4 | 2 |
| 17 | ECS Service | 45 min | 5 | 2 |
| 18 | Deployment Verification | 30 min | 3 | 0 |
| 19 | CloudWatch Dashboard | 45 min | 3 | 0 |
| 20 | CloudWatch Alarms | 30 min | 3 | 0 |

**Total Steps:** 20
**Total Time:** ~12 hours
**Total Errors:** 15
**Average Difficulty:** 3.2/5

---

## Resources Created

### Networking (6 resources)
- 1 VPC
- 4 Subnets (2 public, 2 private)
- 1 Internet Gateway
- 1 NAT Gateway
- 1 Elastic IP
- 2 Route Tables

### Security (4 resources)
- 2 Security Groups
- 2 IAM Roles

### Compute (5 resources)
- 1 ECR Repository
- 1 ECS Cluster
- 1 Task Definition
- 1 ECS Service
- 2 ECS Tasks (running)

### Load Balancing (2 resources)
- 1 Application Load Balancer
- 1 Target Group

### Monitoring (4 resources)
- 1 CloudWatch Log Group
- 1 CloudWatch Dashboard
- 2 CloudWatch Alarms

**Total Resources:** 24

---

## Key Metrics (Baseline)

### Deployment Time
- **Initial setup:** 12 hours
- **Time to first running application:** 12 hours
- **Average time per resource:** 36 minutes

### Reliability
- **Deployment attempts:** 1
- **Failed attempts:** 0 (after corrections)
- **Errors during deployment:** 15
- **Time spent fixing errors:** ~2 hours (included in total)

### Complexity
- **AWS Console screens visited:** ~30
- **Form fields filled manually:** ~150+
- **Copy-paste operations:** ~20 (ARNs, IDs, URIs)
- **Screenshot documentation:** ~60 images

### Skills Required
- Understanding of VPC networking
- Knowledge of security groups
- IAM roles and policies
- ECS concepts (tasks, services, clusters)
- Load balancer configuration
- CloudWatch monitoring
- Docker image management

---

## Common Errors and Issues

### Error 1: Wrong VPC Selected
- **Step:** Security Group creation
- **Impact:** Had to delete and recreate
- **Time lost:** 10 minutes
- **Lesson:** Always verify VPC selection

### Error 2: Wrong Subnet Type for ALB
- **Step:** ALB creation
- **Impact:** ALB cannot be internet-facing in private subnets
- **Time lost:** 15 minutes
- **Lesson:** Public subnets for ALB, private for ECS tasks

### Error 3: Target Group Type
- **Step:** Target Group creation
- **Impact:** Instances type doesn't work with Fargate
- **Time lost:** 10 minutes
- **Lesson:** Fargate requires IP address type

### Error 4: Security Group Source
- **Step:** ECS Security Group
- **Impact:** Initially allowed 0.0.0.0/0 instead of ALB SG
- **Time lost:** 5 minutes
- **Lesson:** Tasks should only accept traffic from ALB

### Error 5: Task Definition Image URI
- **Step:** Task Definition
- **Impact:** Typo in ECR image URI caused task failure
- **Time lost:** 20 minutes (including troubleshooting)
- **Lesson:** Copy-paste URIs, don't type manually

[List all 15 errors with similar detail]

---

## Deployment Dependencies
```
ECR Repository
    ↓
Docker Image
    ↓
VPC → Subnets → IGW/NAT → Route Tables
    ↓
Security Groups
    ↓
IAM Roles
    ↓
CloudWatch Log Group
    ↓
Task Definition
    ↓
Target Group
    ↓
Load Balancer
    ↓
ECS Cluster → ECS Service
    ↓
Running Application
    ↓
Monitoring Dashboard
```

**Key Observation:** Strict dependency order. Cannot skip or reorder steps.

---

## Manual Deployment Challenges

### 1. Configuration Complexity
- Many interdependent resources
- Must remember IDs, ARNs, names from previous steps
- Easy to select wrong resource from dropdowns
- Long forms with many fields

### 2. Error-Prone Process
- Copy-paste errors (typos in IDs/URIs)
- Wrong selections (VPC, subnets, types)
- Missing required fields
- Unclear error messages

### 3. Time-Consuming
- Each resource requires multiple console screens
- Wait times for resource provisioning
- Troubleshooting errors takes significant time

### 4. Documentation Burden
- Manual screenshot collection
- Timing each step
- Recording all configuration details
- Tracking errors and resolutions

### 5. Repeatability Issues
- Difficult to reproduce exactly
- Human errors in repeated deployments
- Configuration drift over time
- No version control of infrastructure

---

## Comparison Preview

This manual deployment will be compared against automated CI/CD deployment in Week 9.

**Expected automated improvements:**
- Deployment time: <10 minutes (vs 12 hours manual)
- Error rate: 0% (vs 15 errors manual)
- Repeatability: 100% identical (vs variable manual)
- Documentation: Automatic (vs manual screenshots)
- Skills required: Git push only (vs deep AWS knowledge)

---

## Application Status

**Deployment Status:** SUCCESS
**Application URL:** http://task-manager-alb-442717427.eu-west-2.elb.amazonaws.com/
**Running Tasks:** 1/1 (For now might change to 2)
**Target Health:** 1/1 healthy
**CloudWatch Logs:** Active
**Monitoring Dashboard:** Active
**Alarms:** Configured

**Application is fully operational and ready for evaluation testing.**

---

## Cost Summary

**Monthly Running Costs (if left running):**
- NAT Gateway: ~$32.40/month
- ALB: ~$16.20/month (+ data processing)
- Fargate: 2 tasks × 0.5 vCPU × 1GB = ~$14/month
- Data transfer: ~$5/month
- **Total: ~$67/month**

**Recommendation:** Destroy resources after evaluation to avoid costs.

---

## Screenshots Index

All screenshots organized in: `docs/screenshots/week-4-manual-deployment/`

**Total screenshots:** ~60
**Organized by day:**
- Day 1: ECR (5 images)
- Day 2: Networking (12 images)
- Day 3: Security (8 images)
- Day 4: ECS Setup (7 images)
- Day 5: Load Balancer (8 images)
- Day 6: Service Deployment (7 images)
- Day 7: Monitoring (8 images)
- Testing: Application (5 images)

---

## Lessons Learned

### What Worked Well
- Systematic step-by-step approach
- Screenshot documentation captured all decisions
- Error tracking helped identify patterns
- Resource naming convention kept things organized

### What Was Challenging
- Remembering IDs and ARNs from previous steps
- Understanding security group relationships
- Subnet selection (public vs private)
- Long wait times for resources to provision
- Troubleshooting task failures required multiple services

### Key Takeaways
1. Manual deployment requires deep AWS knowledge
2. Easy to make configuration mistakes
3. Error messages often unclear
4. Time-consuming even for experienced users
5. Difficult to reproduce exactly
6. Documentation overhead is significant
7. Infrastructure as Code would eliminate most issues