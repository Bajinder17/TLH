import os
import sys
import json

# Print important info for debugging
print("Starting Vercel serverless function")
print(f"Python version: {sys.version}")
print(f"Working directory: {os.getcwd()}")

# Ensure API key is accessible in Vercel environment
api_key = os.environ.get('REACT_APP_VIRUSTOTAL_API_KEY', '')
if api_key:
    print(f"API key found with length: {len(api_key)}")
else:
    print("WARNING: No API key found in environment")

# Ensure the current directory is in the Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

# Create 'reports' directory if it doesn't exist (for local report storage)
reports_dir = os.path.join(current_dir, 'reports')
if not os.path.exists(reports_dir):
    try:
        os.makedirs(reports_dir)
        print(f"Created reports directory: {reports_dir}")
    except Exception as e:
        print(f"Warning: Could not create reports directory: {e}")

try:
    # Import the Flask app
    from index import app
    print("Successfully imported app from index.py")
except Exception as e:
    print(f"Error importing app: {str(e)}")
    raise e

# This entry point is used by Vercel
handler = app
