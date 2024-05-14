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
        _future = api_pb2.Future(resultLocation = future.result_location, hostName = future.host_name, port = future.port)
        request = api_pb2.GetResultRequest(future=_future)
        response = self.stub.GetResult(request)
        return response.result

    def ExecuteTask(self, task: Task) -> Future:
        _task = api_pb2.Task(taskId = task.taskId, taskDefinition = task.taskDefintion, taskData = task.taskData)
        request = api_pb2.TaskRequest(task=_task)
        response = self.stub.ExecuteTask(request)
        return Future(result_location=response.future.resultLocation, host_name=response.future.hostName, port=response.future.port)
