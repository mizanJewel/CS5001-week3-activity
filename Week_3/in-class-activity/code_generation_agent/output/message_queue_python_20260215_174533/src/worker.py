"""Worker thread implementation for processing messages from the queue."""

import logging
import threading
import time
from src.queue import MessageQueue

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Worker(threading.Thread):
    """Worker thread that processes messages from a queue."""

    def __init__(self, queue: MessageQueue) -> None:
        """Initialize the worker with a message queue.

        Args:
            queue: MessageQueue instance to process messages from
        """
        super().__init__()
        self.queue = queue
        self._stop_event = threading.Event()

    def run(self) -> None:
        """Main worker loop that processes messages until stopped."""
        while not self._stop_event.is_set():
            try:
                message = self.queue.dequeue()
                self._process_message(message)
            except queue.Empty:
                # Queue is empty, wait briefly before checking again
                time.sleep(0.1)
            except Exception as e:
                logger.error(f"Error processing message: {e}")

    def _process_message(self, message: Any) -> None:
        """Process a single message.

        Args:
            message: The message to process
        """
        logger.info(f"Processing message: {message}")
        # Simulate work
        time.sleep(0.5)
        logger.info(f"Finished processing: {message}")

    def stop(self) -> None:
        """Signal the worker to stop processing messages."""
        self._stop_event.set()
        self.join()
