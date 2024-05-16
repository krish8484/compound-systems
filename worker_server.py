from concurrent import futures
import api_pb2
import api_pb2_grpc
import grpc
from logging_provider import logging
from worker import Worker
from Data.task import Task
from Data.future import Future

SCHEDULER_HOST = "localhost"
SCHEDULER_PORT = 50051
WORKER_HOST = "localhost"
WORKER_PORT = 50052

class WorkerServer(api_pb2_grpc.WorkerApiServicer):
    def __init__(self):
        self.worker = Worker(SCHEDULER_HOST, SCHEDULER_PORT, WORKER_HOST, WORKER_PORT)

    def GetResult(self, request, context):
        result = self.worker.get_result(Future(resultLocation= request.future.resultLocation, hostName=request.future.hostName, port=request.future.port))
        return api_pb2.GetResultResponse(result=result)

    def SubmitTask(self, request, context):
        future = self.worker.submit_task(Task(taskId=request.task.taskId, taskDefintion=request.task.taskDefinition, taskData=request.task.taskData))
        return api_pb2.TaskResponse(future=api_pb2.Future(resultLocation=future.resultLocation, hostName=future.hostName, port=future.port))

def serve():
    server = grpc.server(futures.ThreadPoolExecutor())
    api_pb2_grpc.add_WorkerApiServicer_to_server(WorkerServer(), server)
    server.add_insecure_port('localhost:50052')
    server.start()
    logging.info("Worker listening on {}:{}".format(WORKER_HOST, WORKER_PORT))
    server.wait_for_termination()

if __name__ == '__main__':
    serve()