from dataclasses import dataclass, field
from typing import List, Dict, Optional
from datetime import datetime

@dataclass
class ToDo:
    """Represents a to-do item with title, description, due date, and completion status."""
    id: Optional[int] = None
    title: str = field(metadata={"required": True})
    description: str = field(default="")
    due_date: str = field(default="")
    completed: bool = field(default=False)

    def to_dict(self) -> Dict:
        """Convert the ToDo object to a dictionary."""
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'due_date': self.due_date,
            'completed': self.completed
        }

    def update(self, **kwargs) -> None:
        """Update the ToDo object with new values."""
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)

class TodoDatabase:
    """In-memory database for storing to-do items."""
    def __init__(self) -> None:
        self.todos: List[ToDo] = []
        self.next_id = 1

    def create(self, todo: ToDo) -> None:
        """Create a new to-do item in the database."""
        todo.id = self.next_id
        self.todos.append(todo)
        self.next_id += 1

    def get_all(self) -> List[Dict]:
        """Get all to-do items from the database."""
        return [todo.to_dict() for todo in self.todos]

    def get_by_id(self, todo_id: int) -> Optional[ToDo]:
        """Get a to-do item by ID."""
        for todo in self.todos:
            if todo.id == todo_id:
                return todo
        return None

    def update(self, todo: ToDo) -> None:
        """Update a to-do item in the database."""
        for i, t in enumerate(self.todos):
            if t.id == todo.id:
                self.todos[i] = todo
                break

    def delete(self, todo_id: int) -> None:
        """Delete a to-do item from the database."""
        self.todos = [todo for todo in self.todos if todo.id != todo_id]
