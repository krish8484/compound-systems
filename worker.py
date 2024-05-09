import signal
import sys
import socket

class Worker:
    def __init__(self, scheduler_host, scheduler_port):
        self.scheduler_host = scheduler_host
        self.scheduler_port = scheduler_port
        signal.signal(signal.SIGINT, self.sigterm_handler)

    def start_client(self):
        worker_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        worker_socket.connect((self.scheduler_host, self.scheduler_port))
        print("Worker connected to Scheduler.")
        while True:
            task = self.get_task(worker_socket)
            if task:
                self.execute_task(task)
                self.notify_task_completion(task)

    def get_task(self, worker_socket):
        return worker_socket.recv(1024).decode()

    def execute_task(self, task):
        print(f"executing task {task}")
        pass

    def notify_task_completion(self, task):
        pass

    def sigterm_handler(self, signum, frame):
        print("Exiting gracefully.")
        sys.exit(0)

# Example usage
if __name__ == "__main__":
    worker = Worker("localhost", 8888)
    worker.start_client()
