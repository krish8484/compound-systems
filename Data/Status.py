import api_pb2

class Status:
    
    def __init__(self, status):
        self.success = status

    # Converts the current Status object to a protobuf Status message (api_pb2.Status)
    def to_proto(self) -> api_pb2.Status:
        _status = api_pb2.Status(success = self.success)
        return _status
    
    def __str__(self):
        return "[Status success : {}]".format(self.success)