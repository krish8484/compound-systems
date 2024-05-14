import api_pb2_grpc
import api_pb2
import grpc
from Data.future import Future
from Data.task import Task

class SchedulerClient:

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.channel = grpc.insecure_channel('{}:{}'.format(self.host, self.port))
        self.stub = api_pb2_grpc.SchedulerApiStub(self.channel)

    def SubmitTask(self, task: Task) -> Future:
        _task = api_pb2.Task(taskId = task.taskId, taskDefinition = task.taskDefintion, taskData = task.taskData)
        request = api_pb2.TaskRequest(task=_task)
        response = self.stub.SubmitTask(request)
        return Future(result_location=response.future.resultLocation, host_name=response.future.hostName, port=response.future.port)
    
    def TaskCompleted(self, task_id, worker_id) -> bool:
        request = api_pb2.TaskCompletedRequest(taskId = task_id, workerId = worker_id)
        response = self.stub.TaskCompleted(request)
        return response.status.success
    
    def RegisterWorker(self, worker_id) -> bool:
        request = api_pb2.RegisterWorkerRequest(workerId = worker_id)
        response = self.stub.RegisterWorker(request)
        return response.status.success
    

