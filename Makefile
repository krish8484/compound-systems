.PHONY: setup install proto test test-with-system lint clean start-scheduler start-workers start-driver run-all stop-all help

# Default target
help:
	@echo "Compound Systems - Available commands:"
	@echo "  setup        - Install dependencies and compile protobuf"
	@echo "  install      - Install dependencies using uv"
	@echo "  proto        - Compile protobuf files"
	@echo "  test         - Run all tests (requires system to be running)"
	@echo "  test-with-system - Start system and run tests"
	@echo "  lint         - Run flake8 linting"
	@echo "  clean        - Clean generated files"
	@echo "  start-scheduler - Start scheduler server (Random mode)"
	@echo "  start-workers   - Start 4 workers (2 CPU, 2 GPU)"
	@echo "  start-driver    - Run the driver example"
	@echo "  run-all      - Start scheduler, workers, and run driver"
	@echo "  stop-all     - Stop all running processes"

# Install dependencies
install:
	uv sync

# Setup everything
setup: install proto

# Compile protobuf files
proto:
	@if [ ! -f "api_pb2.py" ] || [ ! -f "api_pb2_grpc.py" ]; then \
		echo "Compiling protobuf files..."; \
		if command -v protoc &> /dev/null; then \
			protoc -I Protos --python_out=. --grpc_python_out=. Protos/api.proto 2>/dev/null || echo "Warning: Could not compile protobuf files. Using existing files if available."; \
		else \
			echo "Warning: protoc not found, trying grpc_tools.protoc..."; \
			uv run python -m grpc_tools.protoc -I Protos --python_out=. --grpc_python_out=. Protos/api.proto 2>/dev/null || echo "Warning: Could not compile protobuf files. Using existing files if available."; \
		fi; \
	else \
		echo "Protobuf files already exist, skipping compilation."; \
	fi

# Run tests (requires system to be running)
test:
	uv run pytest

# Run tests with system startup
test-with-system:
	@echo "Starting system for tests..."
	@make start-scheduler &
	@sleep 3
	@make start-workers &
	@sleep 5
	@echo "Running tests..."
	@uv run pytest
	@echo "Stopping system..."
	@make stop-all

# Run linting
lint:
	uv run flake8 .

# Clean generated files
clean:
	rm -f api_pb2.py api_pb2_grpc.py
	rm -rf __pycache__ */__pycache__ */*/__pycache__
	rm -rf .pytest_cache

# Start scheduler
start-scheduler:
	@echo "Starting scheduler on port 50051 (Random mode)..."
	PYTHONPATH=. uv run python Scheduler/scheduler_server.py --PortNumber 50051 --SchedulerMode Random

# Start workers
start-workers:
	@echo "Starting 4 workers..."
	@echo "Worker 1 (CPU) on port 50052..."
	PYTHONPATH=. uv run python Worker/worker_server.py --PortNumber 50052 --MaxThreadCount 2 --HardwareGeneration Gen2 &
	@echo "Worker 2 (CPU) on port 50053..."
	PYTHONPATH=. uv run python Worker/worker_server.py --PortNumber 50053 --MaxThreadCount 2 --HardwareGeneration Gen2 &
	@echo "Worker 3 (GPU) on port 50054..."
	PYTHONPATH=. uv run python Worker/worker_server.py --PortNumber 50054 --MaxThreadCount 2 --HardwareGeneration Gen2 --gpuEnabled &
	@echo "Worker 4 (GPU) on port 50055..."
	PYTHONPATH=. uv run python Worker/worker_server.py --PortNumber 50055 --MaxThreadCount 2 --HardwareGeneration Gen2 --gpuEnabled &
	@echo "Workers started. Waiting 5 seconds for registration..."
	@sleep 5
	@echo "Workers ready!"

# Start driver
start-driver:
	@echo "Running driver example..."
	PYTHONPATH=. uv run python Driver/driver.py

# Run everything
run-all: start-scheduler start-workers
	@echo "System started! Running driver in 3 seconds..."
	@sleep 3
	PYTHONPATH=. uv run python Driver/driver.py

# Stop all processes
stop-all:
	@echo "Stopping all processes..."
	pkill -f scheduler_server.py || true
	pkill -f worker_server.py || true
	@echo "All processes stopped."

# Development helpers
dev-setup: setup
	@echo "Development environment ready!"
	@echo "Run 'make test-with-system' to run tests with system"
	@echo "Run 'make run-all' to start the full system" 