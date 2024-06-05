from enum import Enum
from typing import Union
import api_pb2
from Data.task import Task
from Data.future import Future


class Error:
    def __init__(self, errorType: api_pb2.ErrorType, errorMessage: str, failingTask: Union[Task, api_pb2.Task] = None, failingFuture: Union[Future, api_pb2.Future] = None):
        self.errorType = errorType
        self.errorMessage = errorMessage
        self.failingFuture = None
        self.failingTask = None
        if failingTask:
            if (isinstance(failingTask, Task)):
                self.failingTask = failingTask
            else:
                self.failingTask = Task(failingTask.taskId, failingTask.taskDefinition, failingTask.taskData)
        if failingFuture:
            if (isinstance(failingFuture, Future)):
                self.failingFuture = failingFuture
            else:
                self.failingFuture = Future(failingFuture.resultLocation, failingFuture.hostName, failingFuture.port)

    def to_proto(self):
        error_proto = api_pb2.Error(
            errorType=self.errorType,
            errorMessage=self.errorMessage
        )
        if self.failingTask:
            error_proto.failingTask.CopyFrom(self.failingTask.to_proto())
        if self.failingFuture:
            error_proto.failingFuture.CopyFrom(self.failingFuture.to_proto())
        return error_proto
    
    def __str__(self):
        return f"ErrorType: {self.errorType}\nErrorMessage: {self.errorMessage}\nFailingTask: {self.failingTask}\nFailingFuture: {self.failingFuture}"
