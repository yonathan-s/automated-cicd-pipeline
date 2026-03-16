"""
Test suite for Task Manager API
"""
import pytest
import json
from app import app, tasks


@pytest.fixture
def client():
    """Create test client"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


@pytest.fixture(autouse=True)
def reset_tasks():
    """Reset tasks before each test"""
    tasks.clear()
    tasks.extend([
        {"id": 1, "title": "Test task 1", "completed": False},
        {"id": 2, "title": "Test task 2", "completed": True}
    ])


def test_health_endpoint(client):
    """Test health check endpoint"""
    response = client.get('/health')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['status'] == 'healthy'


def test_get_all_tasks(client):
    """Test getting all tasks"""
    response = client.get('/tasks')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert len(data) == 2


def test_get_task_by_id(client):
    """Test getting specific task"""
    response = client.get('/tasks/1')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['title'] == 'Test task 1'


def test_get_nonexistent_task(client):
    """Test getting task that doesn't exist"""
    response = client.get('/tasks/999')
    assert response.status_code == 404


def test_create_task(client):
    """Test creating new task"""
    new_task = {'title': 'New test task', 'completed': False}
    response = client.post('/tasks',
                          data=json.dumps(new_task),
                          content_type='application/json')
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data['title'] == 'New test task'
    assert 'id' in data


def test_create_task_missing_title(client):
    """Test creating task without title"""
    new_task = {'completed': False}
    response = client.post('/tasks',
                          data=json.dumps(new_task),
                          content_type='application/json')
    assert response.status_code == 400


def test_update_task(client):
    """Test updating existing task"""
    update_data = {'title': 'Updated task', 'completed': True}
    response = client.put('/tasks/1',
                         data=json.dumps(update_data),
                         content_type='application/json')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['title'] == 'Updated task'
    assert data['completed'] is True


def test_update_nonexistent_task(client):
    """Test updating task that doesn't exist"""
    update_data = {'title': 'Updated task'}
    response = client.put('/tasks/999',
                         data=json.dumps(update_data),
                         content_type='application/json')
    assert response.status_code == 404


def test_delete_task(client):
    """Test deleting task"""
    response = client.delete('/tasks/1')
    assert response.status_code == 200
    
    # Verify task was deleted
    response = client.get('/tasks/1')
    assert response.status_code == 404


def test_delete_nonexistent_task(client):
    """Test deleting task that doesn't exist"""
    response = client.delete('/tasks/999')
    assert response.status_code == 404