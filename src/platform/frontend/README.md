# Deployment Metrics Platform Frontend

This is the React frontend for the deployment metrics platform. It provides the dashboard and charts used to display deployment records, compare manual and automated deployments, and show statistical analysis results.

## Features

- Dashboard summary cards
- Deployment list view
- Comparison charts
- Statistical analysis view
- Manual deployment simulator interface

## Requirements

- Node.js
- npm

## Setup

Open a terminal in this folder:

```bash
cd src/platform/frontend

# Install dependencies:

npm install

# Create an environment file if needed:

copy .env.example .env

# Then start the development server:

npm start

# The frontend will normally open at:

http://localhost:3000

```
## Backend API URL

The frontend reads the backend API base URL from:

REACT_APP_API_BASE_URL

If no environment variable is set, it defaults to:

http://localhost:5001/api

Example .env
REACT_APP_API_BASE_URL=http://localhost:5001/api

Build for production:
```bash
npm run build
```

## Notes
This frontend does not work by itself.
The backend API in src/platform/backend must also be running.



