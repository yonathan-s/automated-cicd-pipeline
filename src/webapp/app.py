"""
Task Manager API
A simple Flask REST API for managing tasks
"""

from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# In-memory task storage
tasks = [
    {"id": 1, "title": "Sample task 1", "completed": False},
    {"id": 2, "title": "Sample task 2", "completed": True}
]

# Counter for task IDs
next_id = 3


@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "service": "Task Manager API",
        "version": "1.0.0"
    })


@app.route('/tasks', methods=['GET'])
def get_tasks():
    """Get all tasks"""
    return jsonify(tasks)


@app.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    """Get a specific task by ID"""
    task = next((t for t in tasks if t['id'] == task_id), None)
    if task is None:
        return jsonify({"error": "Task not found"}), 404
    return jsonify(task)


@app.route('/tasks', methods=['POST'])
def create_task():
    """Create a new task"""
    global next_id
    
    if not request.json or 'title' not in request.json:
        return jsonify({"error": "Title is required"}), 400
    
    task = {
        "id": next_id,
        "title": request.json['title'],
        "completed": request.json.get('completed', False)
    }
    
    tasks.append(task)
    next_id += 1
    
    return jsonify(task), 201


@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    """Update an existing task"""
    task = next((t for t in tasks if t['id'] == task_id), None)
    if task is None:
        return jsonify({"error": "Task not found"}), 404
    
    if not request.json:
        return jsonify({"error": "Invalid request"}), 400
    
    task['title'] = request.json.get('title', task['title'])
    task['completed'] = request.json.get('completed', task['completed'])
    
    return jsonify(task)


@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    """Delete a task"""
    global tasks
    task = next((t for t in tasks if t['id'] == task_id), None)
    if task is None:
        return jsonify({"error": "Task not found"}), 404
    
    tasks = [t for t in tasks if t['id'] != task_id]
    return jsonify({"message": "Task deleted successfully"})


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

#automated deployment test
