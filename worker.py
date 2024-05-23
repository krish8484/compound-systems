import time
import signal
import sys
import uuid
from scheduler_client import SchedulerClient
from Data.future import Future
from Data.task import Task
from Data.WorkerInfo import WorkerInfo
from logging_provider import logging
import multiprocessing
import threading
from random import randrange
import grpc
import numpy as np
import json

class Worker:
    def __init__(
            self,
            scheduler_host,
            scheduler_port,
            worker_host,
            worker_port,
            add_delay,
            max_workers_count,
            gpu_enabled):
        self.scheduler_host = scheduler_host
        self.scheduler_port = scheduler_port
        self.worker_host = worker_host
        self.worker_port = worker_port
        self.scheduler_client = SchedulerClient(self.scheduler_host, self.scheduler_port)
        self.add_delay = add_delay
        self.max_workers_count = max_workers_count
        self.gpu_enabled = gpu_enabled

        self.add_random_delay()
        workerInfo = WorkerInfo(
            self.worker_host,
            self.worker_port,
            self.max_workers_count,
            self.gpu_enabled)
        
        try:
            self.worker_id = self.scheduler_client.RegisterWorker(workerInfo)
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
        self.operations = {
            "dot_product": self.dot_product,
            "mat_add": self.mat_add,
            "mat_subtract": self.mat_subtract,
            # Add more functions as needed
        }
        signal.signal(signal.SIGINT, self.sigterm_handler)

    def submit_task(self, task: Task) -> Future:
        self.add_random_delay()
        resultLocation = str(uuid.uuid4())
        self.dummyFileStore[resultLocation] = f"TASK {task.taskId} NOT COMPLETED".encode()
        future = Future(resultLocation=resultLocation, hostName=self.worker_host, port=self.worker_port)
        threading.Thread(target=self.execute_task, args=(task, future)).start()
        logging.info(f"submitted task {task} to worker {self.worker_id}")
        return future

    def execute_task(self, task: Task, future: Future):
        logging.info(f"executing task {task}")

        self.add_random_delay()
        arguments = task.taskData[0:].decode('utf-8').strip()
        function_name = task.taskDefintion

        if function_name in self.operations:
            arguments = self.decode_argument(arguments)
            result = self.operations[function_name](*arguments)
            self.dummyFileStore[future.resultLocation] = json.dumps(result).encode()

        else:
            logging.info("Unknown function:", function_name)

    def get_result(self, future: Future) -> bytes:
        self.add_random_delay()
        return self.dummyFileStore[future.resultLocation]

    def notify_task_completion(self, task):
        self.add_delay()
        pass

    def sigterm_handler(self, signum, frame):
        logging.info("Exiting gracefully.")
        sys.exit(0)

    def add_random_delay(self):
        if self.add_delay:
            if randrange(100) > 50:
                logging.info(f"AddDelay is true - Adding delay of 5 seconds.")
                time.sleep(5)
            else:
                logging.info(f"AddDelay is true but not adding any delay.")
                
    def decode_argument(self, arg):
        # Convert bytes to NumPy array
        return [np.array(matrix) for matrix in json.loads(arg)]

    def dot_product(self, matrix1, matrix2):
        # Perform dot product of the matrices
        result = np.dot(matrix1, matrix2)
        return result.tolist()

    def mat_add(self, matrix1, matrix2):
        # Perform matrix addition
        result = np.add(matrix1, matrix2)
        return result.tolist()

    def mat_subtract(self, matrix1, matrix2):
        # Perform matrix subtraction
        result = np.subtract(matrix1, matrix2)
        return result.tolist()
