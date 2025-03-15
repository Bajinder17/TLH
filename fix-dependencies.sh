#!/bin/bash

echo "Fixing node dependencies..."

# Remove node_modules and package-lock.json
rm -rf node_modules
rm -f package-lock.json

# Clear npm cache
npm cache clean --force

# Reinstall dependencies
npm install

echo "Dependencies reinstalled successfully!"
