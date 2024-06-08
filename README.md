# CS244b Course Project

# Getting Started

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

Details:

1) Install miniconda from https://docs.anaconda.com/free/miniconda/
2) Create a conda environment for the experiments
```
conda create --name cs244b --file requirements.txt python=3.9
```

3) Activate the conda package and environment manager:
```
conda activate cs244b
```

4) Run compile_proto script from root repo folder [CS244B](https://github.com/krish8484/cs244b) which generates the necessary gRPC proto files. The script depends on your target machine. For UNIX based machines, run:
```
./compile_proto.sh
```
5) Start the scheduler server from one terminal - 
    python3 scheduler_server.py --PortNumber 50051 --SchedulerMode Random
6) Start multiple worker servers in another terminal - python3 worker_server.py --PortNumber <PortNumber> --MaxThreadCount <MaxThreadCount> --HardwareGeneration <HardwareGeneration>
    Example Command:
    python3 worker_server.py --PortNumber 50055 --MaxThreadCount 2 --HardwareGeneration Gen2 --gpuEnabled

    First parameter is the port number
    Second parameter is the number of threads the worker can process
    Third parameter is the hardware generation parameter which determines if scheduler would send more requests to this worker in LoadAware scheduling mode
    Fourth parameter is an optional parameter. If --gpuEnabled parameter is passed, worker is treated as GPU Enabled.
    Fifth parameter is an optional parameter. If --addDelay parameter is passed, delays are added randomly for the worker operations.

7) Run driver for another terminal - python3 driver.py (There is an example code written under main for testing)
8) Submit tasks with the driver; they should be seen getting executed on the worker.
