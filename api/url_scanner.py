import os
import requests
import time
import base64
import urllib.parse
from dotenv import load_dotenv
from mock_scanner import mock_url_scan

# Load environment variables
load_dotenv()

# Set shorter timeout for API requests
REQUEST_TIMEOUT = 20  # seconds

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
        print("VirusTotal API key not configured, using mock scanner")
        return mock_url_scan(url)
    
    try:
        # Use VirusTotal for URL scanning with timeout
        vt_result = scan_with_virustotal(url)
        return vt_result
    except requests.exceptions.Timeout:
        print("VirusTotal API request timed out")
        return mock_url_scan(url)
    except Exception as e:
        print(f"Error in URL scanning: {str(e)}")
        return mock_url_scan(url)

def scan_with_virustotal(url):
    """Scan URL using VirusTotal API"""
    if not VIRUSTOTAL_API_KEY:
        return {
            'status': 'error',
            'message': 'VirusTotal API key is not configured'
        }
    
    headers = {
        'x-apikey': VIRUSTOTAL_API_KEY
    }
    
    try:
        # URL ID needs to be base64 encoded and URL safe
        url_id = base64.urlsafe_b64encode(url.encode()).decode().strip("=")
        
        # Check if URL has been scanned before - this is fast
        response = requests.get(
            f"https://www.virustotal.com/api/v3/urls/{url_id}",
            headers=headers,
            timeout=REQUEST_TIMEOUT
        )
        
        # If URL exists in VT database, return result immediately
        if response.status_code == 200:
            data = response.json()
            return process_vt_url_response(data)
        
        # For new URLs, use mock scanner to avoid timeout
        # This gives immediate feedback to the user
        print("URL not found in VirusTotal database, using mock scanner for immediate results")
        return mock_url_scan(url)
            
    except requests.exceptions.Timeout:
        print("VirusTotal API request timed out")
        return mock_url_scan(url)
    except Exception as e:
        print(f"Error in VirusTotal URL scan: {str(e)}")
        return mock_url_scan(url)

def process_vt_url_response(data):
    """Process VirusTotal URL scan response"""
    try:
        print(f"Processing VT response data")
        
        # Check if the data structure contains what we need
        if not data or 'data' not in data:
            print(f"Invalid data structure: {data}")
            return {
                'status': 'error',
                'message': 'Invalid response format from VirusTotal (missing data)'
            }
            
        # Handle analysis response format
        if data.get('data', {}).get('type') == 'analysis':
            print("Processing analysis data format")
            # For analysis results, the path is different
            attributes = data.get('data', {}).get('attributes', {})
            stats = attributes.get('stats', {})
            
            # Get the actual last_analysis_stats when available
            results = attributes.get('results', {})
            if not stats and 'last_analysis_stats' in results:
                stats = results.get('last_analysis_stats', {})
        
        # Handle URL response format
        elif data.get('data', {}).get('type') == 'url':
            print("Processing URL data format")
            attributes = data.get('data', {}).get('attributes', {})
            stats = attributes.get('last_analysis_stats', {})
        else:
            print(f"Unknown data type: {data.get('data', {}).get('type')}")
            return {
                'status': 'error',
                'message': 'Unknown response data type from VirusTotal'
            }
        
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
        return {
            'status': 'error',
            'message': f'Error processing scan results: {str(e)}'
        }
