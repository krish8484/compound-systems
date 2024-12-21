# Compound Systems for AI Workloads

## Project Description

Distributed Futures are an extension of traditional RPCs in which a reference to the computed value is returned that may reside on a remote node. We have developed and evaluated a distributed futures system intended for mixed fine-grain and course-grain workloads. Our worker-scheduler pairing can optimize across GPU or CPU simulated workers across different software and hardware generations. System provides a mechanism for clients to track task completion and retrieve results.

The system's performance is measured against multiple matrix operations, map reduce operations and a RAG-LLM (Retrieval-Augmented Generation Large Language Model) application leveraging shared memory for reuse, drawing inspiration from web application prefetching strategies. 

## Steps to run experiments (using CI pipeline)

Run the github workflow in `.github/workflows/python-package-conda.yml` using the following command:
``` 
gh workflow run
```

In case of any errors with gh, you may also run the individual commands in the `python-package-conda.yml` file.

## Steps to run expirements (using Driver)

We need to start the scheduler and workers in different terminals. 
Make sure to start atleast one GPU and one CPU enabled worker. This ensures that all types of workloads can be run. Once scheduler and workers are up, run the tests in the tests directory with pytest.

Following steps go over the starting the scheduler in PowerOf2 mode and start 4 workers (2 of them with GPU). 

1) Install miniconda from https://docs.anaconda.com/free/miniconda/

2) Create a conda environment for the experiments
```
conda create --name comp-sys --file requirements.txt python=3.9
```

3) Activate the conda package and environment manager:
```
conda activate comp-sys
```

4) Run compile_proto script from root repo folder [compound-systems](https://github.com/krish8484/compound-systems) which generates the necessary gRPC proto files. The script depends on your target machine. 

For UNIX based machines, run:
```
./compile_proto.sh
```

For Windows OS machine, run:
```
compile_proto.cmd
```

5) Start the scheduler server from a terminal -
```
cd Scheduler;
python3 scheduler_server.py --PortNumber 50051 --SchedulerMode PowerOf2
```
Reference Command:
`python3 scheduler_server.py --PortNumber <PortNumber> --SchedulerMode <SchedulingMode> --AssingedWorkersPerTask <AssignedWorkersPerTask>`

- First parameter is the port number. Type `int`.
- Second parameter is the scheduling algorithm that would be used for request routing in the scheduler. Type `string`. It supports 4 modes `Random`, `RoundRobin`, `LoadAware` and `PowerOf2`
- Third parameter is an optional parameter representing the number of workers a single task would assigned.  Type `int`. This Task Replication Strategy helps up retrieve a task computation from another worker when one of them is down.

6) Start multiple worker servers in different terminals - 
`Worker1`
```
cd Worker;
python3 worker_server.py --PortNumber 50052 --MaxThreadCount 2 --HardwareGeneration Gen2
```

`Worker2`
```
cd Worker;
python3 worker_server.py --PortNumber 50053 --MaxThreadCount 2 --HardwareGeneration Gen2
```

`Worker3`
```
cd Worker;
python3 worker_server.py --PortNumber 50054 --MaxThreadCount 2 --HardwareGeneration Gen2 --gpuEnabled
```

`Worker4`
```
cd Worker;
python3 worker_server.py --PortNumber 50055 --MaxThreadCount 2 --HardwareGeneration Gen2 --gpuEnabled
```

Reference Command:
`python3 worker_server.py --PortNumber <PortNumber> --MaxThreadCount <MaxThreadCount> --HardwareGeneration <HardwareGeneration>`

- First parameter is the port number. Type `int`.
- Second parameter is the number of threads the worker can process. Type `int`.
- Third parameter is the hardware generation parameter. Type `string`. It supports 4 values `Gen1`, `Gen2`, `Gen3` and `Gen4`. Scheduler uses this information in `LoadAware` and `PowerOf2` scheduling modes to determine the number of requests worker can handle.
- Fourth parameter is an optional parameter. If --gpuEnabled parameter is passed, worker is treated as GPU Enabled.
- Fifth parameter is an optional parameter. If --addDelay parameter is passed, delays are added randomly for the worker operations.

7) Run driver for another terminal - 
```
cd Driver;
python3 driver.py
```
Driver code runs all the supported operations in the system with predefined inputs.

`Driver can be expanded to modify inputs to run any supported operations `

As soon as you start the driver, the tasks would start getting executed and would be visible in terminal logs.
