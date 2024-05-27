import threading
import queue
import signal
import sys
import random
from Data.task import Task
from Data.future import Future
from Data.WorkerInfo import WorkerInfo
from worker_client import WorkerClient
from logging_provider import logging
import grpc

class Scheduler:
    def __init__(self, scheduler_mode):
        self.task_queue = queue.Queue()
        self.completion_status = {}
        self.workerConnectInfoLock = threading.Lock()
        self.workerIdLock = threading.Lock()
        self.workers = {} # Map that maintains the worker id to hostName,portNum
        self.workerQueue = [] # Queue for round robin scheduling
        self.workerQueueLock = threading.Lock()
        self.globalIncrementalWorkerId = 0; # A globally incrementing worker id maintained by the scheduler
        self.schedulerMode = scheduler_mode
        signal.signal(signal.SIGINT, self.sigterm_handler)

    def submit_task(self, task : Task) -> Future:
        random_worker = self.get_worker()
        worker_client = WorkerClient(random_worker.hostName , int(random_worker.portNumber))
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

    def register_worker(self, workerInfo):
        print("In register worker at scheduler")
        assignedWorkerId = 0

        with self.workerIdLock:
            assignedWorkerId = self.globalIncrementalWorkerId
            self.globalIncrementalWorkerId +=1

        with self.workerConnectInfoLock:
            self.workers[assignedWorkerId] = workerInfo

        logging.info(f"Worker {assignedWorkerId} registered. WorkerInfo: {workerInfo}")

        self.workerQueue.append(assignedWorkerId) #lock free addition
        return assignedWorkerId


    def task_completed(self, task_id, worker_id, status):
        logging.info(f"Scheduler recevied message of completion {task_id} from {worker_id} - Success {status}")
        return True

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

    def get_worker(self):
        if self.schedulerMode == 'Random':
            if self.globalIncrementalWorkerId > 1:
                random_worker_id = random.randint(0, self.globalIncrementalWorkerId - 1)
            else:
                random_worker_id = 0

            return self.workers[random_worker_id]
        
        elif self.schedulerMode == 'RoundRobin':
            if len(self.workerQueue) > 0:
                with self.workerQueueLock:
                    assignedWorkerId = self.workerQueue.pop(0)
            else:
                logging.info(f"No worker found.")
                return None
        
            worker =  self.workers[assignedWorkerId]
            self.workerQueue.append(assignedWorkerId) # Assign the worker id back into queue at the end
            return worker