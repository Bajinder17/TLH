import os
import sys

# Set up Python path
dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.dirname(dir_path))
sys.path.append(dir_path)

# Debug info
print(f"Python version: {sys.version}")
print(f"Working directory: {os.getcwd()}")
print(f"Directory contents: {os.listdir(dir_path)}")

# Check critical environment variables
vt_api_key = os.environ.get('REACT_APP_VIRUSTOTAL_API_KEY', '')
print(f"API key configured: {'Yes' if vt_api_key else 'No'}")

# Import the Flask app after path setup
try:
    from index import app
    print("Successfully imported Flask app")
except Exception as e:
    print(f"Error importing app: {str(e)}")
    raise e

# This is used by Vercel
handler = app
