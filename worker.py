import time
import signal
import sys
import uuid
from scheduler_client import SchedulerClient
from Data.future import Future
from Data.task import Task
from logging_provider import logging
import multiprocessing
import threading
import grpc

class Worker:
    def __init__(self, scheduler_host, scheduler_port, worker_host, worker_port):
        self.scheduler_host = scheduler_host
        self.scheduler_port = scheduler_port
        self.worker_host = worker_host
        self.worker_port = worker_port
        self.scheduler_client = SchedulerClient(self.scheduler_host, self.scheduler_port)

        try:
            self.worker_id = self.scheduler_client.RegisterWorker(self.worker_host, self.worker_port)
            logging.info(f"Registered worker - WorkerId assigned from scheduler is {self.worker_id}")
        except grpc.RpcError as rpc_error:
            if rpc_error.code() == grpc.StatusCode.CANCELLED:
                logging.error(f"RegisterWorker: RPC Cancelled. RPC Error: code={rpc_error.code()} message={rpc_error.details()}")
            elif rpc_error.code() == grpc.StatusCode.UNAVAILABLE:
                logging.error(f"RegisterWorker: Scheduler Unavailable. RPC Error: code={rpc_error.code()} message={rpc_error.details()}")
            else:
                logging.error(f"RegisterWorker: Unhandled RPC error: code={rpc_error.code()} message={rpc_error.details()}")

        # Datastore for storing task result in memory. CREATED FOR TESTING FLOW -> NEED TO CHANGE TO FILE BASED SYSTEM LATER (Swarnim's PR)
        self.dummyFileStore = {}
        signal.signal(signal.SIGINT, self.sigterm_handler)

    def submit_task(self, task: Task) -> Future:
        resultLocation = str(uuid.uuid4())
        self.dummyFileStore[resultLocation] = f"TASK {task.taskId} NOT COMPLETED".encode()
        future = Future(resultLocation=resultLocation, hostName=self.worker_host, port=self.worker_port)
        threading.Thread(target=self.execute_task, args=(task, future)).start()
        logging.info(f"submitted task {task} to worker {self.worker_id}")
        return future

    def execute_task(self, task: Task, future: Future):
        logging.info(f"executing task {task}")
        time.sleep(5)
        self.dummyFileStore[future.resultLocation] = f"TASK {task.taskId} DONE".encode()
    
    def get_result(self, future: Future) -> bytes:
        return self.dummyFileStore[future.resultLocation]

    def notify_task_completion(self, task):
        pass

    def sigterm_handler(self, signum, frame):
        logging.info("Exiting gracefully.")
        sys.exit(0)
