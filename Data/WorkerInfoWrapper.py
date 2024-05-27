class WorkerInfoWrapper:
    
    def __init__(self, workerInfo, workerId):
        self.hostName = workerInfo.hostName
        self.portNumber = workerInfo.portNumber
        self.maxThreadCount = workerInfo.maxThreadCount
        self.isGPUEnabled = workerInfo.isGPUEnabled
        self.workerId = workerId

    def __str__(self):
        return "[HostName: {} || PortNumber: {} || MaxThreadCount: {} || IsGPUEnabled: {} || WorkerId: {}]".format(self.hostName, self.portNumber, self.maxThreadCount, self.isGPUEnabled, self.workerId)
