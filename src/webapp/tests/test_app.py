"""
Test suite for final Task Manager API
"""

import json
import pytest
from app import app, tasks


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


@pytest.fixture(autouse=True)
def reset_tasks():
    tasks.clear()
    tasks.extend([
        {
            "id": "task-1",
            "title": "Test task 1",
            "description": "First test task",
            "completed": False,
            "created_at": "2026-01-01T10:00:00",
            "updated_at": "2026-01-01T10:00:00"
        },
        {
            "id": "task-2",
            "title": "Test task 2",
            "description": "Second test task",
            "completed": True,
            "created_at": "2026-01-01T10:05:00",
            "updated_at": "2026-01-01T10:05:00"
        }
    ])


def test_home_page(client):
    response = client.get('/')
    assert response.status_code == 200


def test_health_endpoint(client):
    response = client.get('/health')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['status'] == 'healthy'


def test_get_all_tasks(client):
    response = client.get('/api/tasks')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['count'] == 2
    assert len(data['tasks']) == 2


def test_get_single_task(client):
    response = client.get('/api/tasks/task-1')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['title'] == 'Test task 1'


def test_get_missing_task(client):
    response = client.get('/api/tasks/does-not-exist')
    assert response.status_code == 404


def test_create_task(client):
    payload = {
        "title": "New task",
        "description": "Created during test"
    }
    response = client.post(
        '/api/tasks',
        data=json.dumps(payload),
        content_type='application/json'
    )
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data['title'] == 'New task'
    assert data['description'] == 'Created during test'
    assert 'id' in data


def test_create_task_missing_title(client):
    payload = {"description": "No title here"}
    response = client.post(
        '/api/tasks',
        data=json.dumps(payload),
        content_type='application/json'
    )
    assert response.status_code == 400


def test_update_task(client):
    payload = {
        "title": "Updated task title",
        "completed": True
    }
    response = client.put(
        '/api/tasks/task-1',
        data=json.dumps(payload),
        content_type='application/json'
    )
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['title'] == 'Updated task title'
    assert data['completed'] is True


def test_delete_task(client):
    response = client.delete('/api/tasks/task-1')
    assert response.status_code == 200

    response = client.get('/api/tasks/task-1')
    assert response.status_code == 404


def test_get_stats(client):
    response = client.get('/api/stats')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['total'] == 2
    assert data['completed'] == 1
    assert data['pending'] == 1