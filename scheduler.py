import threading
import queue
import signal
import sys
from logging_provider import logging

class Scheduler:
    def __init__(self):
        self.task_queue = queue.Queue()
        self.completion_status = {}
        self.lock = threading.Lock()
        self.workers = {}
        signal.signal(signal.SIGINT, self.sigterm_handler)

    def submit_task(self, task):
        with self.lock:
            self.task_queue.put(task)
            self.completion_status[task] = False
        logging.info("Task submitted to scheduler: {}".format(task))

    def register_worker(self, worker_id):
        self.workers[worker_id] = []

    def task_completed(self, task_id, worker_id):
        self.workers[worker_id].remove(task_id)

    def assign_task(self):
        with self.lock:
            if not self.task_queue.empty():
                return self.task_queue.get()
            else:
                return None

    def get_task_completion(self, task):
        pass

    def handle_worker(self, client_socket):
        while True:
            task = self.assign_task()
            if task:
                client_socket.send(task.encode())
                self.get_task_completion(task)

    def sigterm_handler(self, signum, frame):
        print("Exiting gracefully.")
        sys.exit(0)
