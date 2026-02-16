import pytest
from src.models import ToDo, TodoDatabase

def test_todo_creation():
    """Test creating a ToDo object."""
    todo = ToDo(title='Test Todo', description='Test Description', due_date='2023-12-31', completed=False)
    assert todo.title == 'Test Todo'
    assert todo.description == 'Test Description'
    assert todo.due_date == '2023-12-31'
    assert todo.completed is False

def test_todo_to_dict():
    """Test converting a ToDo object to a dictionary."""
    todo = ToDo(id=1, title='Test Todo', description='Test Description', due_date='2023-12-31', completed=False)
    todo_dict = todo.to_dict()
    assert todo_dict == {
        'id': 1,
        'title': 'Test Todo',
        'description': 'Test Description',
        'due_date': '2023-12-31',
        'completed': False
    }

def test_todo_update():
    """Test updating a ToDo object."""
    todo = ToDo(title='Test Todo', description='Test Description', due_date='2023-12-31', completed=False)
    todo.update(title='Updated Todo', description='Updated Description', completed=True)
    assert todo.title == 'Updated Todo'
    assert todo.description == 'Updated Description'
    assert todo.completed is True

def test_todo_database_create():
    """Test creating a to-do item in the database."""
    db = TodoDatabase()
    todo = ToDo(title='Test Todo', description='Test Description', due_date='2023-12-31', completed=False)
    db.create(todo)
    assert len(db.todos) == 1
    assert db.todos[0].id == 1

def test_todo_database_get_all():
    """Test getting all to-do items from the database."""
    db = TodoDatabase()
    todo1 = ToDo(title='Test Todo 1', description='Test Description 1', due_date='2023-12-31', completed=False)
    todo2 = ToDo(title='Test Todo 2', description='Test Description 2', due_date='2023-12-31', completed=False)
    db.create(todo1)
    db.create(todo2)
    todos = db.get_all()
    assert len(todos) == 2
    assert todos[0]['title'] == 'Test Todo 1'
    assert todos[1]['title'] == 'Test Todo 2'

def test_todo_database_get_by_id():
    """Test getting a to-do item by ID."""
    db = TodoDatabase()
    todo1 = ToDo(title='Test Todo 1', description='Test Description 1', due_date='2023-12-31', completed=False)
    todo2 = ToDo(title='Test Todo 2', description='Test Description 2', due_date='2023-12-31', completed=False)
    db.create(todo1)
    db.create(todo2)
    retrieved_todo = db.get_by_id(1)
    assert retrieved_todo.title == 'Test Todo 1'

def test_todo_database_update():
    """Test updating a to-do item in the database."""
    db = TodoDatabase()
    todo = ToDo(title='Test Todo', description='Test Description', due_date='2023-12-31', completed=False)
    db.create(todo)
    todo.title = 'Updated Todo'
    db.update(todo)
    retrieved_todo = db.get_by_id(1)
    assert retrieved_todo.title == 'Updated Todo'

def test_todo_database_delete():
    """Test deleting a to-do item from the database."""
    db = TodoDatabase()
    todo1 = ToDo(title='Test Todo 1', description='Test Description 1', due_date='2023-12-31', completed=False)
    todo2 = ToDo(title='Test Todo 2', description='Test Description 2', due_date='2023-12-31', completed=False)
    db.create(todo1)
    db.create(todo2)
    db.delete(1)
    todos = db.get_all()
    assert len(todos) == 1
    assert todos[0]['title'] == 'Test Todo 2'
