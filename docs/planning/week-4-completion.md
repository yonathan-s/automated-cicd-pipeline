# Week 4 Completion Report

**Week:** 6-12 March 2025
**Phase:** AWS Manual Deployment (Baseline Collection)

---

## Objectives Achieved

- Manual deployment of containerized application to AWS
- Complete infrastructure setup from scratch
- Application accessible via Application Load Balancer
- Monitoring and logging configured
- Comprehensive baseline documentation collected

---

## Resources Created Summary

**Total AWS Resources:** 24
**Total Time Invested:** ~12 hours
**Total Errors Encountered:** 15
**Total Screenshots:** ~60

---

## Deployment Milestones

- Day 1: ECR and Docker image
- Day 2: VPC and networking
- Day 3: Security groups and IAM
- Day 4: ECS cluster and task definition
- Day 5: Application Load Balancer
- Day 6: ECS service deployment
- Day 7: CloudWatch monitoring

---

## Application Status

**Status:** DEPLOYED AND OPERATIONAL
**URL:** http://[Your ALB DNS]
**Tasks Running:** 2/2
**Health Status:** Healthy
**Logs:** Flowing to CloudWatch
**Monitoring:** Dashboard active
**Alarms:** Configured

---

## Baseline Metrics Collected

### Deployment Time
- **Total time:** ~12 hours
- **Steps required:** 20 major steps
- **Console interactions:** ~30 different screens
- **Manual configurations:** ~150+ form fields

### Reliability
- **Errors encountered:** 15
- **Time fixing errors:** ~2 hours
- **Success rate:** 100% (after corrections)

### Repeatability
- **Documentation burden:** High (60 screenshots, detailed logs)
- **Reproducibility:** Moderate (human error likely in repeat attempts)

### Security
- **Manual security checks:** Configuration review only
- **Automated security scans:** ECR image scanning only

### Monitoring
- **Visibility:** Good (CloudWatch dashboard)
- **Setup time:** 45 minutes manual
- **Metrics tracked:** CPU, Memory, Request count, Response time

---

## Key Findings

### Manual Deployment Challenges Identified

1. **Time-consuming:** 12 hours for initial deployment
2. **Error-prone:** 15 configuration errors
3. **Complex:** Requires deep AWS knowledge
4. **Documentation-heavy:** Manual screenshot/logging burden
5. **Difficult to reproduce:** Human variability
6. **No version control:** Infrastructure configuration not tracked
7. **Slow iteration:** Changes require manual console work

### Skills Required

- VPC networking fundamentals
- Security groups and IAM policies
- Container orchestration concepts
- Load balancer configuration
- CloudWatch monitoring
- Troubleshooting AWS services
- Architecture design

---

## Documentation Artifacts

- Manual deployment log (detailed)
- Timing data (CSV format)
- Screenshot collection (60+ images)
- Resource inventory
- Error tracking log
- Verification checklists
- Architecture diagrams
- Deployment summary

---

## Baseline Established

This manual deployment serves as the control group for comparative evaluation.

**Baseline characteristics:**
- Deployment time: ~12 hours
- Error rate: 15 errors / 20 steps = 75% error rate
- Manual steps: ~150 configurations
- Knowledge required: Expert level AWS
- Repeatability: Low (manual process)
- Documentation: High burden

**Next Phase:** Week 5 will automate this entire process with Terraform, reducing deployment to a single command.

---

## Academic Contribution

This week provides:
- **Methodology chapter:** Baseline data collection process
- **Evaluation chapter:** Control group metrics
- **Results chapter:** Comparison data for manual approach
- **Discussion chapter:** Manual deployment limitations

---

## Screenshots Organized
```
docs/screenshots/week-4-manual-deployment/
├── day1-ecr/
├── day2-networking/
├── day3-security/
├── day4-ecs-setup/
├── day5-load-balancer/
├── day6-deployment/
├── day7-monitoring/
└── testing/
```

---

## Files Created This Week

- docs/evaluation/manual-deployment-log.md
- docs/evaluation/manual-deployment-timing.csv
- docs/evaluation/manual-deployment-test-log.md
- docs/evaluation/manual-deployment-summary.md
- docs/evaluation/network-verification-checklist.md
- docs/evaluation/security-verification-checklist.md
- docs/evaluation/alb-verification-checklist.md
- docs/evaluation/manual-resources-created.md
- docs/architecture/manual-network-setup.md
- docs/architecture/manual-security-setup.md
- docs/architecture/iam-roles-explained.md
- docs/planning/week-4-completion.md

---

## Week 4 Status

**STATUS:** COMPLETE

**Ready for Week 5:** YES

**Baseline Data Quality:** EXCELLENT

**Application Status:** LIVE AND OPERATIONAL

---

## Next Week Preview

**Week 5: Infrastructure as Code with Terraform**

Will automate everything from Week 4 using Terraform:
- Single command deployment
- Version-controlled infrastructure
- Reproducible builds
- No manual console work
- Reduced deployment time (hours → minutes)

**Expected time:** 10-12 hours to write Terraform code
**Expected result:** Infrastructure deployable in <5 minutes