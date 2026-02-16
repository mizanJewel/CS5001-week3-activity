"""Message queue implementation using Python's standard library."""

import queue
from typing import Any

class MessageQueue:
    """Thread-safe message queue implementation."""

    def __init__(self) -> None:
        """Initialize the message queue."""
        self._queue = queue.Queue()

    def enqueue(self, message: Any) -> None:
        """Add a message to the queue.

        Args:
            message: The message to enqueue (any type)
        """
        self._queue.put(message)

    def dequeue(self) -> Any:
        """Remove and return a message from the queue.

        Returns:
            The next message in the queue

        Raises:
            queue.Empty: If the queue is empty
        """
        return self._queue.get()

    def size(self) -> int:
        """Get the current size of the queue.

        Returns:
            int: Number of messages in the queue
        """
        return self._queue.qsize()

    def is_empty(self) -> bool:
        """Check if the queue is empty.

        Returns:
            bool: True if queue is empty, False otherwise
        """
        return self.size() == 0
