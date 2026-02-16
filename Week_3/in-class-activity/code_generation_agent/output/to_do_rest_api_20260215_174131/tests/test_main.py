import pytest
from src.main import app
from src.models import ToDo, TodoDatabase

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_get_todos_empty(client):
    """Test getting all to-do items when the database is empty."""
    response = client.get('/todos')
    assert response.status_code == 200
    assert response.json == {'todos': []}

def test_create_todo(client):
    """Test creating a new to-do item."""
    data = {
        'title': 'Test Todo',
        'description': 'Test Description',
        'due_date': '2023-12-31',
        'completed': False
    }
    response = client.post('/todos', json=data)
    assert response.status_code == 201
    assert response.json['todo']['title'] == 'Test Todo'

def test_get_todo(client):
    """Test getting a specific to-do item."""
    data = {
        'title': 'Test Todo',
        'description': 'Test Description',
        'due_date': '2023-12-31',
        'completed': False
    }
    create_response = client.post('/todos', json=data)
    todo_id = create_response.json['todo']['id']
    response = client.get(f'/todos/{todo_id}')
    assert response.status_code == 200
    assert response.json['todo']['title'] == 'Test Todo'

def test_update_todo(client):
    """Test updating a to-do item."""
    data = {
        'title': 'Test Todo',
        'description': 'Test Description',
        'due_date': '2023-12-31',
        'completed': False
    }
    create_response = client.post('/todos', json=data)
    todo_id = create_response.json['todo']['id']
    update_data = {
        'title': 'Updated Todo',
        'description': 'Updated Description',
        'due_date': '2023-12-31',
        'completed': True
    }
    response = client.put(f'/todos/{todo_id}', json=update_data)
    assert response.status_code == 200
    assert response.json['todo']['title'] == 'Updated Todo'

def test_delete_todo(client):
    """Test deleting a to-do item."""
    data = {
        'title': 'Test Todo',
        'description': 'Test Description',
        'due_date': '2023-12-31',
        'completed': False
    }
    create_response = client.post('/todos', json=data)
    todo_id = create_response.json['todo']['id']
    response = client.delete(f'/todos/{todo_id}')
    assert response.status_code == 200
    assert response.json['message'] == 'To-do item deleted successfully'
