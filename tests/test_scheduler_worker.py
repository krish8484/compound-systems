import pytest
import sys
import time
# Add the parent directory of the tests directory to the Python path
sys.path.append("..")
from Data.future import Future
from scheduler_client import SchedulerClient
from worker_client import WorkerClient
from Data.task import Task
from logging_provider import logging
import json
import constants
import numpy as np
import api_pb2

def get_result_from_worker(worker_client, future):
    while True:
        result = worker_client.GetResult(future=future)
        if result.resultStatus == api_pb2.ResultStatus.INPROGRESS:
            time.sleep(constants.WAITTIMEFORPOLLINGRESULT)
            continue
        else:
            return result
    

def validate_result(worker_client, future, expected_result):
    while True:
        result = worker_client.GetResult(future=future)
        if result.resultStatus == api_pb2.ResultStatus.INPROGRESS:
            time.sleep(constants.WAITTIMEFORPOLLINGRESULT)
            continue
        elif result.resultStatus == api_pb2.ResultStatus.ERROR:
            assert 1 == 2, f"An error occurred while fetching the result {result.error}"
        else:
            result = json.loads(result.data)
            break
    assert result == expected_result, f"Expected {expected_result}, but got {result}"
    logging.info(f"Result: {result}")

# Helper function to split text into n chunks
def split_text_into_chunks(text, num_chunks):
    chunk_size = len(text) // num_chunks
    chunks = [text[i * chunk_size:(i + 1) * chunk_size] for i in range(num_chunks)]
    if len(text) % num_chunks != 0:
        chunks[-1] += text[num_chunks * chunk_size:]  # Add the remaining text to the last chunk
    return chunks

@pytest.fixture
def scheduler_client():
    return SchedulerClient("localhost", 50051)

@pytest.fixture
def matrix1():
    return [[1, 2], [3, 4]]

@pytest.fixture
def matrix2():
    return [[5, 6], [7, 8]]

@pytest.fixture
def words():
    return ["hello", "world", "python", "multiple words", "with spaces", "complex_phrases!", "1234567890"]

@pytest.fixture
def numbers():
    return [1, 2, 3, 4, 5, 6, 7, 8]

@pytest.fixture
def large_text():
    return "This is an example of a large text. " * 1000000

def test_dot_product(scheduler_client, matrix1, matrix2):
    task = Task(taskId="0", taskDefintion="dot_product", taskData=[json.dumps(matrix1).encode(), json.dumps(matrix2).encode()])
    future = scheduler_client.SubmitTask(task)[0]

    worker_client = WorkerClient(future.hostName, future.port)

    expected_result = [[19, 22], [43, 50]]
    validate_result(worker_client, future, expected_result)

def test_mat_add(scheduler_client, matrix1, matrix2):
    task = Task(taskId="1", taskDefintion="mat_add", taskData=[json.dumps(matrix1).encode(), json.dumps(matrix2).encode()])
    future = scheduler_client.SubmitTask(task)[0]

    worker_client = WorkerClient(future.hostName, future.port)

    expected_result = [[6, 8], [10, 12]]
    validate_result(worker_client, future, expected_result)

def test_mat_subtract(scheduler_client, matrix1, matrix2):
    task = Task(taskId="2", taskDefintion="mat_subtract", taskData=[json.dumps(matrix1).encode(), json.dumps(matrix2).encode()])
    future = scheduler_client.SubmitTask(task)[0]

    worker_client = WorkerClient(future.hostName, future.port)

    expected_result = [[-4, -4 ], [-4, -4]]
    validate_result(worker_client, future, expected_result)

def test_char_count(scheduler_client, words):
    for word in words:
        task = Task(taskId="3", taskDefintion="print_char_count", taskData=[json.dumps(word).encode()])
        future = scheduler_client.SubmitTask(task)[0]

        worker_client = WorkerClient(future.hostName, future.port)

        expected_result = len(word)
        validate_result(worker_client, future, expected_result)

def test_addition(scheduler_client, numbers):
    byte_numbers = [bytes([num]) for num in numbers]
    task = Task(taskId="4", taskDefintion="sum_of_integers", taskData=byte_numbers)
    future = scheduler_client.SubmitTask(task)[0]

    worker_client = WorkerClient(future.hostName, future.port)

    expected_result = sum(numbers)
    validate_result(worker_client, future, expected_result)

def test_retrieval(scheduler_client, matrix1, matrix2):
    task = Task(taskId="5", taskDefintion="retrieval", taskData=[json.dumps(matrix1).encode(), json.dumps(matrix2).encode()])
    future = scheduler_client.SubmitTask(task)[0]

    worker_client = WorkerClient(future.hostName, future.port)

    expected_result = [[1, 2], [3, 4]]
    # poll_for_result(worker_client, future, expected_result)

def test_generation(scheduler_client, matrix1):
    task = Task(taskId="6", taskDefintion="generation", taskData=[json.dumps(matrix1).encode()])
    future = scheduler_client.SubmitTask(task)[0]

    worker_client = WorkerClient(future.hostName, future.port)

    expected_result = np.array([
        [[0.5671, 1.3624], [0.112, 0.4556]],
        [[1.4104, 0.7489], [0.2594, 0.6226]]
    ])

    # poll_for_result(worker_client, future, expected_result)

def test_passing_futures_as_args_flow(scheduler_client, matrix1, matrix2):
    future = scheduler_client.SubmitTask(Task(taskId="0", taskDefintion="dot_product", taskData=[json.dumps(matrix1).encode(), json.dumps(matrix2).encode()]))
    future2 = scheduler_client.SubmitTask(Task(taskId="1", taskDefintion="mat_add", taskData=[json.dumps(matrix1).encode(), json.dumps(matrix2).encode()]))
    future3 = scheduler_client.SubmitTask(Task(taskId="2", taskDefintion="mat_subtract", taskData=[future, future2]))[0]
    # future4 = scheduler_client.SubmitTask(Task(taskID="3", taskDefinition="retrieval", taskData=[json.dumps(matrix1).encode(), json.dumps(matrix2).encode()]))

    # TODO: add future4
    workerClient = WorkerClient(future3.hostName, future3.port)

    expected_result = [[13, 14], [33, 38]]
    validate_result(workerClient, future3, expected_result)

# Multiple workers here doesn't guarantee that the task will be assigned to different workers. It depends on the scheduling mode and the number of workers registered.
# Make sure --AssingedWorkersPerTask is set to more than 1 to ideally test this(not assigning would still work).
def test_assign_task_to_multiple_workers(scheduler_client, matrix1, matrix2):
    futures = scheduler_client.SubmitTask(Task(taskId="0", taskDefintion="dot_product", taskData=[json.dumps(matrix1).encode(), json.dumps(matrix2).encode()]))
    expected_result = [[19, 22], [43, 50]]

    for future in futures:
        logging.info(f"Future: {future}")
        worker_client = WorkerClient(future.hostName, future.port)
        validate_result(worker_client, future, expected_result)

def test_map_reduce(scheduler_client, large_text):
    chunks = split_text_into_chunks(large_text, num_chunks=1000)

    futures = []
    task_id = 1
    for chunk in chunks:
        task = Task(taskId=str(task_id), taskDefintion="print_char_count", taskData=[json.dumps(chunk).encode()])
        future = scheduler_client.SubmitTask(task)
        futures.append(future)
        task_id += 1

    task = Task(taskId=str(task_id), taskDefintion="sum_of_integers", taskData=futures)
    future = scheduler_client.SubmitTask(task)[0]

    worker_client = WorkerClient(future.hostName, future.port)

    expected_result = len(large_text)
    validate_result(worker_client, future, expected_result)

def test_worker_fetching_using_multiple_futures(scheduler_client, matrix1, matrix2):
    futures1 = scheduler_client.SubmitTask(Task(taskId="0", taskDefintion="dot_product", taskData=[json.dumps(matrix1).encode(), json.dumps(matrix2).encode()]))
    resultFuture = scheduler_client.SubmitTask(Task(taskId="0", taskDefintion="dot_product", taskData=[futures1, futures1]))[0]

    worker_client = WorkerClient(resultFuture.hostName, resultFuture.port)

    expected_result = [[1307, 1518], [2967, 3446]]
    validate_result(worker_client, resultFuture, expected_result)

def test_worker_fetching_using_two_futures_where_one_result_is_not_fetchable_and_the_other_is_fetchable(scheduler_client, matrix1, matrix2):
    notReachablePort = 60061
    failingFuture = Future("failingFuture", "localhost", notReachablePort)
    passingFuture = scheduler_client.SubmitTask(Task(taskId="0", taskDefintion="dot_product", taskData=[json.dumps(matrix1).encode(), json.dumps(matrix2).encode()]))[0]
    resultFuture = scheduler_client.SubmitTask(Task(taskId="0", taskDefintion="dot_product", taskData=[[failingFuture, passingFuture], [passingFuture]]))[0]

    worker_client = WorkerClient(resultFuture.hostName, resultFuture.port)

    expected_result = [[1307, 1518], [2967, 3446]]
    validate_result(worker_client, resultFuture, expected_result)

def test_worker_fetching_using_multiple_futures_where_both_results_are_not_fetchable(scheduler_client, matrix1, matrix2):
    notReachablePort = 60061
    failingFuture = Future("failingFuture", "localhost", notReachablePort)
    resultFuture = scheduler_client.SubmitTask(Task(taskId="0", taskDefintion="dot_product", taskData=[[failingFuture], [failingFuture]]))[0]

    worker_client = WorkerClient(resultFuture.hostName, resultFuture.port)
    result = get_result_from_worker(worker_client, resultFuture)

    assert result.resultStatus == api_pb2.ResultStatus.ERROR
    assert result.error.errorType == api_pb2.ErrorType.UNABLETOCONNECTWITHWORKERSFORRESULT
    assert result.error.failingFuture.hostName == failingFuture.hostName
    assert result.error.failingFuture.port == notReachablePort
    assert result.error.failingFuture.resultLocation == failingFuture.resultLocation

def test_worker_fetching_using_future_where_the_result_is_fetchable_but_errored(scheduler_client, matrix1, matrix2):
    failingTask = Task(taskId="1", taskDefintion="failing_operation_for_testing", taskData=["TestError".encode()])
    failingFuture = scheduler_client.SubmitTask(failingTask)[0]
    resultFuture = scheduler_client.SubmitTask(Task(taskId="0", taskDefintion="dot_product", taskData=[[failingFuture], [failingFuture]]))[0]

    worker_client = WorkerClient(resultFuture.hostName, resultFuture.port)
    result = get_result_from_worker(worker_client, resultFuture)

    assert result.resultStatus == api_pb2.ResultStatus.ERROR
    assert result.error.errorType == api_pb2.ErrorType.ERRORWHENEXECUTINGTASK