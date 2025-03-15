import os
import sys

# Set environment variable to indicate we're in Vercel
os.environ['VERCEL'] = '1'

# Ensure the current directory is in the Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

# Import the Flask app
from index import app

# This entry point is used by Vercel
handler = app
