README.md
```
# Message Queue in Python

A lightweight, test-driven message queue implementation in Python with support for producers, consumers, and message persistence.

## Overview
This project implements a simple message queue system with core components:
- `MessageQueue`: FIFO queue with optional persistence
- `Producer`: Sends messages to the queue
- `Consumer`: Receives and processes messages

## Setup
1. Clone the repository
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

## Run
```
python src/main.py
```

## Test
Run unit and integration tests:
```
pytest tests/
```

## Usage Example
```python
from src.message_queue import MessageQueue
from src.producer import Producer
from src.consumer import Consumer

queue = MessageQueue(persistence=True)
producer = Producer(queue)
consumer = Consumer(queue)

producer.send_message("Hello, Queue!")
message = consumer.receive_message()
print(message)  # Output: "Hello, Queue!"
```

## Features
- Thread-safe operations
- Optional message persistence
- Simple producer/consumer interface
- Comprehensive test coverage

---

```
.gitignore
```
# Python project gitignore
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# Environment
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/

# IDE
.idea/
.vscode/
*.swp
*.swo

# Logs
*.log
*.log.*

# Test cache
.pytest_cache/
.hypothesis/
```

---

```
requirements.txt
```
pytest>=7.0.0
pytest-mock>=3.0.0
pika>=1.3.0
```

---

```
src/main.py
```
"""
Main entry point for the message queue system.
Demonstrates basic usage of Producer, Consumer, and MessageQueue.
"""

from message_queue import MessageQueue
from producer import Producer
from consumer import Consumer

def main():
    """Demonstrate message queue usage."""
    queue = MessageQueue(persistence=True)
    producer = Producer(queue)
    consumer = Consumer(queue)

    # Send and receive a message
    producer.send_message("Hello, Queue!")
    message = consumer.receive_message()
    print(f"Received: {message}")

if __name__ == "__main__":
    main()
```

---

```
src/message_queue.py
```
"""
Core message queue implementation with FIFO behavior and optional persistence.
"""

import threading
import json
import os
from typing import Optional, List, Any

class MessageQueue:
    """
    A thread-safe message queue with optional persistence.

    Attributes:
        persistence (bool): If True, messages are saved to disk.
        queue (List[Any]): In-memory message storage.
        lock (threading.Lock): Thread synchronization.
        storage_file (str): Path to persistence file.
    """

    def __init__(self, persistence: bool = False, storage_file: str = "queue_storage.json"):
        """
        Initialize the message queue.

        Args:
            persistence: Enable disk persistence.
            storage_file: Path to persistence file.
        """
        self.persistence = persistence
        self.queue: List[Any] = []
        self.lock = threading.Lock()
        self.storage_file = storage_file

        if self.persistence:
            self._load_from_disk()

    def enqueue(self, message: Any) -> None:
        """
        Add a message to the queue.

        Args:
            message: Message to enqueue.
        """
        with self.lock:
            self.queue.append(message)
            if self.persistence:
                self._save_to_disk()

    def dequeue(self) -> Optional[Any]:
        """
        Remove and return the oldest message from the queue.

        Returns:
            The oldest message, or None if queue is empty.
        """
        with self.lock:
            if not self.queue:
                return None
            message = self.queue.pop(0)
            if self.persistence:
                self._save_to_disk()
            return message

    def size(self) -> int:
        """Return the number of messages in the queue."""
        with self.lock:
            return len(self.queue)

    def _save_to_disk(self) -> None:
        """Persist the queue to disk."""
        try:
            with open(self.storage_file, "w") as f:
                json.dump(self.queue, f)
        except IOError as e:
            raise RuntimeError(f"Failed to save queue: {e}") from e

    def _load_from_disk(self) -> None:
        """Load the queue from disk."""
        try:
            if os.path.exists(self.storage_file):
                with open(self.storage_file, "r") as f:
                    self.queue = json.load(f)
        except (IOError, json.JSONDecodeError) as e:
            raise RuntimeError(f"Failed to load queue: {e}") from e
```

---

```
src/producer.py
```
"""
Message producer for the message queue system.
"""

from typing import Any
from message_queue import MessageQueue

class Producer:
    """
    Sends messages to a MessageQueue.

    Attributes:
        queue (MessageQueue): Target queue for messages.
    """

    def __init__(self, queue: MessageQueue):
        """
        Initialize the producer.

        Args:
            queue: MessageQueue instance to send messages to.
        """
        self.queue = queue

    def send_message(self, message: Any) -> None:
        """
        Enqueue a message into the target queue.

        Args:
            message: Message to send.
        """
        self.queue.enqueue(message)
```

---

```
src/consumer.py
```
"""
Message consumer for the message queue system.
"""

from typing import Optional, Any
from message_queue import MessageQueue

class Consumer:
    """
    Receives messages from a MessageQueue.

    Attributes:
        queue (MessageQueue): Source queue for messages.
    """

    def __init__(self, queue: MessageQueue):
        """
        Initialize the consumer.

        Args:
            queue: MessageQueue instance to receive messages from.
        """
        self.queue = queue

    def receive_message(self) -> Optional[Any]:
        """
        Dequeue and return the oldest message from the queue.

        Returns:
            The oldest message, or None if queue is empty.
        """
        return self.queue.dequeue()
```

---

```
tests/test_message_queue.py
```
"""
Unit tests for MessageQueue class.
"""

import pytest
import os
from src.message_queue import MessageQueue

@pytest.fixture
def temp_queue_file(tmp_path):
    """Fixture for a temporary queue storage file."""
    return tmp_path / "test_queue.json"

def test_enqueue_dequeue():
    """Test basic enqueue and dequeue operations."""
    queue = MessageQueue()
    queue.enqueue("msg1")
    queue.enqueue("msg2")

    assert queue.dequeue() == "msg1"
    assert queue.dequeue() == "msg2"
    assert queue.dequeue() is None

def test_size():
    """Test queue size tracking."""
    queue = MessageQueue()
    assert queue.size() == 0

    queue.enqueue("msg")
    assert queue.size() == 1

    queue.dequeue()
    assert queue.size() == 0

def test_persistence(temp_queue_file):
    """Test message persistence to disk."""
    queue = MessageQueue(persistence=True, storage_file=str(temp_queue_file))

    queue.enqueue("persistent_msg")
    assert queue.size() == 1

    # Simulate restart by creating a new queue instance
    new_queue = MessageQueue(persistence=True, storage_file=str(temp_queue_file))
    assert new_queue.size() == 1
    assert new_queue.dequeue() == "persistent_msg"

def test_thread_safety():
    """Test thread-safe operations."""
    queue = MessageQueue()
    messages = ["msg1", "msg2", "msg3"]

    def worker(msg):
        queue.enqueue(msg)

    import threading
    threads = [threading.Thread(target=worker, args=(msg,)) for msg in messages]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    assert queue.size() == 3
    assert queue.dequeue() in messages
```

---

```
tests/test_producer.py
```
"""
Unit tests for Producer class.
"""

import pytest
from unittest.mock import Mock
from src.producer import Producer
from src.message_queue import MessageQueue

def test_send_message():
    """Test message sending via Producer."""
    mock_queue = Mock(spec=MessageQueue)
    producer = Producer(mock_queue)

    producer.send_message("test_message")
    mock_queue.enqueue.assert_called_once_with("test_message")

def test_send_various_types():
    """Test sending different message types."""
    mock_queue = Mock(spec=MessageQueue)
    producer = Producer(mock_queue)

    test_messages = [123, "string", {"key": "value"}, None]
    for msg in test_messages:
        producer.send_message(msg)
        mock_queue.enqueue.assert_called_with(msg)
```

---

```
tests/test_consumer.py
```
"""
Unit tests for Consumer class.
"""

import pytest
from unittest.mock import Mock
from src.consumer import Consumer
from src.message_queue import MessageQueue

def test_receive_message():
    """Test message receiving via Consumer."""
    mock_queue = Mock(spec=MessageQueue)
    mock_queue.dequeue.return_value = "test_message"
    consumer = Consumer(mock_queue)

    assert consumer.receive_message() == "test_message"
    mock_queue.dequeue.assert_called_once()

def test_receive_empty():
    """Test receiving from empty queue."""
    mock_queue = Mock(spec=MessageQueue)
    mock_queue.dequeue.return_value = None
    consumer = Consumer(mock_queue)

    assert consumer.receive_message() is None
```

---

```
tests/integration/test_queue_integration.py
```
"""
Integration tests for the complete message queue system.
"""

import pytest
from src.message_queue import MessageQueue
from src.producer import Producer
from src.consumer import Consumer

def test_end_to_end_flow():
    """Test complete message flow: Producer -> Queue -> Consumer."""
    queue = MessageQueue()
    producer = Producer(queue)
    consumer = Consumer(queue)

    # Send and receive a message
    producer.send_message("integration_test")
    assert consumer.receive_message() == "integration_test"

def test_multiple_producers_consumers():
    """Test multiple producers and consumers."""
    queue = MessageQueue()
    producers = [Producer(queue) for _ in range(3)]
    consumers = [Consumer(queue) for _ in range(2)]

    # Send messages from multiple producers
    for i, p in enumerate(producers):
        p.send_message(f"msg_{i}")

    # Consume all messages
    received = []
    for c in consumers:
        while True:
            msg = c.receive_message()
            if msg is None:
                break
            received.append(msg)

    assert len(received) == 3
    assert set(received) == {"msg_0", "msg_1", "msg_2"}

def test_persistence_integration(tmp_path):
    """Test persistence in an end-to-end scenario."""
    storage_file = tmp_path / "integration_storage.json"
    queue = MessageQueue(persistence=True, storage_file=str(storage_file))
    producer = Producer(queue)
    consumer = Consumer(queue)

    # First session
    producer.send_message("persistent_integration")
    assert consumer.receive_message() == "persistent_integration"

    # Second session (simulate restart)
    new_queue = MessageQueue(persistence=True, storage_file=str(storage_file))
    new_consumer = Consumer(new_queue)
    assert new_consumer.receive_message() is None  # Queue should be empty after dequeue
```

---

```
=== SELF-REVIEW ===
Generated all required files as specified in the YAML plan:
- README.md: Complete documentation with setup, usage, and examples
- .gitignore: Standard Python project exclusions
- requirements.txt: Minimal dependencies (pytest, pytest-mock, pika)
- src/main.py: Demonstration entry point
- src/message_queue.py: Core queue implementation with persistence
- src/producer.py: Message sender
- src/consumer.py: Message receiver
- tests/test_message_queue.py: Unit tests for queue operations
- tests/test_producer.py: Unit tests for producer
- tests/test_consumer.py: Unit tests for consumer
- tests/integration/test_queue_integration.py: End-to-end tests

All files follow the specified structure:
- Type hints where applicable
- Docstrings for public classes/functions
- Clear error handling
- Offline-safe tests (no external dependencies in tests)
- Minimal but comprehensive test coverage
- Thread-safe implementation in MessageQueue
- Optional persistence with JSON storage
