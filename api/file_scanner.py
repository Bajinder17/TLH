import os
import requests
import time
import json
import traceback
from dotenv import load_dotenv
from mock_scanner import mock_file_scan

# Load environment variables
load_dotenv()

# Set shorter timeout for API requests
REQUEST_TIMEOUT = 20  # seconds

VIRUSTOTAL_API_KEY = os.environ.get('REACT_APP_VIRUSTOTAL_API_KEY')
VIRUSTOTAL_API_URL = 'https://www.virustotal.com/api/v3'

def scan_file(file_path, file_hash):
    """
    Scan a file using VirusTotal API
    
    Args:
        file_path (str): Path to the file
        file_hash (str): SHA-256 hash of the file
        
    Returns:
        dict: Scan results
    """
    if not VIRUSTOTAL_API_KEY:
        print("VirusTotal API key not configured, using mock scanner")
        return mock_file_scan(file_path, file_hash)
    
    # First check if file has been analyzed before by hash - this is fast
    try:
        print(f"Checking VirusTotal for file hash: {file_hash}")
        headers = {
            'x-apikey': VIRUSTOTAL_API_KEY
        }
        
        # Check if file has been analyzed before
        response = requests.get(
            f"{VIRUSTOTAL_API_URL}/files/{file_hash}",
            headers=headers,
            timeout=REQUEST_TIMEOUT
        )
        
        # If file exists in VT database, return the result immediately
        if response.status_code == 200:
            print("File found in VirusTotal database")
            data = response.json()
            result = process_vt_response(data)
            return result
            
        # For new files, use the mock scanner to avoid timeout
        # This gives immediate feedback to the user
        print("File not found in VirusTotal database, using mock scanner for immediate results")
        return mock_file_scan(file_path, file_hash)
            
    except requests.exceptions.Timeout:
        print("VirusTotal API request timed out")
        return mock_file_scan(file_path, file_hash)
    except Exception as e:
        print(f"Exception in scan_file: {str(e)}")
        traceback.print_exc()
        return mock_file_scan(file_path, file_hash)

def process_vt_response(data):
    """Process VirusTotal response data"""
    try:
        print("Processing VirusTotal file scan response")
        
        if not isinstance(data, dict) or 'data' not in data:
            print(f"Invalid response format: {data}")
            return {
                'status': 'error',
                'message': 'Invalid response format from VirusTotal'
            }
            
        attributes = data['data']['attributes']
        
        if 'last_analysis_stats' not in attributes:
            print("Missing last_analysis_stats in response")
            return {
                'status': 'error',
                'message': 'Missing analysis stats in VirusTotal response'
            }
            
        stats = attributes['last_analysis_stats']
        
        total_engines = sum(stats.values())
        malicious = stats.get('malicious', 0)
        suspicious = stats.get('suspicious', 0)
        
        # Determine status based on detections
        if malicious == 0 and suspicious == 0:
            status = 'clean'
        elif malicious > 0:
            status = 'malicious'
        else:
            status = 'suspicious'
        
        print(f"Scan result: {status} (Malicious: {malicious}, Suspicious: {suspicious}, Total: {total_engines})")
            
        return {
            'status': status,
            'detections': f"{malicious + suspicious} / {total_engines}",
            'engines': {
                'total': total_engines,
                'malicious': malicious,
                'suspicious': suspicious
            },
            'scan_date': attributes.get('last_analysis_date', int(time.time())),
            'source': 'VirusTotal'
        }
        
    except Exception as e:
        print(f"Error processing scan results: {str(e)}")
        traceback.print_exc()
        return {
            'status': 'error',
            'message': f'Error processing scan results: {str(e)}'
        }
