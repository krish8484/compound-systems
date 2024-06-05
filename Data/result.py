from typing import Union
from Data.error import Error
import api_pb2

class Result:
    def __init__(self, resultStatus: api_pb2.ResultStatus, data: bytes = None, error: Union[api_pb2.Error, Error]  = None):
        self.resultStatus = resultStatus
        self.data = data
        self.error = None
        if error:
            if isinstance(error, Error):
                self.error = error
            else:
                self.error = Error(error.errorType, error.errorMessage, error.failingTask, error.failingFuture)

    def to_proto(self):
        result_proto = api_pb2.Result(
            resultStatus=self.resultStatus,
            data=self.data
        )
        if self.error:
            result_proto.error.CopyFrom(self.error.to_proto()) 
        return result_proto

