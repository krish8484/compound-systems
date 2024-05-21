from Data.future import Future
import api_pb2

class Task:
    # self.taskData is a list of future or/and bytes
    def __init__(self, taskId, taskDefintion, taskData):
        self.taskId = taskId
        self.taskDefintion = taskDefintion
        if len(taskData)!=0 and not isinstance(taskData[0], api_pb2.TaskDataParam):
            self.taskData = taskData
        # Converts list of api_pb2.TaskDataParam to list of future and/or bytes
        else:
            self.taskData = []
            for i in taskData:
                if i.WhichOneof("dataParam") == "future":
                    self.taskData.append(Future(i.future.resultLocation, i.future.hostName, i.future.port))
                else:
                    self.taskData.append(i.data)

    def to_proto(self) -> api_pb2.Task:
        task = api_pb2.Task(taskId = self.taskId, taskDefinition = self.taskDefintion)
        for i in self.taskData:
            if isinstance(i, Future):
                task.taskData.append(api_pb2.TaskDataParam(future = api_pb2.Future(resultLocation = i.resultLocation, hostName = i.hostName, port = i.port)))
            else:
                task.taskData.append(api_pb2.TaskDataParam(data = i))
        return task
        
    def __str__(self):
        return "[Task ID: {} || Task Definition: {}]".format(self.taskId, self.taskDefintion)
