import threading
import queue
import signal
import sys
import random
from Data.task import Task
from Data.future import Future
from Data.WorkerInfo import WorkerInfo
from Data.WorkerInfoWrapper import WorkerInfoWrapper
from worker_client import WorkerClient
from logging_provider import logging
from exceptions import NoWorkerAvailableError
import grpc
import constants

class Scheduler:
    def __init__(self, scheduler_mode):
        self.task_queue = queue.Queue()
        self.completion_status = {}
        self.workerIdLock = threading.Lock()
        self.workerMapLock = threading.Lock()
        self.workers = {} # Map that maintains the worker id to hostName,portNum - Only used when scheduling mode is Random
        self.workerQueue = queue.Queue() # Thread Safe Queue - Only used when scheduling mode is round robin
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

        if self.schedulerMode == constants.SCHEDULINGMODE_RANDOM:
            with self.workerMapLock:
                self.workers[assignedWorkerId] = workerInfo
        elif self.schedulerMode == constants.SCHEDULINGMODE_ROUNDROBIN:
            workerInfoWithWorkerId = WorkerInfoWrapper(workerInfo, assignedWorkerId)
            self.workerQueue.put(workerInfoWithWorkerId)

        logging.info(f"Worker {assignedWorkerId} registered. WorkerInfo: {workerInfo}")   
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
        if self.schedulerMode == constants.SCHEDULINGMODE_RANDOM:
            logging.info(f"Getting worker for {self.schedulerMode}")
            if self.globalIncrementalWorkerId > 1:
                random_worker_id = random.randint(0, self.globalIncrementalWorkerId - 1)
                with self.workerMapLock:
                    return self.workers[random_worker_id]
            else:
                logging.info(f"No worker found.")
                raise NoWorkerAvailableError(self.schedulerMode)
        elif self.schedulerMode == constants.SCHEDULINGMODE_ROUNDROBIN:
            logging.info(f"Getting worker for {self.schedulerMode}")
            if self.workerQueue.qsize() > 0:
                # dequeue and enqueue again and return the wrapped worker info object
                wrappedWorkerInfo = self.workerQueue.get()
                self.workerQueue.put(wrappedWorkerInfo)
                return wrappedWorkerInfo
            else:
                logging.info(f"No worker found.")
                raise NoWorkerAvailableError(self.schedulerMode)
        
            
            