from Data.future import Future

class WorkerUnableToExecuteTaskError(Exception):
    def __init__(self, future: Future):
        self.future = future

class NoWorkerAvailableError(Exception):
    def __init__(self, schedulerMode):
        self.schedulerMode = schedulerMode