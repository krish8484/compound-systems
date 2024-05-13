from concurrent import futures
import api_pb2
import api_pb2_grpc
import grpc
from logging_provider import logging
from scheduler import Scheduler

class SchedulerServer(api_pb2_grpc.SchedulerApiServicer):

    def __init__(self):
        self.scheduler = Scheduler()

    def SubmitTask(self, request, context):
        pass
    
    def TaskCompleted(self, request, context):
        self.scheduler.task_completed(request.taskId, request.workerId)
        return api_pb2.TaskCompletedResponse(status = api_pb2.Status(success = True))
    
    def RegisterWorker(self, request, context):
        self.scheduler.register_worker(request.workerId)
        return api_pb2.RegisterWorkerResponse(status = api_pb2.Status(success = True))

def serve():
    server = grpc.server(futures.ThreadPoolExecutor())
    api_pb2_grpc.add_SchedulerApiServicer_to_server(SchedulerServer(), server)
    server.add_insecure_port('localhost:50051')
    server.start()
    logging.info("Scheduler listening on {}".format("localhost:50051"))
    server.wait_for_termination()

if __name__ == '__main__':
    serve()