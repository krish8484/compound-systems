import api_pb2

class Future:

    def __init__(self, resultLocation, hostName, port):
        self.resultLocation = resultLocation
        self.hostName = hostName
        self.port = port

    def to_proto(self):
        return api_pb2.Future(resultLocation = self.resultLocation, hostName = self.hostName, port = self.port)
    
    def __str__(self):
        return f"[resultLocation:{self.resultLocation} || host_name:{self.hostName} || port:{self.port}]"