# Deployment Metrics Platform

An interactive platform for collecting, analyzing, and visualizing deployment metrics.

## Features

- 📊 Real-time deployment tracking
- 📈 Statistical analysis (t-tests, chi-square, effect sizes)
- 🔄 Manual deployment simulator
- 📉 Comparative visualizations
- 🔗 GitHub Actions integration

## Quick Start

### Start the Platform
```powershell
cd src/platform
.\start-platform.ps1
```

Platform runs on: http://localhost:5000

### API Endpoints

**Deployments:**
- `GET /api/deployments` - List all deployments
- `POST /api/deployments` - Create deployment record
- `GET /api/deployments/:id` - Get specific deployment

**Statistics:**
- `GET /api/statistics` - Get deployment statistics
- `GET /api/statistics/summary` - Dashboard summary
- `GET /api/analysis/full` - Complete statistical analysis

**Simulator:**
- `POST /api/simulate/manual` - Simulate single manual deployment
- `POST /api/simulate/manual/batch` - Simulate multiple (default 10)
- `GET /api/simulate/summary` - Simulation statistics

## Integration with CI/CD

The platform automatically receives metrics from GitHub Actions after each deployment.

Metrics include:
- Deployment duration
- Success/failure status
- Test results
- Security scan results
- Commit info

## Development

**Backend Stack:**
- Flask (Python web framework)
- SQLAlchemy (Database ORM)
- SQLite (Database)
- NumPy & SciPy (Statistical analysis)

**Data Model:**
- Deployments (main records)
- DeploymentErrors (error tracking)
- DeploymentMetrics (custom metrics)

## Usage Examples

### Simulate Manual Deployments
```bash
# Simulate 10 manual deployments
curl -X POST http://localhost:5000/api/simulate/manual/batch \
  -H "Content-Type: application/json" \
  -d '{"count": 10, "spread_days": 30}'
```

### Get Statistical Analysis
```bash
curl http://localhost:5000/api/analysis/full
```

### View Latest Deployments
```bash
curl http://localhost:5000/api/deployments?limit=5
```

## Database

SQLite database located at: `backend/deployments.db`

To reset database: Delete the file and restart the platform.

