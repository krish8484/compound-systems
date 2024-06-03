from scheduler_client import SchedulerClient
from worker_client import WorkerClient
from Data.task import Task
from logging_provider import logging
import json

# Example usage
if __name__ == "__main__":
    schedulerClient = SchedulerClient("localhost", 50051)
    matrix1 = [[1, 2], [3, 4]]
    matrix2 = [[5, 6], [7, 8]]

    futures1 = schedulerClient.SubmitTask(Task(taskId="0", taskDefintion="dot_product", taskData=[json.dumps(matrix1).encode(), json.dumps(matrix2).encode()]))
    futures2 = schedulerClient.SubmitTask(Task(taskId="1", taskDefintion="mat_add", taskData=[json.dumps(matrix1).encode(), json.dumps(matrix2).encode()]))
    future3 = schedulerClient.SubmitTask(Task(taskId="2", taskDefintion="mat_subtract", taskData=[futures1, futures2]))[0]
    future4 = schedulerClient.SubmitTask(Task(taskId="3", taskDefintion="retrieval", taskData=[json.dumps(matrix1).encode(), json.dumps(matrix2).encode()]))[0]
    future5 = schedulerClient.SubmitTask(Task(taskId="4", taskDefintion="generation", taskData=[json.dumps(matrix1).encode()]))[0]
    
    logging.info(f"Received future: {futures1}")
    logging.info(f"Received future: {futures2}")
    logging.info(f"Received future: {future3}")
    logging.info(f"Received future: {future4}")
    logging.info(f"Received future: {future5}")
    
    future1 = futures1[0]
    future2 = futures2[0]

    workerClient = WorkerClient(future1.hostName, future1.port)
    result = workerClient.GetResult(future1)
    logging.info(f"Result: {result.data}")
    workerClient = WorkerClient(future2.hostName, future2.port)
    result = workerClient.GetResult(future2)
    logging.info(f"Result: {result.data}")
    workerClient = WorkerClient(future3.hostName, future3.port)
    result = workerClient.GetResult(future3)
    logging.info(f"Result: {result.data}")
    workerClient = WorkerClient(future4.hostName, future4.port)
    result = workerClient.GetResult(future4)
    logging.info(f"Result: {result.data}")
    workerClient = WorkerClient(future5.hostName, future5.port)
    result = workerClient.GetResult(future5)
    logging.info(f"Result: {result.data}")
