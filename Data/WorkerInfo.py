class WorkerInfo:
    
    def __init__(self, hostName, portNumber, maxThreadCount, isGPUEnabled, hardwareGeneration):
        self.hostName = hostName
        self.portNumber = portNumber
        self.maxThreadCount = maxThreadCount
        self.isGPUEnabled = isGPUEnabled
        self.hardwareGeneration = hardwareGeneration

    def __str__(self):
        return "[HostName: {} || PortNumber: {} || MaxThreadCount: {} || IsGPUEnabled: {} || Hardware Generation: {}]".format(self.hostName, self.portNumber, self.maxThreadCount, self.isGPUEnabled, self.hardwareGeneration)

    def __lt__(self, other):
        return self.portNumber < other.portNumber
    
    def __gt__(self, other):
        return self.portNumber > other.portNumber