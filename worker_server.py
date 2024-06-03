from concurrent import futures
import api_pb2
import api_pb2_grpc
import grpc
from logging_provider import logging
from worker import Worker
from Data.task import Task
from Data.future import Future
import argparse

SCHEDULER_HOST = "localhost"
SCHEDULER_PORT = 50051
WORKER_HOST = "localhost"
WORKER_PORT = 50052
ADD_DELAY = False
MAX_THREAD_COUNT = 2
GPU_ENABLED = False

class WorkerServer(api_pb2_grpc.WorkerApiServicer):
    def __init__(self):
        self.worker = Worker(
            SCHEDULER_HOST,
            SCHEDULER_PORT,
            WORKER_HOST,
            WORKER_PORT,
            ADD_DELAY,
            MAX_THREAD_COUNT,
            GPU_ENABLED)

    def GetResult(self, request, context):
        result = self.worker.get_result(Future(resultLocation= request.future.resultLocation, hostName=request.future.hostName, port=request.future.port))
        return api_pb2.GetResultResponse(result=result.to_proto())

    def SubmitTask(self, request, context):
        future = self.worker.submit_task(Task(taskId=request.task.taskId, taskDefintion=request.task.taskDefinition, taskData=request.task.taskData))
        return api_pb2.TaskResponse(future=api_pb2.Future(resultLocation=future.resultLocation, hostName=future.hostName, port=future.port))

def serve():
    server = grpc.server(futures.ThreadPoolExecutor())
    api_pb2_grpc.add_WorkerApiServicer_to_server(WorkerServer(), server)
    hostNamePortNumber = WORKER_HOST + ':' + str(WORKER_PORT)
    server.add_insecure_port(hostNamePortNumber)
    server.start()
    logging.info("Worker listening on {}".format(hostNamePortNumber))
    server.wait_for_termination()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-p",
        "--PortNumber",
        type=int,
        help="Please pass the port number.",
        required=True)

    parser.add_argument(
        "-m",
        "--MaxThreadCount",
        type=int,
        help="Please pass the max thread that you want worker to spawn.",
        required=False,
        default=5)

    parser.add_argument(
        '--gpuEnabled',
        action="store_true",
        help='Please pass GPUEnabled flag. This makes the worker eligible for GPU enabled tasks.')

    parser.add_argument(
        "--addDelay",
        action="store_true", 
        help="Please pass the AddDelay parameter. This adds a random delay in worker operations.")
    
    args = parser.parse_args()
    WORKER_PORT = int(args.PortNumber)
    MAX_THREAD_COUNT = int(args.MaxThreadCount)

    if args.addDelay: 
        ADD_DELAY = True
        logging.info("Will add random delays..") 
    else: 
        logging.info("Will not add random delays")

    if args.gpuEnabled: 
        GPU_ENABLED = True
        logging.info("Will mark worker as GPU Enabled..") 
    else: 
        logging.info("Will not mark worker as GPU Enabled") 
    
    serve()
