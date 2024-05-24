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
        _future = api_pb2.Future(resultLocation = future.resultLocation, hostName = future.hostName, port = future.port)
        request = api_pb2.GetResultRequest(future=_future)
        response = self.stub.GetResult(request)
        return response.result

    def SubmitTask(self, task: Task) -> Future:
        _task = task.to_proto()
        request = api_pb2.TaskRequest(task=_task)
        response = self.stub.SubmitTask(request)
        return Future(resultLocation=response.future.resultLocation, hostName=response.future.hostName, port=response.future.port)
