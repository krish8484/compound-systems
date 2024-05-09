CS244b Course Project

The Distributed Task Execution System is designed to efficiently distribute and execute tasks across multiple worker processes while providing a mechanism for clients to track task completion and retrieve results. This system aims to leverage parallelism and distributed computing to enhance task execution performance.

Steps to Run

1) Install miniconda from https://docs.anaconda.com/free/miniconda/
2) conda create --name cs244b python=3.9
3) conda activate cs244b
4) Trigger driver from one terminal - python3 driver.py (this will start the scheduler as well)
5) Start the worker in another terminal - python3 worker.py
5) Submit tasks with driver, they should be seen getting executed on worker.