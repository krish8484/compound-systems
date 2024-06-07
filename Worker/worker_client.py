import grpc
import api_pb2_grpc
import api_pb2
from Data.future import Future
from Data.task import Task
from Data.result import Result

class WorkerClient:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.channel = grpc.insecure_channel('{}:{}'.format(self.host, self.port))
        self.stub = api_pb2_grpc.WorkerApiStub(self.channel)

    def GetResult(self, future: Future, timeout = None) -> Result:
        _future = api_pb2.Future(resultLocation = future.resultLocation, hostName = future.hostName, port = future.port)
        request = api_pb2.GetResultRequest(future=_future)
        if (timeout != None):
            result = self.stub.GetResult(request, timeout = float(timeout)).result
        else:
            result = self.stub.GetResult(request).result
        return Result(result.resultStatus, result.data, result.error)

    def SubmitTask(self, task: Task, timeout = None) -> Future:
        _task = task.to_proto()
        request = api_pb2.TaskRequest(task=_task)
        if (timeout != None):
            response = self.stub.SubmitTask(request, timeout = float(timeout))
        else:
            response = self.stub.SubmitTask(request)
        return Future(resultLocation=response.future.resultLocation, hostName=response.future.hostName, port=response.future.port)
