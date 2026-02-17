"""
Unit tests for the Task Manager API
"""

import pytest
import sys
import os

# Add src/webapp to path so we can import app
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src/webapp')))

from app import app, tasks

@pytest.fixture
def client():
    """Create a test client"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        # Clear tasks before each test
        tasks.clear()
        yield client

def test_health_check(client):
    """Test the health check endpoint"""
    response = client.get('/health')
    assert response.status_code == 200
    
    data = response.get_json()
    assert data['status'] == 'healthy'
    assert 'timestamp' in data
    assert data['service'] == 'task-manager-api'

def test_get_tasks_empty(client):
    """Test getting tasks when none exist"""
    response = client.get('/api/tasks')
    assert response.status_code == 200
    
    data = response.get_json()
    assert data['count'] == 0
    assert data['tasks'] == []

def test_create_task(client):
    """Test creating a new task"""
    task_data = {
        'title': 'Test Task',
        'description': 'This is a test task'
    }
    
    response = client.post('/api/tasks', json=task_data)
    assert response.status_code == 201
    
    data = response.get_json()
    assert data['title'] == 'Test Task'
    assert data['description'] == 'This is a test task'
    assert data['completed'] == False
    assert 'id' in data
    assert 'created_at' in data

def test_create_task_without_title(client):
    """Test that creating a task without title fails"""
    task_data = {
        'description': 'No title'
    }
    
    response = client.post('/api/tasks', json=task_data)
    assert response.status_code == 400
    
    data = response.get_json()
    assert 'error' in data

def test_get_task_by_id(client):
    """Test getting a specific task by ID"""
    # First create a task
    task_data = {'title': 'Test Task'}
    create_response = client.post('/api/tasks', json=task_data)
    created_task = create_response.get_json()
    task_id = created_task['id']
    
    # Now get it
    response = client.get(f'/api/tasks/{task_id}')
    assert response.status_code == 200
    
    data = response.get_json()
    assert data['id'] == task_id
    assert data['title'] == 'Test Task'

def test_get_nonexistent_task(client):
    """Test getting a task that doesn't exist"""
    response = client.get('/api/tasks/nonexistent-id')
    assert response.status_code == 404

def test_update_task(client):
    """Test updating a task"""
    # Create a task
    task_data = {'title': 'Original Title'}
    create_response = client.post('/api/tasks', json=task_data)
    task_id = create_response.get_json()['id']
    
    # Update it
    update_data = {
        'title': 'Updated Title',
        'completed': True
    }
    response = client.put(f'/api/tasks/{task_id}', json=update_data)
    assert response.status_code == 200
    
    data = response.get_json()
    assert data['title'] == 'Updated Title'
    assert data['completed'] == True

def test_delete_task(client):
    """Test deleting a task"""
    # Create a task
    task_data = {'title': 'Task to Delete'}
    create_response = client.post('/api/tasks', json=task_data)
    task_id = create_response.get_json()['id']
    
    # Delete it
    response = client.delete(f'/api/tasks/{task_id}')
    assert response.status_code == 200
    
    # Verify it's gone
    get_response = client.get(f'/api/tasks/{task_id}')
    assert get_response.status_code == 404

def test_get_stats(client):
    """Test the stats endpoint"""
    # Create some tasks
    client.post('/api/tasks', json={'title': 'Task 1'})
    client.post('/api/tasks', json={'title': 'Task 2'})
    
    # Mark one as completed
    tasks[0]['completed'] = True
    
    response = client.get('/api/stats')
    assert response.status_code == 200
    
    data = response.get_json()
    assert data['total'] == 2
    assert data['completed'] == 1
    assert data['pending'] == 1
    assert data['completion_rate'] == 50.0

def test_multiple_tasks(client):
    """Test creating and retrieving multiple tasks"""
    # Create 3 tasks
    for i in range(3):
        client.post('/api/tasks', json={'title': f'Task {i+1}'})
    
    # Get all tasks
    response = client.get('/api/tasks')
    data = response.get_json()
    
    assert data['count'] == 3
    assert len(data['tasks']) == 3