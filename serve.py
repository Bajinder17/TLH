import os
import sys
import subprocess
from dotenv import load_dotenv

def main():
    """Start the application with proper environment variables"""
    # Load environment variables from .env file
    load_dotenv()
    
    print("Starting ThreatLightHouse application...")
    
    # Check required environment variables
    if not os.environ.get('REACT_APP_VIRUSTOTAL_API_KEY'):
        print("WARNING: VirusTotal API key not set. File and URL scanning will not work.")
    
    if not os.environ.get('REACT_APP_SUPABASE_URL') or not os.environ.get('REACT_APP_SUPABASE_ANON_KEY'):
        print("WARNING: Supabase credentials not set. Report storage will use local files.")
    
    # Start the API server
    api_process = subprocess.Popen([sys.executable, "api/index.py"])
    print("API server started on http://localhost:5000")
    
    try:
        # After API server is up, start React dev server
        subprocess.run(["npm", "start"], check=True)
    finally:
        # When React server stops, terminate API server
        api_process.terminate()
        print("API server stopped")

if __name__ == "__main__":
    main()
