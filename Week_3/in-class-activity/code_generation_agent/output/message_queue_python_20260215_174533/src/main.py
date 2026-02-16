"""Main module for the message queue system."""

from src.queue import MessageQueue
from src.worker import Worker

def create_queue_system() -> tuple[MessageQueue, Worker]:
    """Create and return a queue system with queue and worker.

    Returns:
        tuple: (MessageQueue, Worker) instance
    """
    queue = MessageQueue()
    worker = Worker(queue)
    return queue, worker

def main() -> None:
    """Main entry point for the message queue system."""
    queue, worker = create_queue_system()
    worker.start()

    # Example usage
    queue.enqueue("Test message 1")
    queue.enqueue("Test message 2")

    # Wait for messages to be processed
    import time
    time.sleep(2)
    worker.stop()

if __name__ == "__main__":
    main()
