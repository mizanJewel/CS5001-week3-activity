# To-Do REST API with Flask

A simple REST API for managing to-do items with date and checkbox functionality.

## Features
- Create, Read, Update, and Delete (CRUD) to-do items
- Each to-do item has a title, description, due date, and completion status
- RESTful API endpoints

## Installation
```bash
pip install -r requirements.txt
```

## Running the API
```bash
python src/main.py
```

## API Endpoints
- `GET /todos`: List all to-do items
- `POST /todos`: Create a new to-do item
- `GET /todos/<id>`: Retrieve a specific to-do item
- `PUT /todos/<id>`: Update a to-do item
- `DELETE /todos/<id>`: Delete a to-do item

## Testing
```bash
pytest tests/
```

## Usage Example
1. Start the API server:
   ```bash
   python src/main.py
   ```
2. Create a new to-do item:
   ```bash
   curl -X POST -H "Content-Type: application/json" -d '{"title":"Buy groceries","description":"Milk, eggs, bread","due_date":"2023-12-31","completed":false}' http://localhost:5000/todos
   ```
3. List all to-do items:
   ```bash
   curl http://localhost:5000/todos
   ```
4. Update a to-do item:
   ```bash
   curl -X PUT -H "Content-Type: application/json" -d '{"title":"Buy groceries","description":"Milk, eggs, bread, butter","due_date":"2023-12-31","completed":true}' http://localhost:5000/todos/1
   ```
5. Delete a to-do item:
   ```bash
   curl -X DELETE http://localhost:5000/todos/1
