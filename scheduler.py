import threading
import queue
import signal
import sys
import random
from Data.task import Task
from Data.future import Future
from worker_client import WorkerClient
from logging_provider import logging

class Scheduler:
    def __init__(self):
        self.task_queue = queue.Queue()
        self.completion_status = {}
        self.lock = threading.Lock()
        self.workers = []
        signal.signal(signal.SIGINT, self.sigterm_handler)

    def submit_task(self, task : Task) -> Future:
        random_worker = random.choice(self.workers)
        worker_client = WorkerClient(random_worker.split(":")[0], int(random_worker.split(":")[1]))
        logging.info(f"Task {task} submitted to worker:{random_worker}")
        return worker_client.SubmitTask(task)

    def register_worker(self, worker_id):
        self.workers.append(worker_id)
        logging.info(f"Worker {worker_id} registered")

    def task_completed(self, task_id, worker_id):
        pass

    def assign_task(self):
        with self.lock:
            if not self.task_queue.empty():
                return self.task_queue.get()
            else:
                return None

    def get_task_completion(self, task):
        pass

    def sigterm_handler(self, signum, frame):
        logging.info("Exiting gracefully.")
        sys.exit(0)
