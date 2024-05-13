import grpc
import api_pb2_grpc
import api_pb2
from Data.future import Future
from Data.task import Task

class WorkerClient:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.channel = grpc.insecure_channel('{}:{}'.format(self.host, self.port))
        self.stub = api_pb2_grpc.WorkerApiStub(self.channel)

    def GetResult(self, future: Future) -> bytes:
        _future = api_pb2.Future(future.result_location)
        request = api_pb2.GetResultRequest(task_id=_future)
        response = self.stub.GetResult(request)
        return response.result

    def ExecuteTask(self, task: Task) -> Future:
        _task = api_pb2.Task(taskId = task.task_id, taskDefinition = task.taskDefintion, taskData = task.taskData)
        request = api_pb2.TaskRequest(task=_task)
        response = self.stub.ExecuteTask(request)
        return Future(result_location=response.future.resultLocation)
