from concurrent import futures
import api_pb2
import api_pb2_grpc
import grpc
import logging

logging.basicConfig(format='%(asctime)s - %(process)d - %(levelname)s - %(message)s', level=logging.DEBUG)

class WorkerServer(api_pb2_grpc.WorkerApiServicer):
    def GetResult(self, request, context):
        pass

    def ExecuteTask(self, request, context):
        pass

def serve():
    server = grpc.server(futures.ThreadPoolExecutor())
    api_pb2_grpc.add_WorkerApiServicer_to_server(WorkerServer(), server)
    server.add_insecure_port('localhost:50052')
    server.start()
    logging.info("Worker listening on {}".format("localhost:50052"))
    server.wait_for_termination()

if __name__ == '__main__':
    serve()