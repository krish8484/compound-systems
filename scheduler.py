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
from queue import PriorityQueue
from typing import Union

class Scheduler:
    def __init__(self, scheduler_mode, assigned_workers_per_task):
        self.task_queue = queue.Queue()
        self.completion_status = {}
        self.workerIdLock = threading.Lock()
        self.schedulerMode = scheduler_mode
        self.assigned_workers_per_task = assigned_workers_per_task

        if self.schedulerMode == constants.SCHEDULINGMODE_RANDOM:
            self.workerMapLock = threading.Lock()
            self.workers = {} # Map that maintains the worker id to hostName,portNum - Only used when scheduling mode is Random
        elif self.schedulerMode == constants.SCHEDULINGMODE_ROUNDROBIN:
            self.workerQueue = queue.Queue() # Thread Safe Queue - Only used when scheduling mode is round robin
        elif self.schedulerMode == constants.SCHEDULINGMODE_LOADAWARE:
            self.WorkersWithGPULock = threading.Lock()
            self.WorkersWithoutGPULock = threading.Lock()
            self.WorkersWithGPU = PriorityQueue()
            self.WorkersWithoutGPU = PriorityQueue()
            self.HardwareGenerationMap = {
                "Gen1": 0.2,
                "Gen2": 0.4,
                "Gen3": 0.6,
                "Gen4": 0.8
            }
            self.WorkersTaskFinishedCount = {} # Map that gets populated when a task finishes. This would be used to repopulate the priority queue opportunistically.
            self.WorkersTaskFinishedCountLock = threading.Lock()

        self.globalIncrementalWorkerId = 0; # A globally incrementing worker id maintained by the scheduler
       
        signal.signal(signal.SIGINT, self.sigterm_handler)

    def submit_task(self, task : Task) -> list[Future]:
        futures = []
        threads = [threading.Thread(target=self.submit_task_to_worker, args=(task, futures)) for _ in range(self.assigned_workers_per_task)]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()
        if len(futures) == 0:
            logging.error(f"No workers found to submit task {task}")
            raise NoWorkerAvailableError(self.schedulerMode)
        return futures

    def submit_task_to_worker(self, task, futures):
        try:
            worker = self.get_worker()
            worker_client = WorkerClient(worker.hostName , int(worker.portNumber))
            logging.info(f"Task {task} submitted to worker:{worker}")
            futures.append(worker_client.SubmitTask(task, timeout=constants.SCHEDULER_TIMEOUT_TO_RECEIVE_FUTURE_FROM_WORKER))
        except NoWorkerAvailableError as noWorkerAvailableError:
            logging.error(f"SubmitTask: No worker available. Scheduler mode: {noWorkerAvailableError.schedulerMode}")
        except grpc.RpcError as rpc_error:
            if rpc_error.code() == grpc.StatusCode.CANCELLED:
                logging.error(f"SubmitTask: RPC Cancelled. RPC Error: code={rpc_error.code()} message={rpc_error.details()}")
            elif rpc_error.code() == grpc.StatusCode.UNAVAILABLE:
                logging.error(f"SubmitTask: Worker Unavailable. RPC Error: code={rpc_error.code()} message={rpc_error.details()}")
            elif rpc_error.code() == grpc.StatusCode.DEADLINE_EXCEEDED:
                logging.error(f"SubmitTask: Deadline Exceeded. RPC Error: code={rpc_error.code()} message={rpc_error.details()}")
            else:
                logging.error(f"SubmitTask: Unhandled RPC error: code={rpc_error.code()} message={rpc_error.details()}")

    def register_worker(self, workerInfo: WorkerInfo) -> int:
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
        elif self.schedulerMode == constants.SCHEDULINGMODE_LOADAWARE:
            if workerInfo.isGPUEnabled is True:
                self.update_priorityQueue(self.WorkersWithGPU, self.WorkersWithGPULock, workerInfo)
            else:
                self.update_priorityQueue(self.WorkersWithoutGPU, self.WorkersWithoutGPULock, workerInfo)
            
            _updatedWorkerInfo = workerInfo
            _updatedWorkerInfo.currentAvailableCap = 0
            with self.WorkersTaskFinishedCountLock:
                self.WorkersTaskFinishedCount[assignedWorkerId] = _updatedWorkerInfo

        logging.info(f"Worker {assignedWorkerId} registered. WorkerInfo: {workerInfo}")   
        return assignedWorkerId

    def task_completed(self, task_id, worker_id, status):
        logging.info(f"Scheduler recevied message of completion {task_id} from {worker_id} - Success {status}")
        with self.WorkersTaskFinishedCountLock: #Lock to ensure that 2 task_completed calls from same worker both update the value correctly
            currentMapWorkerInfo = self.WorkersTaskFinishedCount[worker_id]
            currentMapWorkerInfo.currentAvailableCap = currentMapWorkerInfo.currentAvailableCap + 1
            self.WorkersTaskFinishedCount[worker_id] = currentMapWorkerInfo

        logging.info(f"Scheduler recevied message of completion of Task ID:{task_id} from Worker ID:{worker_id} - Success {status}")
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

    def get_worker(self) -> Union[WorkerInfo, WorkerInfoWrapper]:
        if self.schedulerMode == constants.SCHEDULINGMODE_RANDOM:
            logging.info(f"Getting worker for {self.schedulerMode}")
            if self.globalIncrementalWorkerId > 1:
                random_worker_id = random.randint(0, self.globalIncrementalWorkerId - 1)
                with self.workerMapLock:
                    return self.workers[random_worker_id]
            elif self.globalIncrementalWorkerId == 1:
                with self.workerMapLock:
                    return self.workers[0]
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
        elif self.schedulerMode == constants.SCHEDULINGMODE_LOADAWARE:
            logging.info(f"Getting worker for {self.schedulerMode}")
            wrappedWorkerInfo = self.get_worker_info(self.WorkersWithoutGPU, self.WorkersWithoutGPULock)
            if wrappedWorkerInfo is None:
                # Try getting worker from GPU enabled workers
                wrappedWorkerInfo = self.get_worker_info(self.WorkersWithGPU, self.WorkersWithGPULock)

                if wrappedWorkerInfo is None:
                    # Try to populate the priority queue from the self.WorkersTaskFinishedCount
                    self.WorkersWithoutGPU = PriorityQueue() # Discard and instantiate new priority queue
                    self.repopulate_queue(self.WorkersWithoutGPU, self.WorkersWithoutGPULock, False)

                    # After repopulation, attempt to get the worker again. If it still isn't found, it implies no woker is available.
                    wrappedWorkerInfo = self.get_worker_info(self.WorkersWithoutGPU, self.WorkersWithoutGPULock)

                    if wrappedWorkerInfo is None:
                        logging.info(f"No worker found.")
                        raise NoWorkerAvailableError(self.schedulerMode)
                    else:
                        logging.info(f"Got the worker info after repopulating from the map")
                        return wrappedWorkerInfo
                else:
                    logging.info(f"Got the worker info from GPU Enabled priority queue")
                    return wrappedWorkerInfo
            else:
                logging.info(f"Got the worker info from GPU Disabled priority queue")
                return wrappedWorkerInfo
            # When GPU enabled task is enabled - this code can get uncommented
            # if task.isGPUReqd is True:
            #     if self.WorkersWithGPU.qsize() > 0:
            #         # dequeue and enqueue again and return the wrapped worker info object
            #         wrappedWorkerInfo = self.WorkersWithGPU.get()
            #         wrappedWorkerInfo.currentAvailableCap = wrappedWorkerInfo.currentAvailableCap -1
            #         with self.WorkersWithGPULock:
            #             self.WorkersWithGPU.put(
            #                 -1 * int(wrappedWorkerInfo.currentAvailableCap) * self.HardwareGenerationMap[wrappedWorkerInfo.hardwareGeneration],
            #                 wrappedWorkerInfo)
            #         return wrappedWorkerInfo
            #     else:
            #         logging.info(f"No worker found.")
            #         raise NoWorkerAvailableError(self.schedulerMode)
        
    def repopulate_queue(self, queueName, queueLock, GPUEnabledTask):
        logging.info(f"Repopulating queue {queueName} with {queueLock}")
        with self.WorkersTaskFinishedCountLock and queueLock:
            for workerIdFromMap in self.WorkersTaskFinishedCount:
                workerInfoFromMap = self.WorkersTaskFinishedCount[workerIdFromMap]
                if workerInfoFromMap.isGPUEnabled is GPUEnabledTask:
                    currentMapWorkerInfo = workerInfoFromMap
                    self.update_priorityQueueWithLockAcquired(queueName, workerInfoFromMap)
                    currentMapWorkerInfo.currentAvailableCap = 0 # Reset the value to 0
                    self.WorkersTaskFinishedCount[workerIdFromMap] = currentMapWorkerInfo
    
    def get_worker_info(self, queueName, lockName):
        logging.info(f"In get_worker_info for {queueName} with {lockName} and queue size {queueName.qsize()}")
        if queueName.qsize() > 0:
            # dequeue and enqueue again and return the wrapped worker info object
            with lockName:
                poppedInfo = queueName.get()
                logging.info(f"Got info {poppedInfo}")
                wrappedWorkerInfo = poppedInfo[1]
                wrappedWorkerInfo.currentAvailableCap = wrappedWorkerInfo.currentAvailableCap -1
                if wrappedWorkerInfo.currentAvailableCap > 0: # If there is still capacity, add it back to the priority queue
                    self.update_priorityQueueWithLockAcquired(queueName, wrappedWorkerInfo)

            return wrappedWorkerInfo
        else:
            return None
        
    def update_priorityQueue(self, queueName, queueLock, workerInfo):
        with queueLock:
            self.update_priorityQueueWithLockAcquired(queueName, workerInfo)

    def update_priorityQueueWithLockAcquired(self, queueName, workerInfo):
        availableLoad = float(-1 * int(workerInfo.maxThreadCount) * float(self.HardwareGenerationMap[workerInfo.hardwareGeneration]))
        logging.info(f"Updating the priority queue with {availableLoad} for {workerInfo}")
        queueName.put((availableLoad, workerInfo))
        
