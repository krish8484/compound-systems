class Future:

    def __init__(self, result_location, host_name, port):
        self.result_location = result_location
        self.host_name = host_name
        self.port = port
    
    def __str__(self):
        return f"[result_location:{self.result_location} || host_name:{self.host_name} || port:{self.port}]"