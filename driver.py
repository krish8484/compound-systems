from scheduler_client import SchedulerClient
from worker_client import WorkerClient
from Data.task import Task
from logging_provider import logging


# Example usage
if __name__ == "__main__":
    schedulerClient = SchedulerClient("localhost", 50051)
    future = schedulerClient.SubmitTask(Task(taskId="test id", taskDefintion="test definition", taskData="test".encode()))
    logging.info(f"Received future: {future}")
    workerClient = WorkerClient(future.hostName, future.port)
    while True:
        result = workerClient.GetResult(future)
        logging.info(f"Result: {result}")
        if input("Enter 'q' to quit or any other key to get result again from worker:") == 'q':
            break
    
    

