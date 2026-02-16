from src.utils import validate_todo_data

def test_validate_todo_data_valid():
    """Test validating valid to-do data."""
    data = {
        'title': 'Test Todo',
        'description': 'Test Description',
        'due_date': '2023-12-31',
        'completed': False
    }
    errors = validate_todo_data(data)
    assert errors == []

def test_validate_todo_data_missing_title():
    """Test validating to-do data with missing title."""
    data = {
        'description': 'Test Description',
        'due_date': '2023-12-31',
        'completed': False
    }
    errors = validate_todo_data(data)
    assert 'Title is required' in errors

def test_validate_todo_data_invalid_title():
    """Test validating to-do data with invalid title."""
    data = {
        'title': '',
        'description': 'Test Description',
        'due_date': '2023-12-31',
        'completed': False
    }
    errors = validate_todo_data(data)
    assert 'Title must be a non-empty string' in errors

def test_validate_todo_data_invalid_due_date():
    """Test validating to-do data with invalid due date."""
    data = {
        'title': 'Test Todo',
        'description': 'Test Description',
        'due_date': 'invalid-date',
        'completed': False
    }
    errors = validate_todo_data(data)
    assert 'Due date must be in YYYY-MM-DD format' in errors

def test_validate_todo_data_invalid_completed():
    """Test validating to-do data with invalid completed status."""
    data = {
        'title': 'Test Todo',
        'description': 'Test Description',
        'due_date': '2023-12-31',
        'completed': 'not-a-boolean'
    }
    errors = validate_todo_data(data)
    assert 'Completed must be a boolean' in errors
