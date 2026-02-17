# Task Manager API

A simple Flask REST API for managing tasks, built as a demonstration application for CI/CD pipeline deployment.

## Features

-  Create, Read, Update, Delete (CRUD) operations for tasks
-  RESTful API design
-  Web interface for task management
-  Health check endpoint for monitoring
-  CORS enabled for cross-origin requests
-  In-memory storage (no database required)

## Technology Stack

- **Framework:** Flask 3.0.2
- **Language:** Python 3.11+
- **CORS:** Flask-CORS
- **Frontend:** Vanilla JavaScript + HTML/CSS

## API Endpoints

### Health Check
```
GET /health
```
Returns the health status of the application.

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2025-02-20T10:30:00",
  "service": "task-manager-api",
  "version": "1.0.0"
}
```

### Get All Tasks
```
GET /api/tasks
```
Returns all tasks.

**Response:**
```json
{
  "tasks": [...],
  "count": 5
}
```

### Get Single Task
```
GET /api/tasks/{task_id}
```
Returns a specific task by ID.

**Response:**
```json
{
  "id": "uuid-here",
  "title": "Task title",
  "description": "Task description",
  "completed": false,
  "created_at": "2025-02-20T10:30:00",
  "updated_at": "2025-02-20T10:30:00"
}
```

### Create Task
```
POST /api/tasks
```
Creates a new task.

**Request Body:**
```json
{
  "title": "Task title",
  "description": "Optional description"
}
```

**Response:** 201 Created with task object

### Update Task
```
PUT /api/tasks/{task_id}
```
Updates an existing task.

**Request Body:**
```json
{
  "title": "Updated title",
  "description": "Updated description",
  "completed": true
}
```

**Response:** 200 OK with updated task object

### Delete Task
```
DELETE /api/tasks/{task_id}
```
Deletes a task.

**Response:**
```json
{
  "message": "Task deleted successfully",
  "id": "task-id"
}
```

## Local Development

### Prerequisites

- Python 3.11 or higher
- pip (Python package manager)

### Setup

1. **Create virtual environment:**
```bash
   python -m venv venv
```

2. **Activate virtual environment:**
   
   **Windows (PowerShell):**
```powershell
   .\venv\Scripts\Activate.ps1
```
   
   **macOS/Linux:**
```bash
   source venv/bin/activate
```

3. **Install dependencies:**
```bash
   pip install -r requirements.txt
```

4. **Run the application:**
```bash
   python app.py
```

5. **Access the application:**
   - Web Interface: http://localhost:5000
   - API: http://localhost:5000/api/tasks
   - Health Check: http://localhost:5000/health

### Development Mode

The application runs in debug mode by default, which provides:
- Auto-reload on code changes
- Detailed error messages
- Interactive debugger

**Warning:** Do not use debug mode in production!

## Testing the API

### Using cURL (Windows PowerShell)

**Get all tasks:**
```powershell
curl http://localhost:5000/api/tasks
```

**Create a task:**
```powershell
$body = @{
    title = "New Task"
    description = "Task description"
} | ConvertTo-Json

Invoke-WebRequest -Uri http://localhost:5000/api/tasks -Method POST -Body $body -ContentType "application/json"
```

**Update a task:**
```powershell
$body = @{
    completed = $true
} | ConvertTo-Json

Invoke-WebRequest -Uri http://localhost:5000/api/tasks/TASK_ID -Method PUT -Body $body -ContentType "application/json"
```

**Delete a task:**
```powershell
Invoke-WebRequest -Uri http://localhost:5000/api/tasks/TASK_ID -Method DELETE
```

## Project Structure
```
src/webapp/
├── app.py              # Main Flask application
├── requirements.txt    # Python dependencies
├── README.md          # This file
├── templates/
│   └── index.html     # Web interface
└── venv/              # Virtual environment (not committed)
```

## Environment Variables

Currently, the application uses default settings. Future environment variables:

- `FLASK_ENV` - Environment (development/production)
- `FLASK_APP` - Application entry point
- `PORT` - Port number (default: 5000)

## Known Limitations

- **In-memory storage:** Tasks are lost when the application restarts
- **No authentication:** API is publicly accessible
- **Single instance:** No session persistence across instances
- **No database:** Not suitable for production data persistence

These limitations are intentional for demonstration purposes.

## Future Enhancements (Out of Scope)

- Database integration (PostgreSQL/MongoDB)
- User authentication and authorization
- Task categories and tags
- Search and filtering
- Pagination for large task lists
- WebSocket support for real-time updates

## Contributing

This is a demonstration project for CI/CD pipeline evaluation. Not accepting contributions.

## License

MIT License

## Author

[Your Name] - Computer Science Individual Project