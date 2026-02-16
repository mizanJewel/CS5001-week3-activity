# Message Queue in Python

A simple message queue implementation in Python using standard library components.

## Overview
This project provides a basic message queue system with producer-consumer functionality. It uses Python's built-in `queue.Queue` for thread-safe operations and demonstrates how to process messages concurrently.

## Setup
1. Clone the repository
2. Install dependencies (though none are required beyond Python standard library):
   ```bash
   pip install -r requirements.txt
   ```

## Run
To run the demo:
```bash
python demo/demo.py
```

## Test
Run the test suite with pytest:
```bash
pytest tests/
```

## Usage Example
```python
from src.queue import MessageQueue
from src.worker import Worker

# Create a queue and worker
queue = MessageQueue()
worker = Worker(queue)

# Start the worker in a separate thread
worker.start()

# Enqueue a message
queue.enqueue("Hello, World!")

# Wait for processing
worker.stop()
```

## Features
- Thread-safe message queue
- Worker thread for message processing
- Unit and integration tests
- Demo script showing usage

## Project Structure
```
.
├── README.md
├── .gitignore
├── requirements.txt
├── src/
│   ├── main.py
│   ├── queue.py
│   └── worker.py
└── tests/
    ├── test_queue.py
    └── test_worker.py
└── demo/
    └── demo.py
```

## Dependencies
- Python standard library (queue, threading, time, logging)
- No third-party dependencies

## Quality
- Formatted with Black
- Linted with Ruff
- Type hints included where helpful
- Comprehensive docstrings
