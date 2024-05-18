import threading
import queue
import signal
import sys
import random
from Data.task import Task
from Data.future import Future
from worker_client import WorkerClient
from logging_provider import logging
import grpc

class Scheduler:
    def __init__(self):
        self.task_queue = queue.Queue()
        self.completion_status = {}
        self.workerConnectInfoLock = threading.Lock()
        self.workerIdLock = threading.Lock()
        self.workers = {} # Map that maintains the worker id to hostName,portNum 
        self.globalIncrementalWorkerId = 0; # A globally incrementing worker id maintained by the scheduler
        signal.signal(signal.SIGINT, self.sigterm_handler)

    def submit_task(self, task : Task) -> Future:
        random_worker = random.choice(self.workers)
        worker_client = WorkerClient(random_worker.split(",")[0], int(random_worker.split(",")[1]))
        logging.info(f"Task {task} submitted to worker:{random_worker}")

        try:
            return worker_client.SubmitTask(task)
        except grpc.RpcError as rpc_error:
            if rpc_error.code() == grpc.StatusCode.CANCELLED:
                logging.error(f"SubmitTask: RPC Cancelled. RPC Error: code={rpc_error.code()} message={rpc_error.details()}")
            elif rpc_error.code() == grpc.StatusCode.UNAVAILABLE:
                logging.error(f"SubmitTask: Worker Unavailable. RPC Error: code={rpc_error.code()} message={rpc_error.details()}")
            else:
                logging.error(f"SubmitTask: Unhandled RPC error: code={rpc_error.code()} message={rpc_error.details()}")

    def register_worker(self, host_name, port_number):
        assignedWorkerId = 0;
        
        with self.workerIdLock:
            assignedWorkerId = self.globalIncrementalWorkerId
            self.globalIncrementalWorkerId +=1

        workerConnectInfo = host_name + ',' + str(port_number)
        
        with self.workerConnectInfoLock:
            self.workers[assignedWorkerId] = workerConnectInfo
        
        logging.info(f"Worker {assignedWorkerId} registered. ConnectionInfo: {workerConnectInfo}")

        return assignedWorkerId


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
