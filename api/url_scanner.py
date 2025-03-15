import os
import requests
import time
import base64
import urllib.parse
import json
import traceback
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set timeout for API requests
REQUEST_TIMEOUT = 60  # seconds

VIRUSTOTAL_API_KEY = os.environ.get('REACT_APP_VIRUSTOTAL_API_KEY')

def scan_url(url):
    """
    Scan a URL for malicious content using VirusTotal
    
    Args:
        url (str): URL to scan
        
    Returns:
        dict: Scan results
    """
    if not VIRUSTOTAL_API_KEY:
        return {
            'status': 'error',
            'message': 'VirusTotal API key not configured'
        }
    
    try:
        # Use VirusTotal for URL scanning
        return scan_with_virustotal(url)
    except Exception as e:
        print(f"Error in URL scanning: {str(e)}")
        traceback.print_exc()
        return {
            'status': 'error',
            'message': f'Error scanning URL: {str(e)}'
        }

def scan_with_virustotal(url):
    """Scan URL using VirusTotal API"""
    headers = {
        'x-apikey': VIRUSTOTAL_API_KEY
    }
    
    try:
        # URL ID needs to be base64 encoded and URL safe
        url_id = base64.urlsafe_b64encode(url.encode()).decode().strip("=")
        
        # First, check if the URL has already been analyzed
        print(f"Checking if URL has been analyzed before: {url}")
        
        response = requests.get(
            f"https://www.virustotal.com/api/v3/urls/{url_id}",
            headers=headers,
            timeout=REQUEST_TIMEOUT
        )
        
        # If URL exists, return result immediately
        if response.status_code == 200:
            print("URL found in VirusTotal database")
            data = response.json()
            return process_vt_url_response(data)
        
        # If URL doesn't exist, submit it for analysis
        print("URL not found, submitting for analysis")
        
        data = {
            'url': url
        }
        
        submit_response = requests.post(
            'https://www.virustotal.com/api/v3/urls',
            headers=headers,
            data=data,
            timeout=REQUEST_TIMEOUT
        )
        
        if submit_response.status_code != 200:
            raise Exception(f"Failed to submit URL: {submit_response.text}")
        
        # Get the analysis ID
        analysis_id = submit_response.json().get('data', {}).get('id')
        
        if not analysis_id:
            raise Exception("No analysis ID returned from URL submission")
        
        # Check analysis status (up to 3 attempts)
        max_attempts = 3
        
        for attempt in range(max_attempts):
            print(f"Checking analysis status (attempt {attempt+1}/{max_attempts})")
            
            analysis_response = requests.get(
                f"https://www.virustotal.com/api/v3/analyses/{analysis_id}",
                headers=headers,
                timeout=REQUEST_TIMEOUT
            )
            
            if analysis_response.status_code != 200:
                raise Exception(f"Failed to get analysis status: {analysis_response.text}")
            
            status = analysis_response.json().get('data', {}).get('attributes', {}).get('status')
            
            if status == 'completed':
                print("Analysis completed")
                return process_vt_analysis_response(analysis_response.json())
            
            if attempt < max_attempts - 1:
                print(f"Analysis not complete yet (status: {status}), waiting 5 seconds...")
                time.sleep(5)
        
        # Return partial results
        print("Analysis taking too long, returning partial results")
        return {
            'status': 'pending',
            'message': 'Analysis is still in progress. Please check back later.',
            'source': 'VirusTotal'
        }
            
    except requests.exceptions.Timeout:
        print("VirusTotal API request timed out")
        return {
            'status': 'error',
            'message': 'VirusTotal API request timed out. Please try again later.'
        }
    except Exception as e:
        print(f"Error in VirusTotal URL scan: {str(e)}")
        traceback.print_exc()
        return {
            'status': 'error',
            'message': f'Error scanning URL: {str(e)}'
        }

def process_vt_url_response(data):
    """Process VirusTotal URL scan response"""
    try:
        print("Processing VT URL response")
        
        # Check if the data structure contains what we need
        if not data or 'data' not in data:
            print(f"Invalid data structure: {data}")
            return {
                'status': 'error',
                'message': 'Invalid response format from VirusTotal'
            }
            
        # Handle URL response format
        attributes = data.get('data', {}).get('attributes', {})
        stats = attributes.get('last_analysis_stats', {})
        
        if not stats:
            print(f"Missing stats in response: {data}")
            return {
                'status': 'error',
                'message': 'Missing analysis stats in VirusTotal response'
            }
            
        # Calculate totals
        total_engines = sum(stats.values())
        malicious = stats.get('malicious', 0)
        suspicious = stats.get('suspicious', 0)
        
        # Determine status based on detections
        if malicious == 0 and suspicious == 0:
            status = 'safe'
        elif malicious > 0:
            status = 'malicious'
        else:
            status = 'suspicious'
        
        # Get categories if available
        categories = []
        if 'categories' in attributes:
            categories = list(attributes['categories'].values())
        
        scan_date = attributes.get('last_analysis_date', int(time.time()))
            
        return {
            'status': status,
            'detections': f"{malicious + suspicious} / {total_engines}",
            'engines': {
                'total': total_engines,
                'malicious': malicious,
                'suspicious': suspicious
            },
            'categories': categories,
            'scan_date': scan_date,
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
    """Process VirusTotal analysis response"""
    try:
        attributes = data.get('data', {}).get('attributes', {})
        stats = attributes.get('stats', {})
        
        if not stats:
            print(f"Missing stats in analysis response: {data}")
            return {
                'status': 'error',
                'message': 'Missing analysis stats in VirusTotal response'
            }
        
        # Calculate totals
        total_engines = sum(stats.values())
        malicious = stats.get('malicious', 0)
        suspicious = stats.get('suspicious', 0)
        
        # Determine status based on detections
        if malicious == 0 and suspicious == 0:
            status = 'safe'
        elif malicious > 0:
            status = 'malicious'
        else:
            status = 'suspicious'
        
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
