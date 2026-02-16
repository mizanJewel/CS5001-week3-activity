from flask import Flask, request, jsonify
from models import ToDo, TodoDatabase
from utils import validate_todo_data
from typing import Dict, List, Optional

app = Flask(__name__)
db = TodoDatabase()

@app.route('/todos', methods=['GET'])
def get_todos() -> Dict[str, List[Dict]]:
    """Get all to-do items."""
    try:
        todos = db.get_all()
        return jsonify({'todos': todos})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/todos', methods=['POST'])
def create_todo() -> Dict[str, Dict]:
    """Create a new to-do item."""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400

        errors = validate_todo_data(data)
        if errors:
            return jsonify({'errors': errors}), 400

        todo = ToDo(**data)
        db.create(todo)
        return jsonify({'todo': todo.to_dict()}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/todos/<int:todo_id>', methods=['GET'])
def get_todo(todo_id: int) -> Dict[str, Optional[Dict]]:
    """Get a specific to-do item by ID."""
    try:
        todo = db.get_by_id(todo_id)
        if not todo:
            return jsonify({'error': 'To-do item not found'}), 404
        return jsonify({'todo': todo.to_dict()})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/todos/<int:todo_id>', methods=['PUT'])
def update_todo(todo_id: int) -> Dict[str, Optional[Dict]]:
    """Update a specific to-do item by ID."""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400

        errors = validate_todo_data(data)
        if errors:
            return jsonify({'errors': errors}), 400

        todo = db.get_by_id(todo_id)
        if not todo:
            return jsonify({'error': 'To-do item not found'}), 404

        todo.update(**data)
        db.update(todo)
        return jsonify({'todo': todo.to_dict()})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/todos/<int:todo_id>', methods=['DELETE'])
def delete_todo(todo_id: int) -> Dict[str, Optional[Dict]]:
    """Delete a specific to-do item by ID."""
    try:
        todo = db.get_by_id(todo_id)
        if not todo:
            return jsonify({'error': 'To-do item not found'}), 404

        db.delete(todo_id)
        return jsonify({'message': 'To-do item deleted successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
