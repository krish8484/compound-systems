import pytest
import sys
import time
# Add the parent directory of the tests directory to the Python path
sys.path.append("..")
from scheduler_client import SchedulerClient
from worker_client import WorkerClient
from Data.task import Task
from logging_provider import logging
import json
import constants

def poll_for_result(worker_client, future, expected_result):
    while True:
        result = worker_client.GetResult(future=future)
        if result == constants.NOTCOMPLETED:
            time.sleep(constants.WAITTIMEFORPOLLINGRESULT)
            continue
        elif result == constants.ERROR:
            assert 1 == 2, "An error occurred while fetching the result"
        else:
            result = json.loads(result)
            break
    assert result == expected_result, f"Expected {expected_result}, but got {result}"
    logging.info(f"Result: {result}")

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
    future = scheduler_client.SubmitTask(task)[0]

    worker_client = WorkerClient(future.hostName, future.port)

    expected_result = [[19, 22], [43, 50]]
    poll_for_result(worker_client, future, expected_result)


def test_mat_add(scheduler_client, matrix1, matrix2):
    task = Task(taskId="1", taskDefintion="mat_add", taskData=[json.dumps(matrix1).encode(), json.dumps(matrix2).encode()])
    future = scheduler_client.SubmitTask(task)[0]

    worker_client = WorkerClient(future.hostName, future.port)

    expected_result = [[6, 8], [10, 12]]
    poll_for_result(worker_client, future, expected_result)

def test_mat_subtract(scheduler_client, matrix1, matrix2):
    task = Task(taskId="2", taskDefintion="mat_subtract", taskData=[json.dumps(matrix1).encode(), json.dumps(matrix2).encode()])
    future = scheduler_client.SubmitTask(task)[0]

    worker_client = WorkerClient(future.hostName, future.port)

    expected_result = [[-4, -4 ], [-4, -4]]
    poll_for_result(worker_client, future, expected_result)

def test_passing_futures_as_args_flow(scheduler_client, matrix1, matrix2):
    future = scheduler_client.SubmitTask(Task(taskId="0", taskDefintion="dot_product", taskData=[json.dumps(matrix1).encode(), json.dumps(matrix2).encode()]))[0]
    future2 = scheduler_client.SubmitTask(Task(taskId="1", taskDefintion="mat_add", taskData=[json.dumps(matrix1).encode(), json.dumps(matrix2).encode()]))[0]
    future3 = scheduler_client.SubmitTask(Task(taskId="2", taskDefintion="mat_subtract", taskData=[future, future2]))[0]

    workerClient = WorkerClient(future3.hostName, future3.port)

    expected_result = [[13, 14], [33, 38]]
    poll_for_result(workerClient, future3, expected_result)

# Multiple workers here doesn't guarantee that the task will be assigned to different workers. It depends on the scheduling mode and the number of workers registered.
# Make sure --AssingedWorkersPerTask is set to more than 1 to ideally test this(not assigning would still work).
def test_assign_task_to_multiple_workers(scheduler_client, matrix1, matrix2):
    futures = scheduler_client.SubmitTask(Task(taskId="0", taskDefintion="dot_product", taskData=[json.dumps(matrix1).encode(), json.dumps(matrix2).encode()]))
    expected_result = [[19, 22], [43, 50]]

    for future in futures:
        logging.info(f"Future: {future}")
        worker_client = WorkerClient(future.hostName, future.port)
        poll_for_result(worker_client, future, expected_result)