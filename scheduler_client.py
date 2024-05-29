import api_pb2_grpc
import api_pb2
import grpc
from Data.future import Future
from Data.task import Task
from Data.WorkerInfo import WorkerInfo

class SchedulerClient:

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.channel = grpc.insecure_channel('{}:{}'.format(self.host, self.port))
        self.stub = api_pb2_grpc.SchedulerApiStub(self.channel)

    def SubmitTask(self, task: Task) -> list[Future]:
        _task = task.to_proto()
        request = api_pb2.TaskRequest(task=_task)
        response = self.stub.SubmitTask(request)
        return [Future(resultLocation=future.resultLocation, hostName=future.hostName, port=future.port) for future in response.futures]
    
    def TaskCompleted(self, task_id, worker_id, _status) -> bool:
        _protoStatus = _status.to_proto()
        request = api_pb2.TaskCompletedRequest(
            taskId = task_id,
            workerId = worker_id,
            status = _protoStatus)
        response = self.stub.TaskCompleted(request)
        return response.status.success
    
    def RegisterWorker(self, workerInfo: WorkerInfo) -> int:
        _workerInfo = api_pb2.WorkerInfo(
            hostName = workerInfo.hostName,
            portNumber = workerInfo.portNumber,
            maxThreadCount = workerInfo.maxThreadCount,
            isGPUEnabled = workerInfo.isGPUEnabled)
        request = api_pb2.RegisterWorkerRequest(workerInfo = _workerInfo)
        response = self.stub.RegisterWorker(request)
        return response.workerIdAssignedByScheduler
