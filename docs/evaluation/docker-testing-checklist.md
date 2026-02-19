# Docker Container Testing Checklist

## Test Date: 18/02/2026

---

## 1. Build Tests

### Build from scratch
```bash
docker build --no-cache -t task-manager-api:test .
```
- [x] Build completes without errors
- [x] No security warnings
- Build time: 36.9 seconds
- Final image size: MB

### Build with cache
```bash
docker build -t task-manager-api:test .
```
- [x] Build uses cache layers
- Build time (cached): 4.0 seconds

---

## 2. Container Startup Tests

### Basic startup
```bash
docker run -d -p 5000:5000 --name test-container task-manager-api:test
```
- [x] Container starts successfully
- [x] No errors in logs

### Check container health
```bash
docker ps
```
- [x] STATUS shows "healthy" (wait 30 seconds)
- [x] Port mapping correct: 0.0.0.0:5000->5000/tcp

---

## 3. Application Tests

### Health endpoint
```bash
curl http://localhost:5000/health
```
- [x] Returns HTTP 200
- [x] JSON response valid
- [x] Shows "healthy" status

### Web interface
- [x] Browser loads http://localhost:5000
- [x] Interface renders correctly
- [x] No console errors

### API functionality
- [x] Can create task via API
- [x] Can read tasks
- [x] Can update task
- [x] Can delete task
- [x] Stats endpoint works

---

## 4. Performance Tests

### Resource usage (run for 2 minutes)
```bash
docker stats test-container
```
- CPU usage: 0.04 %
- Memory usage: 24.88 MB / 3.675 GB
- Network I/O stable: 10.4 KB / 17.4 KB

### Load test (create 100 tasks)
```bash
for i in 1..100; do
  curl -X POST http://localhost:5000/api/tasks \
    -H "Content-Type: application/json" \
    -d '{"title": "Task '$i'"}'
done
```
- [x] All requests succeed
- [x] No memory leaks
- [x] Response time consistent

---

## 5. Reliability Tests

### Container restart
```bash
docker restart test-container
```
- [x] Container restarts successfully
- [x] Application comes back up
- [x] No data persistence issues (expected - in-memory storage)

### Force kill and auto-restart
```bash
docker run -d -p 5000:5000 --restart unless-stopped --name test-restart task-manager-api:test
docker kill test-restart
# Wait 5 seconds
docker ps
```
- [x] Container automatically restarts
- [x] Application accessible again

---

## 6. Docker Compose Tests

### Start services
```bash
docker compose up -d
```
- [x] Services start successfully
- [x] Network created
- [x] Container healthy

### Logs
```bash
docker compose logs
```
- [x] No error messages
- [x] Application logs visible

### Stop and cleanup
```bash
docker compose down
```
- [x] Containers stopped
- [x] Containers removed
- [x] Network removed

---

## 7. Security Tests

### Non-root user check
```bash
docker exec test-container whoami
```
- [x] Shows "appuser" (not root)

### File permissions check
```bash
docker exec test-container ls -la /app
```
- [x] Files owned by appuser

### No secrets in image
```bash
docker history task-manager-api:test
```
- [x] No sensitive data visible in layers
- [x] No .env files included

---

## 8. Debugging Tests

### Shell access
```bash
docker exec -it test-container /bin/bash
```
- [x] Can access container shell
- [x] Python available
- [x] Application files present

### Log access
```bash
docker logs test-container
```
- [x] Logs visible and formatted
- [x] Timestamps correct
- [x] Log level appropriate

---

## 9. Cleanup Tests

### Remove container
```bash
docker stop test-container
docker rm test-container
```
- [x] Container stops cleanly
- [x] Container removes without errors

### Remove image
```bash
docker rmi task-manager-api:test
```
- [x] Image removes successfully

---

## 10. Edge Case Tests

### Invalid port mapping
```bash
docker run -d -p 9999:5000 --name test-port task-manager-api:test
```
- [x] Container starts
- [x] Accessible on http://localhost:9999
- [x] Application works normally

### Environment variable override
```bash
docker run -d -p 5000:5000 -e FLASK_ENV=development --name test-env task-manager-api:test
docker logs test-env
```
- [ ] Environment variable applied
- [ ] Debug mode enabled (if FLASK_ENV=development)

---






