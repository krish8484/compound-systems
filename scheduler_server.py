from concurrent import futures
import api_pb2
import api_pb2_grpc
import grpc
from logging_provider import logging
from scheduler import Scheduler
from Data.task import Task
from Data.WorkerInfo import WorkerInfo
import argparse
import constants

SCHEDULER_HOST = "localhost"
SCHEDULER_PORT = 50051
SCHEDULER_MODE = "Random"
ASSINGED_WORKERS_PER_TASK = 1

class SchedulerServer(api_pb2_grpc.SchedulerApiServicer):

    def __init__(self):
        self.scheduler = Scheduler(SCHEDULER_MODE, ASSINGED_WORKERS_PER_TASK)

    def SubmitTask(self, request, context):
        futures = self.scheduler.submit_task(Task(taskId = request.task.taskId, taskDefintion = request.task.taskDefinition, taskData = request.task.taskData))
        proto_futures = [api_pb2.Future(resultLocation=future.resultLocation, hostName=future.hostName, port=future.port) for future in futures]
        return api_pb2.SubmitTaskToSchedulerResponse(futures=proto_futures)
    
    def TaskCompleted(self, request, context):
        logging.info(f"Received request of task completion")
        try:
            self.scheduler.task_completed(
                request.taskId,
                request.workerId,
                request.status)
            return api_pb2.TaskCompletedResponse(status = api_pb2.Status(success = True))
        except Exception as e:
            logging.error(e)
            return api_pb2.TaskCompletedResponse(status = api_pb2.Status(success = False))
    
    def RegisterWorker(self, request, context):
        assignedWorkerId = self.scheduler.register_worker(
            WorkerInfo(
                hostName = request.workerInfo.hostName,
                portNumber=request.workerInfo.portNumber,
                maxThreadCount=request.workerInfo.maxThreadCount,
                isGPUEnabled=request.workerInfo.isGPUEnabled,
                hardwareGeneration=request.workerInfo.hardwareGeneration))
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
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-p",
        "--PortNumber",
        type=int,
        help="Please pass the port number.",
        required=True)
    
    parser.add_argument(
        "-m",
        "--SchedulerMode",
        choices=['Random', 'RoundRobin', 'LoadAware'],
        help="Choose 'Random' or 'RoundRobin' mode",
        required=True)
    
    parser.add_argument(
        "-w",
        "--AssingedWorkersPerTask",
        type=int,
        help="Please pass the no of workers to assign per task submitted to scheduler",
        required=False,
        default=1)
   
    args = parser.parse_args()
    SCHEDULER_PORT = int(args.PortNumber)
    SCHEDULER_MODE = args.SchedulerMode
    ASSINGED_WORKERS_PER_TASK = int(args.AssingedWorkersPerTask)

    if SCHEDULER_MODE == constants.SCHEDULINGMODE_RANDOM:
        logging.info("Random scheduling mode selected..")
    elif SCHEDULER_MODE == constants.SCHEDULINGMODE_ROUNDROBIN:
        logging.info("RoundRobin scheduling mode selected..")
    elif SCHEDULER_MODE == constants.SCHEDULINGMODE_LOADAWARE:
        logging.info("LoadAware scheduling mode selected..")
    
    serve()