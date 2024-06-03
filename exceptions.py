from Data.future import Future
from Data.error import Error

class WorkerUnableToExecuteTaskError(Exception):
    def __init__(self, errorFromWorker: Error):
        self.error = errorFromWorker

class NoWorkerAvailableError(Exception):
    def __init__(self, schedulerMode):
        self.schedulerMode = schedulerMode

class UnableToReachWorkerForResultError(Exception):
    def __init__(self, future: Future, grpcErrorDetails: str):
        self.future = future
        self.grpcErrorDetails = grpcErrorDetails
