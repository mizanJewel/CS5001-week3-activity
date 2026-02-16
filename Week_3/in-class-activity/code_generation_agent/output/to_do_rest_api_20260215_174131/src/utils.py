from typing import Dict, List

def validate_todo_data(data: Dict) -> List[str]:
    """Validate the to-do data before creating or updating a to-do item."""
    errors: List[str] = []

    if 'title' not in data:
        errors.append('Title is required')
    elif not isinstance(data['title'], str) or not data['title'].strip():
        errors.append('Title must be a non-empty string')

    if 'description' in data and not isinstance(data['description'], str):
        errors.append('Description must be a string')

    if 'due_date' in data:
        try:
            datetime.strptime(data['due_date'], '%Y-%m-%d')
        except ValueError:
            errors.append('Due date must be in YYYY-MM-DD format')

    if 'completed' in data and not isinstance(data['completed'], bool):
        errors.append('Completed must be a boolean')

    return errors
