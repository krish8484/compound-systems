class Task:
    
    def __init__(self, taskId, taskDefintion, taskData):
        self.taskId = taskId
        self.taskDefintion = taskDefintion
        self.taskData = taskData

    def __str__(self):
        return "[Task ID: {} || Task Definition: {}]".format(self.taskId, self.taskDefintion)
