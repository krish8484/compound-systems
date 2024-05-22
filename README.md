CS244b Course Project

The Distributed Task Execution System is designed to efficiently distribute and execute tasks across multiple worker processes while providing a mechanism for clients to track task completion and retrieve results. This system aims to leverage parallelism and distributed computing to enhance task execution performance.

A set of capability extensions will be pursued from the base implementation to process across multiple machines with simplified scheduling, introduce a global scheduler for efficient resource allocation, and integrate shared memory mechanisms to facilitate seamless data sharing among distributed components. 

Subsequent versions will implement a specific distributed system for a RAG-LLM (Retrieval-Augmented Generation Large Language Model) application leveraging shared memory for reuse, drawing inspiration from web application prefetching strategies. 

Steps to Run

1) Install miniconda from https://docs.anaconda.com/free/miniconda/
2) conda create --name cs244b --file requirements.txt python=3.9
3) conda activate cs244b
4) Run compile_proto script based on your target machine from root repo folder (CS244B)
5) Start the scheduler server from one terminal - python3 scheduler_server.py
6) Start the worker server in another terminal - python3 worker_server.py <PortNumber>
    Example Command: python3 worker_server.py 50054
    Example Command: python3 worker_server.py 50054 --addDelay

    If --addDelay parameter is passed, delays are added randomly for the worker operations.

7) Run driver for another terminal - python3 driver.py (There is an example code written under main for testing)
8) Submit tasks with the driver; they should be seen getting executed on the worker.
