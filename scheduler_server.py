from concurrent import futures
import api_pb2
import api_pb2_grpc
import grpc
from logging_provider import logging
from scheduler import Scheduler
from Data.task import Task
from Data.WorkerInfo import WorkerInfo

SCHEDULER_HOST = "localhost"
SCHEDULER_PORT = 50051

class SchedulerServer(api_pb2_grpc.SchedulerApiServicer):

    def __init__(self):
        self.scheduler = Scheduler()

    def SubmitTask(self, request, context):
        future = self.scheduler.submit_task(Task(taskId = request.task.taskId, taskDefintion = request.task.taskDefinition, taskData = request.task.taskData))
        return api_pb2.TaskResponse(future=api_pb2.Future(resultLocation=future.resultLocation, hostName=future.hostName, port=future.port))
    
    def TaskCompleted(self, request, context):
        try:
            self.scheduler.task_completed(request.taskId, request.workerId)
            return api_pb2.TaskCompletedResponse(status = api_pb2.Status(success = True))
        except Exception as e:
            logging.error(e)
            return api_pb2.TaskCompletedResponse(status = api_pb2.Status(success = False))
    
    def RegisterWorker(self, request, context):
        print("In scheduler server")
        assignedWorkerId = self.scheduler.register_worker(
            WorkerInfo(
                hostName = request.workerInfo.hostName,
                portNumber=request.workerInfo.portNumber,
                maxThreadCount=request.workerInfo.maxThreadCount,
                isGPUEnabled=request.workerInfo.isGPUEnabled))
        return api_pb2.RegisterWorkerResponse(workerIdAssignedByScheduler = assignedWorkerId)

def serve():
    scheduler_endpoint = f"{SCHEDULER_HOST}:{SCHEDULER_PORT}"
    server = grpc.server(futures.ThreadPoolExecutor())
    api_pb2_grpc.add_SchedulerApiServicer_to_server(SchedulerServer(), server)
    server.add_insecure_port(scheduler_endpoint)
    server.start()
    logging.info("Scheduler listening on {}".format(scheduler_endpoint))
    server.wait_for_termination()

if __name__ == '__main__':
    serve()