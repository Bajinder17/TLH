#!/bin/bash

# Print current directory contents
echo "Current directory: $(pwd)"
echo "Directory contents: $(ls -la)"

# Install frontend dependencies and build
echo "Installing frontend dependencies..."
npm install

echo "Building React app..."
npm run build

# Create necessary directories for API
mkdir -p api/reports

echo "Build process completed!"
exit 0
