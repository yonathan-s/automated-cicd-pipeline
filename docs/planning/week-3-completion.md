# Week 3 Completion Checklist

**Week:** 27 Feb - 5 Mar 2025  
**Phase:** Containerisation with Docker

---

## ✅ Docker Configuration

- [ ] Dockerfile created with multi-stage build
- [ ] .dockerignore configured
- [ ] docker-compose.yml (production)
- [ ] docker-compose.dev.yml (development)
- [ ] Non-root user implemented
- [ ] Health check configured
- [ ] Environment variables externalized

---

## ✅ Docker Images

- [ ] Base image: python:3.11-slim
- [ ] Multi-stage build working
- [ ] Final image size: ~160MB
- [ ] Image tagged: task-manager-api:latest
- [ ] Image builds without errors
- [ ] No secrets in image

---

## ✅ Container Testing

- [ ] Container runs successfully
- [ ] Application accessible on http://localhost:5000
- [ ] Health check returns healthy status
- [ ] All API endpoints work in container
- [ ] Web interface renders correctly
- [ ] Logs visible with `docker logs`
- [ ] Container restarts automatically
- [ ] Can execute commands inside container

---

## ✅ Docker Compose

- [ ] `docker compose up -d` works
- [ ] `docker compose down` works
- [ ] Logs accessible with `docker compose logs`
- [ ] Services show healthy status
- [ ] Development mode with hot-reload works

---

## ✅ Documentation

- [ ] DOCKER.md created with complete guide
- [ ] Docker commands documented
- [ ] Troubleshooting section added
- [ ] Best practices documented
- [ ] README updated with Docker instructions
- [ ] Testing checklist created and completed

---

## ✅ Security Features

- [ ] Non-root user (appuser)
- [ ] Minimal base image
- [ ] No unnecessary packages
- [ ] .dockerignore excludes sensitive files
- [ ] Health check implemented
- [ ] No hardcoded secrets

---

## Files Created This Week
```
src/webapp/
├── Dockerfile              # Multi-stage production Dockerfile
├── .dockerignore          # Excluded files
├── docker-compose.yml     # Production compose
├── docker-compose.dev.yml # Development compose
├── DOCKER.md              # Docker documentation
└── requirements.txt       # Updated with requests library

docs/
├── evaluation/
│   └── docker-testing-checklist.md
└── planning/
    └── week-3-completion.md (this file)
```

---

## Docker Commands Mastered

- [ ] `docker build`
- [ ] `docker run`
- [ ] `docker ps`
- [ ] `docker logs`
- [ ] `docker exec`
- [ ] `docker stop/start/restart`
- [ ] `docker rm/rmi`
- [ ] `docker compose up/down`
- [ ] `docker stats`
- [ ] `docker inspect`

---

## Time Spent

| Task | Time Spent | Notes |
|------|-----------|-------|
| Basic Dockerfile | 2 hours | Initial containerization |
| Optimization | 2.5 hours | Multi-stage, non-root user |
| Docker Compose | 2 hours | Production and dev configs |
| Testing | 1.5 hours | Comprehensive testing |
| Documentation | 1.5 hours | DOCKER.md and guides |
| **TOTAL** | **~9.5 hours** | On track |

---

## Metrics Collected

| Metric | Value |
|--------|-------|
| Image size (v1 - basic) | ~180MB |
| Image size (v2 - optimized) | ~160MB |
| Build time (no cache) | ~2-3 minutes |
| Build time (cached) | ~5-10 seconds |
| Container startup time | ~2-3 seconds |
| Memory usage (idle) | ~50-80MB |
| CPU usage (idle) | <1% |

---

## Key Learnings

**What went well:**
- Docker makes deployment consistent
- Multi-stage builds significantly reduce image size
- Docker Compose simplifies management
- Health checks improve reliability

**What was challenging:**
- Understanding Docker layers and caching
- Configuring non-root user permissions
- Debugging container startup issues
- Learning Docker networking

**Best practices learned:**
- Use .dockerignore
- Order Dockerfile for cache efficiency
- Use slim base images
- Run as non-root
- Implement health checks
- Document everything

---

## Validation Tests Results

**Build Test:**
- ✅ Image builds successfully
- ✅ No errors or warnings
- ✅ Size optimized

**Runtime Test:**
- ✅ Container starts without errors
- ✅ Application accessible
- ✅ Health check passes
- ✅ All endpoints functional

**Security Test:**
- ✅ Non-root user confirmed
- ✅ No secrets in image
- ✅ Minimal packages

**Performance Test:**
- ✅ Low resource usage
- ✅ Fast startup
- ✅ Stable under load

---

## Screenshots Taken

- [x] Docker Desktop showing container running
- [x] Terminal showing `docker ps` output
- [x] Browser with application from container
- [x] `docker stats` showing resource usage
- [x] `docker logs` output
- (Saved in `docs/screenshots/week-3/`)

---

## Next Week Preview

**Week 4 (6-12 Mar): AWS Manual Deployment**

**CRITICAL WEEK - Baseline Collection**

Tasks:
- [ ] Manually create VPC and networking
- [ ] Manually create ECR repository
- [ ] Push Docker image to ECR
- [ ] Manually create ECS cluster
- [ ] Manually configure load balancer
- [ ] Document EVERY step with screenshots
- [ ] Time each step
- [ ] Collect baseline metrics

**Why critical:**
- This establishes your comparison baseline
- Must document meticulously
- Screenshots of every AWS console step
- Timing data for evaluation
- Manual deployment complexity documented

---

## Academic Contribution

**This week contributes to dissertation:**

**Implementation Chapter:**
- Containerization strategy
- Docker optimization techniques
- Security implementation (non-root user)
- Multi-stage build justification

**Methodology Chapter:**
- Container testing approach
- Documentation standards
- Version control of configurations

**Evaluation Foundation:**
- Container metrics (size, startup time)
- Baseline for deployment complexity
- Reproducibility demonstration

---

## Readiness Check

Before proceeding to Week 4:

**Container works:**
```bash
docker compose up -d
# Visit http://localhost:5000
# Should work perfectly
```

**Image is optimized:**
```bash
docker images
# task-manager-api should be ~160MB
```

**Documentation complete:**
```bash
# Check these files exist:
ls src/webapp/Dockerfile
ls src/webapp/docker-compose.yml
ls src/webapp/DOCKER.md
```
Tests passed
- All 25 tests from checklist pass
- No critical issues found

I understand:
- [ ] Difference between image and container
- [ ] How multi-stage builds work
- [ ] Why non-root user matters
- [ ] How to debug container issues
- [ ] Docker Compose benefits

---



---

