# Compound Systems for AI Workloads

## Project Description

Distributed Futures are an extension of traditional RPCs in which a reference to the computed value is returned that may reside on a remote node. We have developed and evaluated a distributed futures system intended for mixed fine-grain and course-grain workloads. Our worker-scheduler pairing can optimize across GPU or CPU simulated workers across different software and hardware generations. System provides a mechanism for clients to track task completion and retrieve results.

The system's performance is measured against multiple matrix operations, map reduce operations and a RAG-LLM (Retrieval-Augmented Generation Large Language Model) application leveraging shared memory for reuse, drawing inspiration from web application prefetching strategies. 

## Quick Start

### Prerequisites

1. Install `uv` (Python package manager):
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```
   Or visit: https://docs.astral.sh/uv/getting-started/installation/

### Setup

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd compound-systems
   ```

2. Run the setup script:
   ```bash
   ./setup.sh
   ```

### Running the System

The system requires a scheduler and workers to be running. Here are the available commands:

#### Single Commands for Testing and Running

```bash
# Run all tests (requires system to be running, run make test-with-system if its not)
make test

# Start system and run tests automatically
make test-with-system

# Start scheduler (Random mode)
make start-scheduler

# Start 4 workers (2 CPU, 2 GPU)
make start-workers

# Run driver example (requires scheduler and workers to be running)
make start-driver

# Start full system and run driver
make run-all

# Stop all processes
make stop-all

# Show all available commands
make help
```

#### Manual Setup (Alternative)

If you prefer to run components manually:

1. **Start the scheduler** (in one terminal):
   ```bash
   make start-scheduler
   ```

2. **Start workers** (in separate terminals):
   ```bash
   make start-workers
   ```

3. **Run the driver** (in another terminal):
   ```bash
   make start-driver
   ```

### Development

```bash
# Install dependencies
make install

# Compile protobuf files
make proto

# Run linting
make lint

# Clean generated files
make clean
```

## System Architecture

### Components

- **Scheduler**: Central coordinator that manages task distribution and worker registration
- **Workers**: Execution nodes that can be CPU or GPU enabled
- **Clients**: Interface for submitting tasks and retrieving results
- **Futures**: References to computed values that may reside on remote nodes

### Scheduling Algorithms

The system supports 4 scheduling modes:
- `Random`: Random worker selection
- `RoundRobin`: Round-robin worker distribution
- `LoadAware`: Load-aware scheduling based on worker capacity
- `PowerOf2`: Power-of-2 choices for load balancing

### Supported Operations

#### Matrix Operations
- `dot_product`: Matrix dot product
- `mat_add`: Matrix addition  
- `mat_subtract`: Matrix subtraction

#### AI/ML Operations
- `retrieval`: Similarity-based retrieval (dot product with cosine similarity)
- `generation`: Text generation operations

#### Utility Operations
- `print_char_count`: Character counting
- `sum_of_integers`: Integer summation

## Testing

The system includes comprehensive tests for:
- Matrix operations
- Map-reduce operations
- RAG-LLM applications
- Fault tolerance scenarios
- Future-based task chaining

**Important**: The tests require the scheduler and workers to be running. Use one of these commands:

```bash
# Option 1: Start system and run tests automatically
make test-with-system

# Option 2: Start system manually, then run tests
make start-scheduler  # in one terminal
make start-workers    # in another terminal
make test            # in a third terminal
```

## CI/CD Pipeline

The system includes a GitHub Actions workflow that runs tests across different scheduling modes. To trigger the workflow:

1. Create a pull request with your changes
2. The workflow will automatically run tests on all supported scheduling modes

## Use Cases

The system is designed for:
- **Matrix operations** (linear algebra)
- **Map-reduce operations** (distributed processing)
- **RAG-LLM applications** (retrieval-augmented generation)
- **Mixed AI workloads** (CPU/GPU optimization)

## Troubleshooting

### Common Issues

1. **Port already in use**: Stop existing processes with `make stop-all`
2. **Module not found**: Ensure you're using `uv run` or the virtual environment
3. **Protobuf errors**: Run `make proto` to regenerate protobuf files
4. **Tests failing**: Make sure scheduler and workers are running before running tests

### Environment Setup

The project uses `uv` for dependency management and creates a virtual environment automatically. All commands should be run with `uv run` or through the Makefile targets.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests: `make test-with-system`
5. Submit a pull request
