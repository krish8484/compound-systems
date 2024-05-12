from concurrent import futures
import api_pb2
import api_pb2_grpc
import grpc
import logging

logging.basicConfig(format='%(asctime)s - %(process)d - %(levelname)s - %(message)s', level=logging.DEBUG)

class SchedulerServer(api_pb2_grpc.SchedulerApiServicer):
    def SubmitTask(self, request, context):
        pass
    
    def TaskCompleted(self, request, context):
        pass 

def serve():
    server = grpc.server(futures.ThreadPoolExecutor())
    api_pb2_grpc.add_SchedulerApiServicer_to_server(SchedulerServer(), server)
    server.add_insecure_port('localhost:50051')
    server.start()
    logging.info("Scheduler listening on {}".format("localhost:50051"))
    server.wait_for_termination()

if __name__ == '__main__':
    serve()