import os
import requests
import time
import json
import traceback
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set longer timeout for API requests
REQUEST_TIMEOUT = 60  # seconds

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
    # Check for API key in environment variable
    if not VIRUSTOTAL_API_KEY:
        print("VirusTotal API key not found, using mock scanner")
        from mock_scanner import mock_file_scan
        return mock_file_scan(file_path, file_hash)
    
    # First check if file has been analyzed before by hash
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
            
        # Handle rate limiting - if we're rate limited, use mock data
        if response.status_code == 429:
            print("VirusTotal API rate limit exceeded, using mock data")
            from mock_scanner import mock_file_scan
            return mock_file_scan(file_path, file_hash)
        
        # If file doesn't exist, upload it for analysis
        print("File not found in VirusTotal database, uploading for analysis")
        
        # Check file size - VirusTotal has upload limits
        file_size = os.path.getsize(file_path)
        if file_size > 32 * 1024 * 1024:  # 32 MB limit
            print("File too large for VirusTotal API, using mock data")
            from mock_scanner import mock_file_scan
            return mock_file_scan(file_path, file_hash)
        
        # Get upload URL
        upload_url_response = requests.get(
            f"{VIRUSTOTAL_API_URL}/files/upload_url",
            headers=headers,
            timeout=REQUEST_TIMEOUT
        )
        
        if upload_url_response.status_code != 200:
            print(f"Failed to get upload URL, using mock data. Error: {upload_url_response.text}")
            from mock_scanner import mock_file_scan
            return mock_file_scan(file_path, file_hash)
        
        upload_url = upload_url_response.json().get('data')
        
        # Upload file
        files = {'file': (os.path.basename(file_path), open(file_path, 'rb'))}
        upload_response = requests.post(
            upload_url,
            headers=headers,
            files=files,
            timeout=REQUEST_TIMEOUT * 2
        )
        
        if upload_response.status_code != 200:
            print(f"Failed to upload file, using mock data. Error: {upload_response.text}")
            from mock_scanner import mock_file_scan
            return mock_file_scan(file_path, file_hash)
        
        analysis_id = upload_response.json().get('data', {}).get('id')
        
        if not analysis_id:
            print("No analysis ID returned from upload, using mock data")
            from mock_scanner import mock_file_scan
            return mock_file_scan(file_path, file_hash)
        
        # Wait for analysis to complete (max 3 attempts)
        max_attempts = 3
        for attempt in range(max_attempts):
            print(f"Checking analysis status (attempt {attempt+1}/{max_attempts})")
            
            # Check analysis status
            analysis_response = requests.get(
                f"{VIRUSTOTAL_API_URL}/analyses/{analysis_id}",
                headers=headers,
                timeout=REQUEST_TIMEOUT
            )
            
            if analysis_response.status_code != 200:
                print(f"Failed to get analysis status, using mock data. Error: {analysis_response.text}")
                from mock_scanner import mock_file_scan
                return mock_file_scan(file_path, file_hash)
            
            status = analysis_response.json().get('data', {}).get('attributes', {}).get('status')
            
            if status == 'completed':
                print("Analysis completed")
                result = process_vt_analysis_response(analysis_response.json())
                return result
            
            if attempt < max_attempts - 1:
                print(f"Analysis not complete yet (status: {status}), waiting before retrying...")
                time.sleep(10)  # Wait 10 seconds before checking again
        
        # Return mock results if complete analysis isn't available
        print("Analysis taking too long, using mock data")
        from mock_scanner import mock_file_scan
        return mock_file_scan(file_path, file_hash)
            
    except requests.exceptions.Timeout:
        print("VirusTotal API request timed out, using mock data")
        from mock_scanner import mock_file_scan
        return mock_file_scan(file_path, file_hash)
    except Exception as e:
        print(f"Exception in scan_file: {str(e)}")
        traceback.print_exc()
        # If anything goes wrong, fall back to mock scanner
        from mock_scanner import mock_file_scan
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

def process_vt_analysis_response(data):
    """Process VirusTotal analysis response data"""
    try:
        print("Processing VirusTotal analysis response")
        
        if not isinstance(data, dict) or 'data' not in data:
            print(f"Invalid response format: {data}")
            return {
                'status': 'error',
                'message': 'Invalid response format from VirusTotal'
            }
        
        attributes = data['data']['attributes']
        
        stats = attributes.get('stats', {})
        
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
        
        print(f"Analysis result: {status} (Malicious: {malicious}, Suspicious: {suspicious}, Total: {total_engines})")
            
        return {
            'status': status,
            'detections': f"{malicious + suspicious} / {total_engines}",
            'engines': {
                'total': total_engines,
                'malicious': malicious,
                'suspicious': suspicious
            },
            'scan_date': int(time.time()),
            'source': 'VirusTotal'
        }
        
    except Exception as e:
        print(f"Error processing analysis results: {str(e)}")
        traceback.print_exc()
        return {
            'status': 'error',
            'message': f'Error processing analysis results: {str(e)}'
        }
