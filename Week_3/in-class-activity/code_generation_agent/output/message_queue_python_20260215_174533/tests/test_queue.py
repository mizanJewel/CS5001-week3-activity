"""Unit tests for the MessageQueue class."""

import pytest
from src.queue import MessageQueue

def test_enqueue_and_dequeue() -> None:
    """Test basic enqueue and dequeue operations."""
    q = MessageQueue()
    q.enqueue("test message")
    assert q.dequeue() == "test message"

def test_queue_size() -> None:
    """Test queue size tracking."""
    q = MessageQueue()
    assert q.size() == 0
    q.enqueue("msg1")
    q.enqueue("msg2")
    assert q.size() == 2
    q.dequeue()
    assert q.size() == 1

def test_is_empty() -> None:
    """Test empty queue detection."""
    q = MessageQueue()
    assert q.is_empty()
    q.enqueue("msg")
    assert not q.is_empty()
    q.dequeue()
    assert q.is_empty()

def test_dequeue_empty_raises() -> None:
    """Test that dequeue raises when queue is empty."""
    q = MessageQueue()
    with pytest.raises(queue.Empty):
        q.dequeue()
