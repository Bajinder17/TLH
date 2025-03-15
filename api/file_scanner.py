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
        
        # IMPORTANT: Print headers for debugging
        print(f"Using API key (first 4 chars): {VIRUSTOTAL_API_KEY[:4]}...")
        
        # Check if file has been analyzed before
        response = requests.get(
            f"{VIRUSTOTAL_API_URL}/files/{file_hash}",
            headers=headers,
            timeout=REQUEST_TIMEOUT
        )
        
        # IMPORTANT: Print response status for debugging
        print(f"Initial VirusTotal file hash check response status: {response.status_code}")
        
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
        try:
            upload_url_response = requests.get(
                f"{VIRUSTOTAL_API_URL}/files/upload_url",
                headers=headers,
                timeout=REQUEST_TIMEOUT
            )
            
            print(f"Upload URL response status: {upload_url_response.status_code}")
            
            if upload_url_response.status_code != 200:
                print(f"Failed to get upload URL: {upload_url_response.text}")
                raise Exception(f"Failed to get upload URL: {upload_url_response.text}")
            
            upload_url = upload_url_response.json().get('data')
            
            if not upload_url:
                print("No upload URL returned")
                raise Exception("No upload URL returned")
                
            print(f"Got upload URL: {upload_url[:30]}...")
            
            # Upload file
            with open(file_path, 'rb') as file_to_upload:
                files = {'file': (os.path.basename(file_path), file_to_upload)}
                upload_response = requests.post(
                    upload_url,
                    headers=headers,
                    files=files,
                    timeout=REQUEST_TIMEOUT * 2
                )
                
                print(f"Upload response status: {upload_response.status_code}")
                
                if upload_response.status_code != 200:
                    print(f"Failed to upload file: {upload_response.text}")
                    raise Exception(f"Failed to upload file: {upload_response.text}")
                
                upload_json = upload_response.json()
                analysis_id = upload_json.get('data', {}).get('id')
                
                if not analysis_id:
                    print(f"No analysis ID returned from upload. Response: {upload_json}")
                    raise Exception("No analysis ID returned from upload")
                
                print(f"Analysis ID: {analysis_id}")
                
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
                    
                    print(f"Analysis status response: {analysis_response.status_code}")
                    
                    if analysis_response.status_code != 200:
                        print(f"Failed to get analysis status: {analysis_response.text}")
                        raise Exception(f"Failed to get analysis status: {analysis_response.text}")
                    
                    analysis_json = analysis_response.json()
                    status = analysis_json.get('data', {}).get('attributes', {}).get('status')
                    
                    print(f"Analysis status: {status}")
                    
                    if status == 'completed':
                        print("Analysis completed")
                        result = process_vt_analysis_response(analysis_json)
                        return result
                    
                    if attempt < max_attempts - 1:
                        sleep_time = 5 * (attempt + 1)  # Increase wait time with each attempt
                        print(f"Analysis not complete yet, waiting {sleep_time} seconds...")
                        time.sleep(sleep_time)
                
                # If we reach this point, the analysis is still not complete
                # Try to get file report one more time using the file hash
                print("Analysis taking too long, trying file hash lookup again")
                final_response = requests.get(
                    f"{VIRUSTOTAL_API_URL}/files/{file_hash}",
                    headers=headers,
                    timeout=REQUEST_TIMEOUT
                )
                
                if final_response.status_code == 200:
                    print("File found in VirusTotal database after upload")
                    data = final_response.json()
                    result = process_vt_response(data)
                    return result
                
                # Return partial results
                print("Analysis still incomplete, returning partial results")
                # Use the analysis data we have
                result = {
                    'status': 'pending',
                    'message': 'Analysis is still in progress. Partial results available.',
                    'detections': 'Pending / Pending',
                    'scan_date': int(time.time()),
                    'source': 'VirusTotal (Partial)'
                }
                return result
        except Exception as upload_error:
            print(f"Error during file upload/analysis: {str(upload_error)}")
            traceback.print_exc()
            raise upload_error
            
    except requests.exceptions.Timeout:
        print("VirusTotal API request timed out")
        raise Exception("VirusTotal API request timed out. Please try again later.")
    except Exception as e:
        print(f"Exception in scan_file: {str(e)}")
        traceback.print_exc()
        raise e

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
