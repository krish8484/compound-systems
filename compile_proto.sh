#!/bin/bash

# Try to use system protoc first, then fall back to grpc_tools.protoc
if command -v protoc &> /dev/null; then
    echo "Using system protoc..."
    protoc -I Protos --python_out=. --grpc_python_out=. Protos/api.proto
else
    echo "System protoc not found, using grpc_tools.protoc..."
    python -m grpc_tools.protoc -I Protos --python_out=. --grpc_python_out=. Protos/api.proto
fi