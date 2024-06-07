import threading
import queue
import signal
import sys
import random
from Data.task import Task
from Data.future import Future
from Data.WorkerInfo import WorkerInfo
from Data.WorkerInfoWrapper import WorkerInfoWrapper
from Worker.worker_client import WorkerClient
from Shared.logging_provider import logging
from Shared.exceptions import NoWorkerAvailableError
import grpc
import Shared.constants as constants
from queue import PriorityQueue
from typing import Union
from Shared.operations import Operations

class Scheduler:
    def __init__(self, scheduler_mode, assigned_workers_per_task):
        self.task_queue = queue.Queue()
        self.completion_status = {}
        self.workerIdLock = threading.Lock()
        self.schedulerMode = scheduler_mode
        self.assigned_workers_per_task = assigned_workers_per_task
        self.operations = Operations(self)
        self.globalIncrementalWorkerId = 0; # A globally incrementing worker id maintained by the scheduler

        if self.schedulerMode == constants.SCHEDULINGMODE_RANDOM:
            self.initialize_random_scheduler()
        elif self.schedulerMode == constants.SCHEDULINGMODE_ROUNDROBIN:
            self.initialize_round_robin_scheduler()
        elif self.schedulerMode == constants.SCHEDULINGMODE_LOADAWARE:
            self.initalize_load_aware_scheduler()
        elif self.schedulerMode == constants.SCHEDULINGMODE_POWEROFTWO:
            self.initalize_power_of_two_scheduler()

       
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
            gpuEnabledTask = task.taskDefintion in self.operations.operationsWithGPU
            logging.info(f"Getting worker for task {task}")
            worker = self.get_worker(gpuEnabledTask)
            logging.info(f"Received worker: {worker} for {task}")

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
            self.register_worker_random_mode(assignedWorkerId, workerInfo)
        elif self.schedulerMode == constants.SCHEDULINGMODE_ROUNDROBIN:
            self.register_worker_round_robin_mode(assignedWorkerId, workerInfo)
        elif self.schedulerMode == constants.SCHEDULINGMODE_LOADAWARE:
            self.register_worker_load_aware(assignedWorkerId, workerInfo)
        elif self.schedulerMode == constants.SCHEDULINGMODE_POWEROFTWO:
            self.register_worker_power_of_two(assignedWorkerId, workerInfo)

        logging.info(f"Worker {assignedWorkerId} registered. WorkerInfo: {workerInfo}")   
        return assignedWorkerId

    def task_completed(self, task_id, worker_id, status):
        logging.info(f"Scheduler recevied message of completion {task_id} from {worker_id} - Success {status}")
        if self.schedulerMode == constants.SCHEDULINGMODE_LOADAWARE:
            with self.WorkersTaskFinishedCountLock: #Lock to ensure that 2 task_completed calls from same worker both update the value correctly
                currentMapWorkerInfo = self.WorkersTaskFinishedCount[worker_id]
                currentMapWorkerInfo.currentAvailableCap = currentMapWorkerInfo.currentAvailableCap + 1
                self.WorkersTaskFinishedCount[worker_id] = currentMapWorkerInfo
        if self.schedulerMode == constants.SCHEDULINGMODE_POWEROFTWO:
            mapLock = None
            mapName = None
            if worker_id in self.WorkersListPowersOf2WithGPU:
                mapLock = self.WorkersPowerOf2WithGPULock
                mapName = self.WorkersPowerOf2WithGPU
            elif worker_id in self.WorkersListPowersOf2WithoutGPU:
                mapLock = self.WorkersPowerOf2WithoutGPULock
                mapName = self.WorkersPowerOf2WithoutGPU
            else:
                logging(f"WorkerId {worker_id} not present in any of the lists.")
                logging.info(f"Scheduler recevied message of completion of Task ID:{task_id} from Worker ID:{worker_id} - Success {status}")
                return True
            
            with mapLock:
                currentMapWorkerInfo = mapName[worker_id]
                currentMapWorkerInfo.currentAvailableCap = currentMapWorkerInfo.currentAvailableCap + 1
                mapName[worker_id] = currentMapWorkerInfo

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

    def get_worker(self, gpuEnabledTask) -> Union[WorkerInfo, WorkerInfoWrapper]:
        if self.schedulerMode == constants.SCHEDULINGMODE_RANDOM:
            logging.info(f"Getting worker for {self.schedulerMode}")
            return self.get_worker_random_mode(gpuEnabledTask)
        elif self.schedulerMode == constants.SCHEDULINGMODE_ROUNDROBIN:
            logging.info(f"Getting worker for {self.schedulerMode}")
            return self.get_worker_round_robin_mode(gpuEnabledTask)
        elif self.schedulerMode == constants.SCHEDULINGMODE_LOADAWARE:
            logging.info(f"Getting worker for {self.schedulerMode}. IsTaskGPUEnabled: {gpuEnabledTask}")
            return self.get_worker_load_aware(gpuEnabledTask)
        elif self.schedulerMode == constants.SCHEDULINGMODE_POWEROFTWO:
            logging.info(f"Getting worker for {self.schedulerMode}. IsTaskGPUEnabled: {gpuEnabledTask}")
            return self.get_worker_power_of_two(gpuEnabledTask)

    def get_worker_load_aware(self, gpuEnabledTask):
        if gpuEnabledTask is True:
            wrappedWorkerInfo = self.get_worker_info(self.WorkersWithGPU, self.WorkersWithGPULock)
            if wrappedWorkerInfo is None:
                # Try to populate the priority queue from the self.WorkersTaskFinishedCount
                self.WorkersWithGPU = PriorityQueue() # Discard and instantiate new priority queue
                self.repopulate_queue(self.WorkersWithGPU, self.WorkersWithGPULock, True)

                # After repopulation, attempt to get the worker again. If it still isn't found, it implies no woker is available.
                wrappedWorkerInfo = self.get_worker_info(self.WorkersWithGPU, self.WorkersWithGPULock)

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

    def get_worker_random_mode(self, gpuEnabledTask):
        listName = self.workerIdsWithoutGPU
        lockName = self.workerIdsWithoutGPULock

        if gpuEnabledTask is True:
            listName = self.workerIdsWithGPU
            lockName = self.workerIdsWithGPULock
        
        with lockName:
            if len(listName) > 0:
                pickedWorkerId = random.choice(listName)
            else:
                if gpuEnabledTask is not True:
                    # If the task doesn't require GPU and there are no workers available w/o GPU, try getting one with GPU
                    listName = self.workerIdsWithGPU
                    lockName = self.workerIdsWithGPULock

                    with lockName:
                        if len(listName) > 0:
                            pickedWorkerId = random.choice(listName)
                else:
                    logging.info(f"No worker found.")
                    raise NoWorkerAvailableError(self.schedulerMode)
        
        with self.workerMapLock:
            return self.workers[pickedWorkerId]

    def get_worker_round_robin_mode(self, gpuEnabledTask):
        queueName = self.workerQueueWithoutGPU
        lockName = self.workerQueueWithoutGPULock

        if gpuEnabledTask is True:
            queueName = self.workerQueueWithGPU
            lockName = self.workerQueueWithGPULock
        
        with lockName:
            if queueName.qsize() > 0:
                pickedWorkerId = queueName.get()
                queueName.put(pickedWorkerId)
            else:
                if gpuEnabledTask is not True:
                    # If the task doesn't require GPU and there are no workers available w/o GPU, try getting one with GPU
                    queueName = self.workerIdsWithGPU
                    lockName = self.workerIdsWithGPULock

                    with lockName:
                        if queueName.qsize() > 0:
                            pickedWorkerId = queueName.get()
                            queueName.put(pickedWorkerId)
                else:
                    logging.info(f"No worker found.")
                    raise NoWorkerAvailableError(self.schedulerMode)
        
        with self.workerMapLock:
            return self.workers[pickedWorkerId]

    def get_worker_power_of_two(self, gpuEnabledTask):
        if gpuEnabledTask is True:
            wrappedWorkerInfo =  self.get_worker_info_power_of_two(
                self.WorkersPowerOf2WithGPU,
                self.WorkersPowerOf2WithGPULock,
                self.WorkersListPowersOf2WithGPU)
            
            if wrappedWorkerInfo is None:
                logging.info(f"No worker found.")
                raise NoWorkerAvailableError(self.schedulerMode)
            
            logging.info(f"Received worker {wrappedWorkerInfo} for GPU Enabled Task.")
            return wrappedWorkerInfo
        else:
            if len(self.WorkersListPowersOf2WithoutGPU) == 0:
                # If no workers without gpu - try getting from worker with gpu
                wrappedWorkerInfo =  self.get_worker_info_power_of_two(
                    self.WorkersPowerOf2WithGPU,
                    self.WorkersPowerOf2WithGPULock,
                    self.WorkersListPowersOf2WithGPU)

                if wrappedWorkerInfo is None:
                    logging.info(f"No worker found.")
                    raise NoWorkerAvailableError(self.schedulerMode)
                
                logging.info(f"No non GPU workers found. Got one GPU worker {wrappedWorkerInfo} for non GPU Enabled Task.")
                return wrappedWorkerInfo
            elif len(self.WorkersListPowersOf2WithoutGPU) == 1:
                # If only worker is available in non cpu workers, get one from gpu workers and get the one with least load
                workerId1 = self.WorkersListPowersOf2WithoutGPU[0];
                logging.info(f"Non GPU Task. But only one non GPU worker available")

                wrappedWorkerInfo2 =  self.get_worker_info_power_of_two(
                    self.WorkersPowerOf2WithGPU,
                    self.WorkersPowerOf2WithGPULock,
                    self.WorkersListPowersOf2WithGPU)
                
                if wrappedWorkerInfo2 is None:
                    logging.info(f"No GPU worker available.")
                    with self.WorkersPowerOf2WithoutGPULock:
                        wrappedWorkerInfo = self.WorkersPowerOf2WithoutGPU[workerId1]
                        self.update_power_of_two_map(wrappedWorkerInfo, self.WorkersPowerOf2WithoutGPU)
                    logging.info(f"Got one non GPU worker {wrappedWorkerInfo} for non GPU Enabled Task.")
                    return wrappedWorkerInfo
                else:
                    with self.WorkersPowerOf2WithoutGPULock:
                        logging.info(f"Trying to get a worker from one GPU/non GPU workers for non GPU Enabled Task.")
                        wrappedWorkerInfo1 = self.WorkersPowerOf2WithoutGPU[workerId1]
                        wrappedWorkerInfo = self.get_worker_least_load(wrappedWorkerInfo1, wrappedWorkerInfo2)
                        logging.info(f"Returning {wrappedWorkerInfo} for non GPU Enabled Task.")

                        if wrappedWorkerInfo.workerId == workerId1:
                            logging.info(f"Returning worker from non GPU workers: {wrappedWorkerInfo} for non GPU Enabled Task.")
                            with self.WorkersPowerOf2WithoutGPULock:
                                self.update_power_of_two_map(wrappedWorkerInfo1, self.WorkersPowerOf2WithoutGPU)
                        else:
                            logging.info(f"Returning worker from GPU workers: {wrappedWorkerInfo} for non GPU Enabled Task.")
                            with self.WorkersPowerOf2WithGPULock:
                                self.update_power_of_two_map(wrappedWorkerInfo2, self.WorkersPowerOf2WithGPU)
                    return wrappedWorkerInfo
            else:
                # if more than 2 non gpu workers are available, get the best of random 2 workers
                logging.info(f"Non GPU Task and more than 2 non GPU workers available")
                wrappedWorkerInfo =  self.get_worker_info_power_of_two(
                    self.WorkersPowerOf2WithoutGPU,
                    self.WorkersPowerOf2WithoutGPULock,
                    self.WorkersListPowersOf2WithoutGPU)

                if wrappedWorkerInfo is None:
                    logging.info(f"No worker found.")
                    raise NoWorkerAvailableError(self.schedulerMode)
                
                logging.info(f"Non GPU Task and more than 2 non GPU workers available. Returning {wrappedWorkerInfo}")
                return wrappedWorkerInfo
    
    def register_worker_load_aware(self, assignedWorkerId, workerInfo: WorkerInfo):
        wrappedWorkerInfo = WorkerInfoWrapper(workerInfo, assignedWorkerId)
        if workerInfo.isGPUEnabled is True:
            self.update_priorityQueue(self.WorkersWithGPU, self.WorkersWithGPULock, wrappedWorkerInfo)
        else:
            self.update_priorityQueue(self.WorkersWithoutGPU, self.WorkersWithoutGPULock, wrappedWorkerInfo)
        
        _updatedWorkerInfo = WorkerInfoWrapper(workerInfo, assignedWorkerId)
        _updatedWorkerInfo.currentAvailableCap = 0
        with self.WorkersTaskFinishedCountLock:
            self.WorkersTaskFinishedCount[assignedWorkerId] = _updatedWorkerInfo
        
        logging.info(f"Finished registering the worker in {self.schedulerMode} mode with {assignedWorkerId}. WorkerInfo {workerInfo}")

    def register_worker_random_mode(self, assignedWorkerId, workerInfo: WorkerInfo):
        # Register all the worker info in a map. 
        # Maintain lists of worker with/without GPU enabled and that can be used during get worker calls.
        with self.workerMapLock:
            self.workers[assignedWorkerId] = workerInfo
        if workerInfo.isGPUEnabled is True:
            with self.workerIdsWithGPULock:
                self.workerIdsWithGPU.append(assignedWorkerId)
        else:
            with self.workerIdsWithoutGPULock:
                self.workerIdsWithoutGPU.append(assignedWorkerId)
        
        logging.info(f"Finished registering the worker in {self.schedulerMode} mode with {assignedWorkerId}. WorkerInfo {workerInfo}")

    def register_worker_round_robin_mode(self, assignedWorkerId, workerInfo: WorkerInfo):
        # Register all the worker info in a map. 
        # Maintain queue of worker with/without GPU enabled and that can be used during get worker calls.
        with self.workerMapLock:
            workerInfoWithWorkerId = WorkerInfoWrapper(workerInfo, assignedWorkerId)
            self.workers[assignedWorkerId] = workerInfoWithWorkerId
        if workerInfo.isGPUEnabled is True:
            with self.workerQueueWithGPULock:
                self.workerQueueWithGPU.put(assignedWorkerId)
        else:
            with self.workerQueueWithoutGPULock:
                self.workerQueueWithoutGPU.put(assignedWorkerId)
        
        logging.info(f"Finished registering the worker in {self.schedulerMode} mode with {assignedWorkerId}. WorkerInfo {workerInfo}")

    def register_worker_power_of_two(self, assignedWorkerId, workerInfo: WorkerInfo):
        mapLockName = self.WorkersPowerOf2WithoutGPULock
        mapName = self.WorkersPowerOf2WithoutGPU

        listLockName = self.WorkersListPowersOf2WithoutGPULock
        listName = self.WorkersListPowersOf2WithoutGPU

        if workerInfo.isGPUEnabled is True:
            mapLockName = self.WorkersPowerOf2WithGPULock
            mapName = self.WorkersPowerOf2WithGPU
            listLockName = self.WorkersListPowersOf2WithGPULock
            listName = self.WorkersListPowersOf2WithGPU
        
        # Append the list with worker id lock free as assignedWorkerId is created under lock
        listName.append(assignedWorkerId)

        with mapLockName:
            logging.info(f"Registering worker {workerInfo}. MapName {mapName} ListName {listName}")
            workerInfoWithWorkerId = WorkerInfoWrapper(workerInfo, assignedWorkerId)
            mapName[assignedWorkerId] = workerInfoWithWorkerId
        
        logging.info(f"Finished registering the worker in {self.schedulerMode} mode with {assignedWorkerId}. WorkerInfo {workerInfo}")

    def initalize_load_aware_scheduler(self):
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

    def initialize_random_scheduler(self):
        self.workerMapLock = threading.Lock()
        self.workers = {} # Map that maintains the worker id to hostName,portNum
        self.workerIdsWithGPULock = threading.Lock()
        self.workerIdsWithGPU = []
        self.workerIdsWithoutGPULock = threading.Lock()
        self.workerIdsWithoutGPU = []

    def initialize_round_robin_scheduler(self):
        self.workerMapLock = threading.Lock()
        self.workers = {} # Map that maintains the worker id to hostName,portNum
        self.workerQueueWithGPULock = threading.Lock()
        self.workerQueueWithGPU = queue.Queue() # Thread Safe Queue - Only used when scheduling mode is round robin
        self.workerQueueWithoutGPULock = threading.Lock()
        self.workerQueueWithoutGPU = queue.Queue() # Thread Safe Queue - Only used when scheduling mode is round robin

    def initalize_power_of_two_scheduler(self):
        self.WorkersPowerOf2WithGPULock = threading.Lock()
        self.WorkersPowerOf2WithoutGPULock = threading.Lock()
        self.WorkersPowerOf2WithoutGPU = {}
        self.WorkersPowerOf2WithGPU = {}
        self.WorkersListPowersOf2WithGPU = []
        self.WorkersListPowersOf2WithoutGPU = []
        self.WorkersListPowersOf2WithoutGPULock = threading.Lock()
        self.WorkersListPowersOf2WithGPULock = threading.Lock()
        self.HardwareGenerationMap = {
            "Gen1": 0.2,
            "Gen2": 0.4,
            "Gen3": 0.6,
            "Gen4": 0.8
        }

    def repopulate_queue(self, queueName, queueLock, GPUEnabledTask):
        logging.info(f"Repopulating queue {queueName} with {queueLock}")
        with self.WorkersTaskFinishedCountLock and queueLock:
            for workerIdFromMap in self.WorkersTaskFinishedCount:
                workerInfoFromMap = self.WorkersTaskFinishedCount[workerIdFromMap]
                if workerInfoFromMap.isGPUEnabled is GPUEnabledTask:
                    currentMapWorkerInfo = workerInfoFromMap
                    self.update_priorityQueueWithLockAcquired(queueName, workerInfoFromMap)
                    workerInfoObj = WorkerInfo(
                        hostName=currentMapWorkerInfo.hostName,
                        portNumber=currentMapWorkerInfo.portNumber,
                        maxThreadCount=currentMapWorkerInfo.maxThreadCount,
                        isGPUEnabled=currentMapWorkerInfo.isGPUEnabled,
                        hardwareGeneration=currentMapWorkerInfo.hardwareGeneration)
                    updatedWorkerInfo = WorkerInfoWrapper(workerInfoObj, currentMapWorkerInfo.workerId)
                    updatedWorkerInfo.currentAvailableCap = 0 # Reset the value to 0
                    self.WorkersTaskFinishedCount[workerIdFromMap] = updatedWorkerInfo
    
    def get_worker_info(self, queueName, lockName):
        logging.info(f"In get_worker_info for {queueName} with {lockName} and queue size {queueName.qsize()}")
        if queueName.qsize() > 0:
            # dequeue and enqueue again and return the wrapped worker info object
            with lockName:
                poppedInfo = queueName.get()
                logging.info(f"Got info {poppedInfo}")
                wrappedWorkerInfo = poppedInfo[1]
                logging.info(f"Current Available Cap {wrappedWorkerInfo.currentAvailableCap}")
                wrappedWorkerInfo.currentAvailableCap = wrappedWorkerInfo.currentAvailableCap -1
                if wrappedWorkerInfo.currentAvailableCap > 0: # If there is still capacity, add it back to the priority queue
                    self.update_priorityQueueWithLockAcquired(queueName, wrappedWorkerInfo)

            return wrappedWorkerInfo
        else:
            return None
        
    def get_worker_info_power_of_two(self, mapName, mapLockName, listName):
        logging.info(f"In get_worker_info for {mapName} with {mapLockName} and list size {len(listName)}")
        if len(listName) > 1:
            workerId1 = random.choice(listName)
            workerId2 = random.choice(listName)
            
            while workerId1 != workerId2:
                workerId2 = random.choice(listName)
            
            with mapLockName:
                wrappedWorkerInfo1 = mapName[workerId1]
                wrappedWorkerInfo2 = mapName[workerId2]
                wrappedWorkerInfo = self.get_worker_least_load(wrappedWorkerInfo1, wrappedWorkerInfo2)
                self.update_power_of_two_map(wrappedWorkerInfo, mapName)

            return wrappedWorkerInfo
        elif len(listName) == 1:
            workerId = listName[0]

            with mapLockName:
                wrappedWorkerInfo = mapName[workerId]
                self.update_power_of_two_map(wrappedWorkerInfo, mapName)

            return wrappedWorkerInfo
        else:
            return None
        
    def get_worker_least_load(self, wrappedWorkerInfo1, wrappedWorkerInfo2):
        if wrappedWorkerInfo1.currentAvailableCap > wrappedWorkerInfo2.currentAvailableCap:
            wrappedWorkerInfo = wrappedWorkerInfo1
        else:
            wrappedWorkerInfo = wrappedWorkerInfo2
        
        return wrappedWorkerInfo
    
    def update_power_of_two_map(self, wrappedWorkerInfo, mapName):
        wrappedWorkerInfo.currentAvailableCap = wrappedWorkerInfo.currentAvailableCap -1
        mapName[wrappedWorkerInfo.workerId] = wrappedWorkerInfo

    def update_priorityQueue(self, queueName, queueLock, wrappedWorkerInfo):
        with queueLock:
            self.update_priorityQueueWithLockAcquired(queueName, wrappedWorkerInfo)

    def update_priorityQueueWithLockAcquired(self, queueName, wrappedWorkerInfo):
        availableLoad = float(-1 * int(wrappedWorkerInfo.maxThreadCount) * float(self.HardwareGenerationMap[wrappedWorkerInfo.hardwareGeneration]))
        logging.info(f"Updating the priority queue with {availableLoad} for {wrappedWorkerInfo}")
        queueName.put((availableLoad, wrappedWorkerInfo))     
