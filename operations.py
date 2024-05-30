from Data.future import Future
from logging_provider import logging
import numpy as np
import json
import constants
from exceptions import WorkerUnableToExecuteTaskError

class Operations:
    def __init__(self, worker):
        self.operationsMapping = {
            "dot_product": self.dot_product,
            "mat_add": self.mat_add,
            "mat_subtract": self.mat_subtract,
            "print_char_count": self.print_char_count,
            "sum_of_integers": self.sum_of_integers,
            # Add more functions as needed
        }
        self.workerObj = worker

    def dot_product(self, matrix1, matrix2):
        # Perform dot product of the matrices
        try:
            if matrix1 == type(Future):
                matrix1 = self.workerObj.get_result_from_worker(matrix1)
            if matrix2 == type(Future):
                matrix2 = self.workerObj.get_result_from_worker(matrix2)
            matrix1 = np.array(json.loads(matrix1))
            matrix2 = np.array(json.loads(matrix2))
            result = np.dot(matrix1, matrix2)
            return result.tolist()
        except WorkerUnableToExecuteTaskError as e:
            logging.error("Unable to get result for future:", e.future)
        except Exception as e:
            logging.error("Unexpected error:", e)
        return constants.ERROR

    def mat_add(self, matrix1, matrix2):
        # Perform matrix addition
        try:
            if matrix1 == type(Future):
                matrix1 = self.workerObj.get_result_from_worker(matrix1)
            if matrix2 == type(Future):
                matrix2 = self.workerObj.get_result_from_worker(matrix2)
            matrix1 = np.array(json.loads(matrix1))
            matrix2 = np.array(json.loads(matrix2))
            result = np.add(matrix1, matrix2)
            return result.tolist()
        except WorkerUnableToExecuteTaskError as e:
            logging.error("Unable to get result for future:", e.future)
        except Exception as e:
            logging.error("Unexpected error:", e)
        return constants.ERROR

    def mat_subtract(self, matrix1, matrix2):
        # Perform matrix subtraction
        try:
            if isinstance(matrix1, Future):
                matrix1 = self.workerObj.get_result_from_worker(matrix1)
            if isinstance(matrix2, Future):
                matrix2 = self.workerObj.get_result_from_worker(matrix2)
            matrix1 = np.array(json.loads(matrix1))
            matrix2 = np.array(json.loads(matrix2))
            result = np.subtract(matrix1, matrix2)
            return result.tolist()
        except WorkerUnableToExecuteTaskError as e:
            logging.error("Unable to get result for future:", e.future)
        except Exception as e:
            logging.error("Unexpected error:", e)
        return constants.ERROR

    def print_char_count(self, variable):
        try:
            if isinstance(variable, Future):
                variable = self.workerObj.get_result_from_worker(variable)
            if isinstance(variable, bytes):
                variable = variable.decode('utf-8')
            if not isinstance(variable, str):
                raise ValueError("Input must be a string or bytes.")
            char_count = len(variable.strip('"'))
            return char_count
        except WorkerUnableToExecuteTaskError as e:
            logging.error("Unable to get result for future:", e.future)
        except Exception as e:
            logging.error("Unexpected error:", e)
            return constants.ERROR

    def sum_of_integers(self, args):
        try:
            if isinstance(args, Future):
                args = self.workerObj.get_result_from_worker(args)
            if isinstance(args, bytes):
                args = args.decode('utf-8')
                args = eval(args)  # Convert string representation of list back to list
            if not isinstance(args, list):
                raise ValueError("Input must be a list or bytes representing a list.")
            if not all(isinstance(item, int) for item in args):
                raise ValueError("All elements in the list must be integers.")
            total_sum = sum(args)
            return total_sum
        except WorkerUnableToExecuteTaskError as e:
            logging.error("Unable to get result for future:", e.future)
        except Exception as e:
            logging.error("Unexpected error:", e)
            return constants.ERROR




