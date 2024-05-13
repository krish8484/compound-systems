# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import api_pb2 as api__pb2


class SchedulerApiStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.SubmitTask = channel.unary_unary(
                '/api.SchedulerApi/SubmitTask',
                request_serializer=api__pb2.TaskRequest.SerializeToString,
                response_deserializer=api__pb2.TaskResponse.FromString,
                )
        self.TaskCompleted = channel.unary_unary(
                '/api.SchedulerApi/TaskCompleted',
                request_serializer=api__pb2.TaskCompletedRequest.SerializeToString,
                response_deserializer=api__pb2.TaskCompletedResponse.FromString,
                )
        self.RegisterWorker = channel.unary_unary(
                '/api.SchedulerApi/RegisterWorker',
                request_serializer=api__pb2.RegisterWorkerRequest.SerializeToString,
                response_deserializer=api__pb2.RegisterWorkerResponse.FromString,
                )


class SchedulerApiServicer(object):
    """Missing associated documentation comment in .proto file."""

    def SubmitTask(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def TaskCompleted(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def RegisterWorker(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_SchedulerApiServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'SubmitTask': grpc.unary_unary_rpc_method_handler(
                    servicer.SubmitTask,
                    request_deserializer=api__pb2.TaskRequest.FromString,
                    response_serializer=api__pb2.TaskResponse.SerializeToString,
            ),
            'TaskCompleted': grpc.unary_unary_rpc_method_handler(
                    servicer.TaskCompleted,
                    request_deserializer=api__pb2.TaskCompletedRequest.FromString,
                    response_serializer=api__pb2.TaskCompletedResponse.SerializeToString,
            ),
            'RegisterWorker': grpc.unary_unary_rpc_method_handler(
                    servicer.RegisterWorker,
                    request_deserializer=api__pb2.RegisterWorkerRequest.FromString,
                    response_serializer=api__pb2.RegisterWorkerResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'api.SchedulerApi', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class SchedulerApi(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def SubmitTask(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/api.SchedulerApi/SubmitTask',
            api__pb2.TaskRequest.SerializeToString,
            api__pb2.TaskResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def TaskCompleted(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/api.SchedulerApi/TaskCompleted',
            api__pb2.TaskCompletedRequest.SerializeToString,
            api__pb2.TaskCompletedResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def RegisterWorker(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/api.SchedulerApi/RegisterWorker',
            api__pb2.RegisterWorkerRequest.SerializeToString,
            api__pb2.RegisterWorkerResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)


class WorkerApiStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.GetResult = channel.unary_unary(
                '/api.WorkerApi/GetResult',
                request_serializer=api__pb2.GetResultRequest.SerializeToString,
                response_deserializer=api__pb2.GetResultResponse.FromString,
                )
        self.ExecuteTask = channel.unary_unary(
                '/api.WorkerApi/ExecuteTask',
                request_serializer=api__pb2.TaskRequest.SerializeToString,
                response_deserializer=api__pb2.TaskResponse.FromString,
                )


class WorkerApiServicer(object):
    """Missing associated documentation comment in .proto file."""

    def GetResult(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ExecuteTask(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_WorkerApiServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'GetResult': grpc.unary_unary_rpc_method_handler(
                    servicer.GetResult,
                    request_deserializer=api__pb2.GetResultRequest.FromString,
                    response_serializer=api__pb2.GetResultResponse.SerializeToString,
            ),
            'ExecuteTask': grpc.unary_unary_rpc_method_handler(
                    servicer.ExecuteTask,
                    request_deserializer=api__pb2.TaskRequest.FromString,
                    response_serializer=api__pb2.TaskResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'api.WorkerApi', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class WorkerApi(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def GetResult(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/api.WorkerApi/GetResult',
            api__pb2.GetResultRequest.SerializeToString,
            api__pb2.GetResultResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def ExecuteTask(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/api.WorkerApi/ExecuteTask',
            api__pb2.TaskRequest.SerializeToString,
            api__pb2.TaskResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
