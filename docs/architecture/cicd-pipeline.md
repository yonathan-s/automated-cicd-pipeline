# CI/CD Pipeline Documentation

## Overview

This project uses GitHub Actions for continuous integration and deployment.

## Pipeline Architecture
```
Git Push (main branch)
    
GitHub Actions Triggered
    
┌─────────────────────────┐
│   BUILD STAGE           │
│  - Checkout code        │
│  - Configure AWS        │
│  - Login to ECR         │
│  - Build Docker image   │
└──────────┬──────────────┘
           
┌─────────────────────────┐
│   TEST STAGE            │
│  - Run unit tests       │
│  - Security scan        │
└──────────┬──────────────┘
           ↓
┌─────────────────────────┐
│   DEPLOY STAGE          │
│  - Push image to ECR    │
│  - Update ECS service   │
│  - Wait for stability   │
└──────────┬──────────────┘
           ↓
┌─────────────────────────┐
│   VALIDATE STAGE        │
│  - Health check         │
│  - Deployment metrics   │
└──────────┬──────────────┘
           ↓
    SUCCESS / ROLLBACK
```

## Workflow Triggers

**Automatic triggers:**
- Push to `main` branch
- Changes in `src/webapp/` directory
- Changes in workflow file

**Manual triggers:**
- Workflow dispatch (for testing)

## Stages Explained

### 1. Build Stage (2-3 minutes)
- Checks out latest code
- Configures AWS credentials from GitHub Secrets
- Logs into Amazon ECR
- Builds Docker image with commit SHA as tag
- Tags image as 'latest' as well

### 2. Test Stage (1 minute)
- Runs pytest test suite inside Docker container
- Scans image for security vulnerabilities (Trivy)
- Uploads security results to GitHub Security tab
- Currently doesn't block on test failures (for development)

### 3. Deploy Stage (2-3 minutes)
- Pushes both tagged images to ECR
- Updates ECS service with force-new-deployment
- Waits for ECS service to stabilize
- Monitors running task count vs desired count

### 4. Validate Stage (1 minute)
- Retrieves ALB DNS name
- Performs health check on `/health` endpoint
- Retries up to 10 times with 30-second intervals
- Fails deployment if health check doesn't pass

### 5. Rollback (if needed)
- Triggered automatically on any stage failure
- Forces new deployment (ECS uses last stable version)
- Notifies in workflow logs

## Security

### Secrets Management
All sensitive credentials stored as GitHub Secrets:
- `AWS_ACCESS_KEY_ID`
- `AWS_SECRET_ACCESS_KEY`
- `AWS_REGION`
- `AWS_ACCOUNT_ID`

Never committed to repository.

### Security Scanning
- Trivy scans every image before deployment
- Checks for CRITICAL and HIGH severity vulnerabilities
- Results visible in GitHub Security tab
- Can be configured to block deployment on findings

### IAM Permissions
GitHub Actions uses dedicated IAM user with minimal permissions:
- ECR: Push/pull images
- ECS: Update services, describe tasks
- ELB: Describe load balancers (for validation)

## Monitoring

### GitHub Actions Interface
- Real-time logs for each stage
- Success/failure notifications
- Deployment history
- Timing metrics

### AWS CloudWatch
- ECS task logs
- Application logs
- Deployment events

## Comparison to Manual Process

| Aspect | Manual | CI/CD |
|--------|--------|-------|
| Trigger | Human decides to deploy | Automatic on git push |
| Build | Local machine | GitHub runners |
| Tests | Maybe run locally | Always run |
| Security scan | Manual, if remembered | Automatic, every time |
| Push to ECR | Manual commands | Automatic |
| Deploy to ECS | AWS Console or CLI | Automatic |
| Validation | Manual testing | Automated health checks |
| Rollback | Manual, slow | Automatic, fast |
| Logs | Scattered | Centralized |
| Time | 30+ minutes | 8-10 minutes |

## Troubleshooting

### Deployment Fails at Build Stage
- Check Dockerfile syntax
- Verify all dependencies in requirements.txt
- Check GitHub Actions logs for specific error

### Deployment Fails at Test Stage
- Review test output in workflow logs
- Run tests locally to debug
- Check if tests need updated dependencies

### Deployment Fails at Security Scan
- Review Trivy findings
- Update base image if vulnerabilities in OS packages
- Update Python packages if vulnerabilities in libraries

### Deployment Fails at Validation
- Check ECS task logs in CloudWatch
- Verify application starts correctly
- Check security groups allow ALB → ECS traffic
- Verify health endpoint returns 200

### Rollback Triggered
- Check which stage failed
- Review error messages
- Fix issue
- Push new commit (triggers new deployment)

## Future Enhancements

Potential improvements:
- Add integration tests
- Add performance testing
- Blue/green deployments
- Canary deployments
- Slack/email notifications
- Deployment approvals for production