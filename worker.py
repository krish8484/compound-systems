import signal
import sys
import socket
import os

class Worker:
    def __init__(self,
        scheduler_host,
        scheduler_port,
        worker_host,
        worker_port):
            self.scheduler_host = scheduler_host
            self.scheduler_port = scheduler_port
            self.worker_host = worker_host
            self.worker_port = worker_port
            self.is_task_executing = False;
            self.executing_task = None
            signal.signal(signal.SIGINT, self.sigterm_handler)

    def start_client_listener(self):
        worker_listener_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        worker_listener_socket.bind((self.worker_host, self.worker_port))
        worker_listener_socket.listen(5) # this number can be #scheduler + #workers

        print("Worker is listening. Host: {0} Port: {1}".format(self.worker_host, self.worker_port)

        incoming_socket, addr = worker_listener_socket.accept()
        with incoming_socket:
            print("Connected by {0}".format(addr))
            while True:
                data = incoming_socket.recv(8)
                # Expect first byte from scheduler/worker to be an identifier
                if not data:
                    break
                if data == "Scheduler":
                    # For scheduler, check if already executing task:
                    if self.is_task_executing:
                        # send error - can't perform the task
                        # incoming_socket.sendall()
                    else:
                        # send that task is being now performed by this task
                        self.is_task_executing = True
                        fileName = self.create_task();
                        returning_data = os.getpid() + "_" + fileName
                        incoming_socket.sendall(returning_data)

                if data == "Worker":
                    self.return_computation();
                    # For worker, check if task is finished
                    # if yes, return the variable/file
                    # if not, return empty/error response
                    incoming_socket.sendall(data)
    pass
                

    def register_worker(self):
        try:
            worker_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            worker_socket.connect((self.scheduler_host, self.scheduler_port))
            print("Worker connected to Scheduler.")
            
            # Send the PID of the worker process to the schduler to register itself
            worker_socket.sendall(os.getpid())

            # Expect the scheduler to send back a success message
            # We can expect scheduler to send an identifier
            data = worker_socket.recv(1024)
            print("Registered the worker successfully. Received {data} from the scheduler.")
        except socket.error:
            print("Error Received")
            raise
        finally:
            worker_socket.close();


    def get_task(self, worker_socket):
        return worker_socket.recv(1024).decode()

    def execute_task(self, task):
        print(f"executing task {task}")
        # once task finishes, set the class variable self.is_task_executing
        self.is_task_executing = True
        pass

    def create_task(self, task):
        print(f"executing task {task}")
        # once task finishes, set the class variable self.is_task_executing
        self.is_task_executing = True
        fileName = "resultFile.txt"
        fileObject = open(fileName, "a")
        fileObject.close()
        self.execute_task = task;

        # Here we should trigger execute task in fire and forget manner.
        return fileName;
        pass

    def notify_task_completion(self, task):
        pass

    def sigterm_handler(self, signum, frame):
        print("Exiting gracefully.")
        sys.exit(0)

# Example usage
if __name__ == "__main__":
    worker = Worker("localhost", 8888)

    try:
        # Register the worker and if it fails throw/end the process
        worker.register_worker()
    except:
        print("Could not register the worker. Will end the process.")
        raise
    
    try:
        # Start a listener where the worker can receive the task from scheduler and other workers
        worker.start_client_listener()
    except:
        print("Received exception while listening. Will end the process.")
        raise
