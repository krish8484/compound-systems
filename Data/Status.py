class Status:
    
    def __init__(self, status):
        self.success = status

    def __str__(self):
        return "[Status success : {}]".format(self.success)