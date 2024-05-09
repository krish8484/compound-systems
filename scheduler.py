import threading
import queue
import signal
import sys
import socket

class Scheduler:
    def __init__(self, host, port):
        self.task_queue = queue.Queue()
        self.completion_status = {}
        self.lock = threading.Lock()
        self.host = host
        self.port = port
        signal.signal(signal.SIGINT, self.sigterm_handler)
        threading.Thread(target=self.start_server, daemon=True).start()

    def submit_task(self, task):
        with self.lock:
            self.task_queue.put(task)
            self.completion_status[task] = False
        print("Task submitted to scheduler:", task)

    def assign_task(self):
        with self.lock:
            if not self.task_queue.empty():
                return self.task_queue.get()
            else:
                return None

    def get_task_completion(self, task):
        pass

    def start_server(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((self.host, self.port))
        server_socket.listen(5)
        print("Scheduler listening on {}:{}".format(self.host, self.port))
        while True:
            client_socket, addr = server_socket.accept()
            print("Worker connected from:", addr)
            threading.Thread(target=self.handle_worker, args=(client_socket,), daemon=True).start()

    def handle_worker(self, client_socket):
        while True:
            task = self.assign_task()
            if task:
                client_socket.send(task.encode())
                self.get_task_completion(task)
        client_socket.close()

    def sigterm_handler(self, signum, frame):
        print("Exiting gracefully.")
        sys.exit(0)
