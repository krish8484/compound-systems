import signal
import sys
import uuid
from scheduler_client import SchedulerClient
from Data.future import Future
from Data.task import Task
from logging_provider import logging

class Worker:
    def __init__(self, scheduler_host, scheduler_port, worker_host, worker_port):
        self.scheduler_host = scheduler_host
        self.scheduler_port = scheduler_port
        self.worker_host = worker_host
        self.worker_port = worker_port
        self.scheduler_client = SchedulerClient(self.scheduler_host, self.scheduler_port)
        self.worker_id = "{}:{}".format(worker_host, worker_port)
        self.scheduler_client.RegisterWorker(self.worker_id)

        # Datastore for storing task result in memory. CREATED FOR TESTING FLOW -> NEED TO CHANGE TO FILE BASED SYSTEM LATER (Swarnim's PR)
        self.dummyFileStore = {}
        signal.signal(signal.SIGINT, self.sigterm_handler)


    def execute_task(self, task: Task) -> Future:
        logging.info(f"executing task {task}")
        resultLocation = str(uuid.uuid4()) #UniqueID
        self.dummyFileStore[resultLocation] = "TASKDONE".encode()
        return Future(result_location=resultLocation, host_name=self.worker_host, port=self.worker_port)
    
    def get_result(self, future: Future) -> bytes:
        return self.dummyFileStore[future.result_location]

    def notify_task_completion(self, task):
        pass

    def sigterm_handler(self, signum, frame):
        logging.info("Exiting gracefully.")
        sys.exit(0)
