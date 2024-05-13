from scheduler import Scheduler

def submit_task(task):
    scheduler.submit_task(task)

# Initialize the scheduler object
scheduler = Scheduler("localhost", 8888)

# Example usage
if __name__ == "__main__":
    while True:
        task = input("Enter a task (or 'q' to quit): ")
        if task.lower() == 'q':
            break
        submit_task(task)
