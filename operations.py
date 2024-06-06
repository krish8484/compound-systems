import numpy as np
import json
from exceptions import *
from simple_transformer import SimpleTransformer

class Operations:
    def __init__(self, worker):
        self.operationsMapping = {
            "dot_product": self.dot_product,
            "mat_add": self.mat_add,
            "mat_subtract": self.mat_subtract,
            "retrieval": self.retrieval,
            "generation": self.generation,
            "print_char_count": self.print_char_count,
            "sum_of_integers": self.sum_of_integers,
            "failing_operation_for_testing": self.failingOperationForTesting
            # Add more functions as needed
        }

        self.operationsWithGPU = {
            "dot_product",
            "retrieval",
            "generation",
            "print_char_count",
            "sum_of_integers",
            "failing_operation_for_testing"
            # Add more functions as needed
        }

        self.workerObj = worker

    def dot_product(self, matrix1, matrix2):
        # Perform dot product of the matrices
        if isinstance(matrix1, list):
            matrix1 = self.workerObj.get_result_from_worker(matrix1)
        if isinstance(matrix2, list):
            matrix2 = self.workerObj.get_result_from_worker(matrix2)
        matrix1 = np.array(json.loads(matrix1))
        matrix2 = np.array(json.loads(matrix2))
        result = np.dot(matrix1, matrix2)
        return result.tolist()


    def mat_add(self, matrix1, matrix2):
        # Perform matrix addition
        if isinstance(matrix1, list):
            matrix1 = self.workerObj.get_result_from_worker(matrix1)
        if isinstance(matrix2, list):
            matrix2 = self.workerObj.get_result_from_worker(matrix2)
        matrix1 = np.array(json.loads(matrix1))
        matrix2 = np.array(json.loads(matrix2))
        result = np.add(matrix1, matrix2)
        return result.tolist()

    def mat_subtract(self, matrix1, matrix2):
        # Perform matrix subtraction
        if isinstance(matrix1, list):
            matrix1 = self.workerObj.get_result_from_worker(matrix1)
        if isinstance(matrix2, list):
            matrix2 = self.workerObj.get_result_from_worker(matrix2)
        matrix1 = np.array(json.loads(matrix1))
        matrix2 = np.array(json.loads(matrix2))
        result = np.subtract(matrix1, matrix2)
        return result.tolist()
        

    def retrieval(self, matrix1, matrix2, top_k=1):
        # similarities as dot products
        # matrix1 are documents, matrix2 are embeddings
        if isinstance(matrix1, list):
            matrix1 = self.workerObj.get_result_from_worker(matrix1)
        if isinstance(matrix2, list):
            matrix2 = self.workerObj.get_result_from_worker(matrix2)
        matrix1 = np.array(json.loads(matrix1))
        matrix2 = np.array(json.loads(matrix2))
        dot_prod = np.dot(matrix1, matrix2)
        mag_1 = np.linalg.norm(matrix1)
        mag_2 = np.linalg.norm(matrix2)
        sim = dot_prod / (mag_1 * mag_2) 
        top_indices = np.argsort(sim)[-top_k:][::-1][0]
        result = [matrix1[i].tolist() for i in top_indices]
        return result

    def print_char_count(self, variable):
        if isinstance(variable, list):
            variable = self.workerObj.get_result_from_worker(variable)
        if isinstance(variable, bytes):
            variable = variable.decode('utf-8')
        if not isinstance(variable, str):
            raise ValueError("Input must be a string or bytes.")
        char_count = len(variable.strip('"'))
        return char_count

    def sum_of_integers(self, *args):
        processed_args = []
        for arg in args:
            if isinstance(arg, list):
                processed_args.append(int(self.workerObj.get_result_from_worker(arg)))
            elif isinstance(arg, bytes):
                processed_arg = int.from_bytes(arg, byteorder='big')
                processed_args.append(processed_arg)
        args = processed_args
        if not isinstance(args, list):
            raise ValueError("Input must be a list or bytes representing a list.")
        if not all(isinstance(item, int) for item in args):
            raise ValueError("All elements in the list must be integers.")
        total_sum = sum(args)
        return total_sum
        
    def generation(self, matrix1):
        if isinstance(matrix1, list):
            matrix1 = self.workerObj.get_result_from_worker(matrix1)
        matrix1 = np.array(json.loads(matrix1))
        model = SimpleTransformer(vocab_size=10, d_model=matrix1.shape[0])
        result = model.gen(matrix1)
        result = np.ceil(result * 10000) / 10000
        return result.tolist()
    
    def failingOperationForTesting(self, exceptionType):
        raise Exception("Failing operation for testing purposes")
