class WorkerInfo:
    
    def __init__(self, hostName, portNumber, maxThreadCount, isGPUEnabled):
        self.hostName = hostName
        self.portNumber = portNumber
        self.maxThreadCount = maxThreadCount
        self.isGPUEnabled = isGPUEnabled

    def __str__(self):
        return "[HostName: {} || PortNumber: {} || MaxThreadCount: {} || IsGPUEnabled: {}]".format(self.hostName, self.portNumber, self.maxThreadCount, self.isGPUEnabled)
