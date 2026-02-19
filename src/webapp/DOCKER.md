# Docker Documentation

## Overview

This document explains how to build and run using Docker.

## Prerequisites

- Docker Desktop installed and running
- Docker Compose (included with Docker Desktop)

## Quick Start

### Using Docker Compose (Recommended)
```bash
# Start the application
docker compose up -d

# View logs
docker compose logs -f

# Stop the application
docker compose down
```

Access the application at: http://localhost:5000

### Using Docker CLI
```bash
# Build image
docker build -t task-manager-api:latest .

# Run container
docker run -d -p 5000:5000 --name task-manager task-manager-api:latest

# View logs
docker logs -f task-manager

# Stop and remove container
docker stop task-manager
docker rm task-manager
```

## Docker Commands Reference

### Building
```bash
# Build image
docker build -t task-manager-api:v1 .

# Build with no cache (fresh build)
docker build --no-cache -t task-manager-api:v1 .

# Build with Docker Compose
docker compose build
```

### Running
```bash
# Run in detached mode
docker run -d -p 5000:5000 --name task-manager task-manager-api:latest

# Run with environment variables
docker run -d -p 5000:5000 \
  -e FLASK_ENV=production \
  --name task-manager \
  task-manager-api:latest

# Run with restart policy
docker run -d -p 5000:5000 --restart unless-stopped --name task-manager task-manager-api:latest
```

### Managing Containers
```bash
# List running containers
docker ps

# List all containers (including stopped)
docker ps -a

# Stop container
docker stop task-manager

# Start stopped container
docker start task-manager

# Restart container
docker restart task-manager

# Remove container
docker rm task-manager

# Force remove running container
docker rm -f task-manager
```

### Logs and Debugging
```bash
# View logs
docker logs task-manager

# Follow logs in real-time
docker logs -f task-manager

# View last 100 lines
docker logs --tail 100 task-manager

# Execute command in running container
docker exec task-manager python --version

# Open interactive shell
docker exec -it task-manager /bin/bash

# View container resource usage
docker stats task-manager

# Inspect container configuration
docker inspect task-manager
```

### Images
```bash
# List images
docker images

# Remove image
docker rmi task-manager-api:v1

# Remove all unused images
docker image prune -a

# Tag image
docker tag task-manager-api:latest task-manager-api:v2
```

### Docker Compose Commands
```bash
# Start services
docker compose up -d

# Stop services
docker compose down

# View logs
docker compose logs -f

# Rebuild and restart
docker compose up -d --build

# Stop and remove everything (containers, networks, volumes)
docker compose down -v

# View running services
docker compose ps

# Scale service (run multiple containers)
docker compose up -d --scale web=3
```

## Dockerfile Explained

### Multi-stage Build

Our Dockerfile uses a multi-stage build for optimization:

**Stage 1: Builder**
- Installs build dependencies
- Installs Python packages

**Stage 2: Runtime**
- Copies only necessary files
- Creates non-root user
- Runs application

### Security Features

1. **Non-root user:** Application runs as `appuser`, not root
2. **Minimal base image:** Uses `python:3.11-slim` (smaller attack surface)
3. **No unnecessary packages:** Only runtime dependencies included
4. **Health check:** Automatic container health monitoring

### Environment Variables

- `FLASK_APP` - Application entry point (app.py)
- `FLASK_ENV` - Environment (production/development)
- `PYTHONUNBUFFERED` - Real-time log output
- `PYTHONDONTWRITEBYTECODE` - Don't create .pyc files

## Docker Compose Files

### docker-compose.yml (Production)

- Optimized for production
- Minimal logging
- Auto-restart enabled
- Health checks configured

### docker-compose.dev.yml (Development)

- Code hot-reload with volumes
- Debug mode enabled
- Verbose logging
- No restart policy

**Usage:**
```bash
# Production
docker compose up -d

# Development
docker compose -f docker-compose.dev.yml up -d
```

## Troubleshooting

### Container won't start
```bash
# Check logs for errors
docker compose logs

# Check if port is already in use
netstat -ano | findstr :5000

# Rebuild image
docker compose build --no-cache
docker compose up -d
```

### Application not accessible
```bash
# Check container is running
docker ps

# Check port mapping
docker port task-manager

# Check if app is listening inside container
docker exec task-manager netstat -tuln | grep 5000
```

### Out of disk space
```bash
# Check Docker disk usage
docker system df

# Clean up
docker system prune -a -f
```

### Image build fails
```bash
# Build with no cache
docker build --no-cache -t task-manager-api:latest .

# Check .dockerignore is correct
cat .dockerignore

# Verify Dockerfile syntax
docker build --check .
```

## Best Practices

1. **Use .dockerignore:** Exclude unnecessary files from image
2. **Multi-stage builds:** Separate build and runtime stages
3. **Non-root user:** Never run as root in production
4. **Health checks:** Monitor container health automatically
5. **Minimal base images:** Use slim/alpine variants
6. **Layer caching:** Order Dockerfile commands for better caching
7. **Environment variables:** Externalize configuration
8. **Volume for data:** Use volumes for persistent data
9. **Network isolation:** Use custom networks
10. **Tag images properly:** Use semantic versioning

## Security Checklist

- [x] Non-root user configured
- [x] Minimal base image (slim)
- [x] No secrets in image
- [x] .dockerignore configured
- [x] Health check implemented
- [x] Environment variables used for config
- [ ] Image scanning (to be added in Week 7)
- [ ] Read-only filesystem (future improvement)

## Performance Tips

1. **Order matters:** Put frequently changing files last in Dockerfile
2. **Combine RUN commands:** Reduces layers
3. **Use .dockerignore:** Faster context transfer
4. **Multi-stage builds:** Smaller final images
5. **Cache dependencies:** Copy requirements.txt before code

## Resource Limits

Set memory and CPU limits in docker-compose.yml:
```yaml
services:
  web:
    deploy:
      resources:
        limits:
          cpus: '0.5'
          memory: 512M
        reservations:
          cpus: '0.25'
          memory: 256M
```

## Next Steps

- Week 4: Deploy to AWS ECS
- Week 7: Add container vulnerability scanning
- Production: Consider orchestration (Kubernetes/ECS)

## References

- [Docker Documentation](https://docs.docker.com/)
- [Dockerfile Best Practices](https://docs.docker.com/develop/develop-images/dockerfile_best-practices/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)