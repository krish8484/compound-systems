import signal
import sys
import uuid
from Data.result import Result
from scheduler_client import SchedulerClient
from worker_client import WorkerClient
from Data.future import Future
from Data.task import Task
from Data.WorkerInfo import WorkerInfo
from Data.Status import Status
from logging_provider import logging
import threading
from random import randrange
import grpc
import json
import time
from operations import Operations
import constants
from exceptions import *
import api_pb2

class UniqueIDGenerator:

    def get_unique_id(self):
        return uuid.uuid4()

class Worker:
    def __init__(
            self,
            scheduler_host,
            scheduler_port,
            worker_host,
            worker_port,
            add_delay,
            max_thread_count,
            gpu_enabled,
            hardware_generation):
        self.scheduler_host = scheduler_host
        self.scheduler_port = scheduler_port
        self.worker_host = worker_host
        self.worker_port = worker_port
        self.scheduler_client = SchedulerClient(self.scheduler_host, self.scheduler_port)
        self.add_delay = add_delay
        self.max_thread_count = max_thread_count
        self.gpu_enabled = gpu_enabled
        self.hardware_generation = hardware_generation
        self.generator = UniqueIDGenerator()
        self.add_random_delay()
        workerInfo = WorkerInfo(
            self.worker_host,
            self.worker_port,
            self.max_thread_count,
            self.gpu_enabled,
            self.hardware_generation)
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
        self.dummyFileStore : dict[str, Result] = {}
        self.operations = Operations(self)
        signal.signal(signal.SIGINT, self.sigterm_handler)

    def submit_task(self, task: Task) -> Future:
        self.add_random_delay()
        if task.taskDefintion not in self.operations.operationsMapping:
            logging.info("Unknown function:", task.taskDefintion)
            raise grpc.RpcError(grpc.StatusCode.INVALID_ARGUMENT, 'The function name is unknown')

        resultLocation = str(self.generator.get_unique_id())
        self.dummyFileStore[resultLocation] = Result(resultStatus = api_pb2.ResultStatus.INPROGRESS)
        future = Future(resultLocation=resultLocation, hostName=self.worker_host, port=self.worker_port)
        threading.Thread(target=self.execute_task, args=(task, future)).start()
        logging.info(f"submitted task {task} to worker {self.worker_id}")
        return future

    def execute_task(self, task: Task, future: Future):
        logging.info(f"executing task {task}")
        self.add_random_delay()
        function_name = task.taskDefintion
        try:
            resultData = self.operations.operationsMapping[function_name](*task.taskData)
            result = Result(api_pb2.ResultStatus.COMPLETED, json.dumps(resultData).encode())
        except WorkerUnableToExecuteTaskError as e:
            result = Result(resultStatus=api_pb2.ResultStatus.ERROR, error=e.error);
        except UnableToReachWorkerForResultError as e:
            error = Error(errorType=api_pb2.ErrorType.UNABLETOCONNECTWITHWORKERSFORRESULT, errorMessage=e.grpcErrorDetails, failingFuture=e.future)
            result = Result(resultStatus=api_pb2.ResultStatus.ERROR, error=error);
        except Exception as e:
            error = Error(errorType=api_pb2.ErrorType.ERRORWHENEXECUTINGTASK, errorMessage=str(e), failingTask=task)
            result = Result(resultStatus=api_pb2.ResultStatus.ERROR, error=error);
        self.dummyFileStore[future.resultLocation] = result
        if (result.resultStatus == api_pb2.ResultStatus.COMPLETED):
            self.notify_task_completion(task, True)
        else:
            self.notify_task_completion(task, False)
    
    def get_result(self, future: Future) -> Result:
        self.add_random_delay()
        logging.info(f"Get Result called on {future.resultLocation}")
        return self.dummyFileStore[future.resultLocation]

    def notify_task_completion(self, _task: Task, _success: bool):
        self.add_random_delay()
        _status = Status(status= _success)
        logging.info(f"Notifying task completion {_task.taskId} - Success {_status}")
        tmp = self.scheduler_client.TaskCompleted(
            _task.taskId,
            self.worker_id,
            _status)
        logging.info(f"Notified the scheduler on task completion of Task ID: {_task.taskId} - {tmp}")


    def get_result_from_worker(self, futures: list[Future]) -> bytes:
        errorResult = None
        errorFuture = None
        grpcErrorDetails = None
        for future in futures:
            if (future.hostName == self.worker_host and future.port == self.worker_port):
                return self.get_result(future).data
            workerClient = WorkerClient(future.hostName, future.port)
            while True:
                try:
                    result = workerClient.GetResult(future=future)
                    if result.resultStatus == api_pb2.ResultStatus.INPROGRESS:
                        time.sleep(constants.WAITTIMEFORPOLLINGRESULT)
                        continue
                    elif result.resultStatus == api_pb2.ResultStatus.ERROR:
                        logging.error(f"GetResultFromWorker: Unable to retreive result from worker as it failed when executing task for the future: {future}")
                        errorResult = result
                        break
                    else:
                        return result.data
                except grpc.RpcError as rpc_error:
                    if rpc_error.code() == grpc.StatusCode.CANCELLED:
                        logging.error(f"GetResultFromWorker: RPC Cancelled. RPC Error: code={rpc_error.code()} message={rpc_error.details()}") 
                    elif rpc_error.code() == grpc.StatusCode.UNAVAILABLE:
                        logging.error(f"GetResultFromWorker: Scheduler Unavailable. RPC Error: code={rpc_error.code()} message={rpc_error.details()}")
                    else:
                        logging.error(f"GetResultFromWorker: Unhandled RPC error: code={rpc_error.code()} message={rpc_error.details()}")
                    errorFuture = future
                    grpcErrorDetails = rpc_error.details()
                    break

        logging.error(f"GetResultFromWorker: Unable to retreive results for all the futures given")
        if errorResult:
            raise WorkerUnableToExecuteTaskError(errorResult.error)
        raise UnableToReachWorkerForResultError(errorFuture, grpcErrorDetails)
                

    def sigterm_handler(self, signum, frame):
        logging.info("Exiting gracefully.")
        sys.exit(0)

    def add_random_delay(self):
        if self.add_delay:
            delayVal = randrange(5,10)
            logging.info(f"AddDelay is true - Adding delay of {delayVal} seconds.")
        else:
            logging.info(f"AddDelay is false - not adding any delay.")
