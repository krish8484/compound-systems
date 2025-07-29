#!/bin/bash

# Compound Systems Setup Script

echo "Setting up Compound Systems..."

# Check if uv is installed
if ! command -v uv &> /dev/null; then
    echo "ERROR: uv is not installed. Please install it first:"
    echo "   curl -LsSf https://astral.sh/uv/install.sh | sh"
    echo "   or visit: https://docs.astral.sh/uv/getting-started/installation/"
    exit 1
fi

echo "uv is installed"

# Install dependencies
echo "Installing dependencies..."
uv sync

# Compile protobuf (only if files don't exist)
if [ ! -f "api_pb2.py" ] || [ ! -f "api_pb2_grpc.py" ]; then
    echo "Compiling protobuf files..."
    # Try to use system protoc if available
    if command -v protoc &> /dev/null; then
        protoc -I Protos --python_out=. --grpc_python_out=. Protos/api.proto 2>/dev/null || echo "Warning: Could not compile protobuf files. Using existing files if available."
    else
        echo "Warning: protoc not found, trying grpc_tools.protoc..."
        uv run python -m grpc_tools.protoc -I Protos --python_out=. --grpc_python_out=. Protos/api.proto 2>/dev/null || echo "Warning: Could not compile protobuf files. Using existing files if available."
    fi
else
    echo "Protobuf files already exist, skipping compilation."
fi

echo "Setup complete!"
echo ""
echo "Quick start commands:"
echo "   make test          - Run all tests"
echo "   make run-all       - Start full system and run driver"
echo "   make help          - Show all available commands"
echo ""
echo "For more information, see README.md" 