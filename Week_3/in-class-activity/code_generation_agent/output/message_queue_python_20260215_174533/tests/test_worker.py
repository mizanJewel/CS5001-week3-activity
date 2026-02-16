"""Unit tests for the Worker class."""

import queue
import threading
import time
from unittest.mock import MagicMock, patch
from src.queue import MessageQueue
from src.worker import Worker

def test_worker_processes_messages() -> None:
    """Test that worker processes messages from the queue."""
    q = MessageQueue()
    q.enqueue("test message")

    worker = Worker(q)
    worker.start()

    # Give worker time to process
    time.sleep(0.2)

    worker.stop()
    assert q.is_empty()

def test_worker_stops_on_command() -> None:
    """Test that worker stops when stop() is called."""
    q = MessageQueue()
    worker = Worker(q)
    worker.start()

    # Verify worker is running
    assert worker.is_alive()

    worker.stop()
    assert not worker.is_alive()

def test_worker_handles_empty_queue() -> None:
    """Test that worker handles empty queue gracefully."""
    q = MessageQueue()
    worker = Worker(q)
    worker.start()

    # Worker should not crash with empty queue
    time.sleep(0.2)
    worker.stop()

def test_worker_error_handling() -> None:
    """Test that worker handles processing errors."""
    q = MessageQueue()
    q.enqueue("valid")
    q.enqueue("invalid")  # This will cause an error in processing

    # Mock the processing to raise an error
    with patch.object(Worker, '_process_message', side_effect=Exception("test error")):
        worker = Worker(q)
        worker.start()
        time.sleep(0.2)
        worker.stop()
