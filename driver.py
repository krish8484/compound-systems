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

    future = schedulerClient.SubmitTask(Task(taskId="0", taskDefintion="dot_product", taskData=[json.dumps(matrix1).encode(), json.dumps(matrix2).encode()]))[0]
    future2 = schedulerClient.SubmitTask(Task(taskId="1", taskDefintion="mat_add", taskData=[json.dumps(matrix1).encode(), json.dumps(matrix2).encode()]))[0]
    future3 = schedulerClient.SubmitTask(Task(taskId="2", taskDefintion="mat_subtract", taskData=[future, future2]))[0]

    logging.info(f"Received future: {future}")
    logging.info(f"Received future: {future2}")
    logging.info(f"Received future: {future3}")

    workerClient = WorkerClient(future.hostName, future.port)
    result = workerClient.GetResult(future)
    logging.info(f"Result: {result}")
    workerClient = WorkerClient(future2.hostName, future2.port)
    result = workerClient.GetResult(future2)
    logging.info(f"Result: {result}")
    workerClient = WorkerClient(future3.hostName, future3.port)
    result = workerClient.GetResult(future3)
    logging.info(f"Result: {result}")
