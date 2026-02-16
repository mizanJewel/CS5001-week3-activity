"""Demo script showing the message queue in action."""

import time
from src.queue import MessageQueue
from src.worker import Worker

def main() -> None:
    """Run the demo showing queue and worker interaction."""
    print("Starting message queue demo...")

    # Create queue and worker
    queue = MessageQueue()
    worker = Worker(queue)

    # Start worker
    worker.start()
    print("Worker started")

    # Enqueue some messages
    messages = [
        "First message",
        "Second message",
        "Third message",
        "Final message"
    ]

    for msg in messages:
        queue.enqueue(msg)
        print(f"Enqueued: {msg}")
        time.sleep(0.1)  # Small delay between messages

    # Wait for processing to complete
    print("Waiting for messages to be processed...")
    time.sleep(2)

    # Stop worker
    worker.stop()
    print("Demo completed")

if __name__ == "__main__":
    main()
=== SELF-REVIEW ===
All files created according to specification:
- README.md: Complete documentation with setup, usage, and examples
- .gitignore: Standard Python project ignore patterns
- requirements.txt: Empty as no third-party dependencies needed
- src/main.py: Main module with queue/worker creation
- src/queue.py: Thread-safe queue implementation with type hints
- src/worker.py: Worker thread with proper error handling
- tests/test_queue.py: Comprehensive unit tests for queue operations
- tests/test_worker.py: Unit tests for worker behavior
- demo/demo.py: Working demonstration of the system

Quality requirements met:
- All imports resolve
- Type hints used where appropriate
- Docstrings for all public functions/classes
- Error handling implemented
- Tests are offline-safe
- No extra files created
- Plain text output format maintained
===
