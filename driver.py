from scheduler_client import SchedulerClient
from worker_client import WorkerClient
from Data.task import Task
from logging_provider import logging


# Example usage
if __name__ == "__main__":
    schedulerClient = SchedulerClient("localhost", 50051)
    future = schedulerClient.SubmitTask(Task(taskId="test id", taskDefintion="test definition", taskData="test".encode()))
    logging.info(f"Received future: {future}")
    workerClient = WorkerClient(future.host_name, future.port)
    result = workerClient.GetResult(future)
    logging.info(f"Result: {result}")
    
    
