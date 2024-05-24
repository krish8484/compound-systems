import pytest
import sys

# Add the parent directory of the tests directory to the Python path
sys.path.append("..")
from scheduler_client import SchedulerClient
from worker_client import WorkerClient
from Data.task import Task
from logging_provider import logging
import json

@pytest.fixture
def scheduler_client():
    return SchedulerClient("localhost", 50051)

@pytest.fixture
def matrix1():
    return [[1, 2], [3, 4]]

@pytest.fixture
def matrix2():
    return [[5, 6], [7, 8]]

def test_dot_product(scheduler_client, matrix1, matrix2):
    task = Task(taskId="0", taskDefintion="dot_product", taskData=[json.dumps(matrix1).encode(), json.dumps(matrix2).encode()])
    future = scheduler_client.SubmitTask(task)

    worker_client = WorkerClient(future.hostName, future.port)
    result = json.loads(worker_client.GetResult(future))  # Ensure result is deserialized from JSON

    expected_result = [[19, 22], [43, 50]]
    assert result == expected_result, f"Expected {expected_result}, but got {result}"
    logging.info(f"Result: {result}")

def test_mat_add(scheduler_client, matrix1, matrix2):
    task = Task(taskId="1", taskDefintion="mat_add", taskData=[json.dumps(matrix1).encode(), json.dumps(matrix2).encode()])
    future = scheduler_client.SubmitTask(task)

    worker_client = WorkerClient(future.hostName, future.port)
    result = json.loads(worker_client.GetResult(future))  # Ensure result is deserialized from JSON

    expected_result = [[6, 8], [10, 12]]
    assert result == expected_result, f"Expected {expected_result}, but got {result}"
    logging.info(f"Result: {result}")

def test_mat_subtract(scheduler_client, matrix1, matrix2):
    task = Task(taskId="2", taskDefintion="mat_subtract", taskData=[json.dumps(matrix1).encode(), json.dumps(matrix2).encode()])
    future = scheduler_client.SubmitTask(task)

    worker_client = WorkerClient(future.hostName, future.port)
    result = json.loads(worker_client.GetResult(future))  # Ensure result is deserialized from JSON

    expected_result = [[-4, -4 ], [-4, -4]]
    assert result == expected_result, f"Expected {expected_result}, but got {result}"
    logging.info(f"Result: {result}")

def test_passing_futures_as_args_flow(scheduler_client, matrix1, matrix2):
    future = scheduler_client.SubmitTask(Task(taskId="0", taskDefintion="dot_product", taskData=[json.dumps(matrix1).encode(), json.dumps(matrix2).encode()]))
    future2 = scheduler_client.SubmitTask(Task(taskId="1", taskDefintion="mat_add", taskData=[json.dumps(matrix1).encode(), json.dumps(matrix2).encode()]))
    future3 = scheduler_client.SubmitTask(Task(taskId="2", taskDefintion="mat_subtract", taskData=[future, future2]))

    workerClient = WorkerClient(future.hostName, future.port)
    result = json.loads(workerClient.GetResult(future3))

    expected_result = [[13, 14], [33, 38]]
    assert result == expected_result, f"Expected {expected_result}, but got {result}"
    logging.info(f"Result: {result}")

    
