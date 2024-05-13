from concurrent import futures
import api_pb2
import api_pb2_grpc
import grpc
from logging_provider import logging
from worker import Worker

SCHEDULER_HOST = "localhost"
SCHEDULER_PORT = 50051
WORKER_HOST = "localhost"
WORKER_PORT = 50052
WORKER_ID = ":".format(WORKER_HOST, WORKER_PORT)

class WorkerServer(api_pb2_grpc.WorkerApiServicer):
    def __init__(self):
        self.worker = Worker(SCHEDULER_HOST, SCHEDULER_PORT, WORKER_HOST, WORKER_PORT)

    def GetResult(self, request, context):
        pass

    def ExecuteTask(self, request, context):
        pass

def serve():
    server = grpc.server(futures.ThreadPoolExecutor())
    api_pb2_grpc.add_WorkerApiServicer_to_server(WorkerServer(), server)
    server.add_insecure_port('localhost:50052')
    server.start()
    logging.info("Worker listening on {}".format(WORKER_ID))
    server.wait_for_termination()

if __name__ == '__main__':
    serve()