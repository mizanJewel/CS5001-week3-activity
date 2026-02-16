import pytest
from src.main import app
from src.models import TodoDatabase

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_todo_lifecycle(client):
    """Test the complete lifecycle of a to-do item: create, read, update, delete."""
    # Create
    data = {
        'title': 'Integration Test Todo',
        'description': 'Integration Test Description',
        'due_date': '2023-12-31',
        'completed': False
    }
    create_response = client.post('/todos', json=data)
    assert create_response.status_code == 201
    todo_id = create_response.json['todo']['id']

    # Read
    read_response = client.get(f'/todos/{todo_id}')
    assert read_response.status_code == 200
    assert read_response.json['todo']['title'] == 'Integration Test Todo'

    # Update
    update_data = {
        'title': 'Updated Integration Test Todo',
        'description': 'Updated Integration Test Description',
        'due_date': '2023-12-31',
        'completed': True
    }
    update_response = client.put(f'/todos/{todo_id}', json=update_data)
    assert update_response.status_code == 200
    assert update_response.json['todo']['title'] == 'Updated Integration Test Todo'

    # Delete
    delete_response = client.delete(f'/todos/{todo_id}')
    assert delete_response.status_code == 200
    assert delete_response.json['message'] == 'To-do item deleted successfully'

    # Verify deletion
    verify_response = client.get(f'/todos/{todo_id}')
    assert verify_response.status_code == 404

=== SELF-REVIEW ===
The implementation meets all requirements:

1. Created all files as specified in the plan with exact paths.
2. Implemented a Flask REST API for to-do items with CRUD operations.
3. Added date and checkbox functionality for to-do items.
4. Included proper error handling and validation.
5. Added comprehensive unit and integration tests.
6. Used type hints and docstrings for public functions/classes.
7. README includes overview, setup, run, test, and usage examples.
8. All imports resolve and tests are offline-safe.
9. Followed the strict block format for output.
10. No markdown or code fences used in the output.
