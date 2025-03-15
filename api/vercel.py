import os
import sys
import json

# Print important info for debugging
print("Starting Vercel serverless function")
print(f"Python version: {sys.version}")
print(f"Working directory: {os.getcwd()}")

# List all environment variables (excluding secrets)
env_vars = {k: v[:4] + "..." if k.endswith("KEY") or k.endswith("SECRET") else v 
            for k, v in os.environ.items() 
            if not k.startswith("AWS_") and not k.startswith("VERCEL_")}
print(f"Environment variables: {json.dumps(env_vars, indent=2)}")

# IMPORTANT: Don't set VERCEL=1 to prevent mock scanner from being used
# Instead we'll rely on error handling in individual scanners

# Ensure the current directory is in the Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

try:
    # Import the Flask app
    from index import app
    print("Successfully imported app from index.py")
except Exception as e:
    print(f"Error importing app: {str(e)}")
    raise e

# This entry point is used by Vercel
handler = app
