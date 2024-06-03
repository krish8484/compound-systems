from Data.future import Future
import api_pb2

class Task:
    # self.taskData is a list of future or/and bytes
    def __init__(self, taskId, taskDefintion, taskData):
        self.taskId : str = taskId
        self.taskDefintion : str = taskDefintion
        if len(taskData)!=0 and not isinstance(taskData[0], api_pb2.TaskDataParam):
            self.taskData = taskData
        # Converts list of api_pb2.TaskDataParam to list of list[future] and/or bytes
        else:
            self.taskData = []
            for i in taskData:
                if i.WhichOneof("dataParam") == "listOfFutures":
                    self.taskData.append([Future(future.resultLocation, future.hostName, future.port) for future in i.listOfFutures.futures])
                else:
                    self.taskData.append(i.data)

    # Converts the current Task object to a protobuf Task message (api_pb2.Task)
    def to_proto(self) -> api_pb2.Task:
        task = api_pb2.Task(taskId = self.taskId, taskDefinition = self.taskDefintion)
        for i in self.taskData:
            if isinstance(i, bytes):
                task.taskData.append(api_pb2.TaskDataParam(data = i))
            else:
                task.taskData.append(api_pb2.TaskDataParam(listOfFutures = api_pb2.ListOfFutures(futures = [future.to_proto() for future in i])))
        return task
        
    def __str__(self):
        return "[Task ID: {} || Task Definition: {}]".format(self.taskId, self.taskDefintion)


