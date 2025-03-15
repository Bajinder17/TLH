import os
import json
import time
import uuid
from datetime import datetime
import hashlib
from dotenv import load_dotenv
from supabase import create_client, Client

# Load environment variables
load_dotenv()

# Initialize Supabase client
supabase_url = os.environ.get('REACT_APP_SUPABASE_URL')
supabase_key = os.environ.get('REACT_APP_SUPABASE_ANON_KEY')

# Use local JSON file if Supabase isn't configured
REPORTS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'reports')
if not os.path.exists(REPORTS_DIR):
    os.makedirs(REPORTS_DIR)

def generate_report(scan_type, scan_data):
    """
    Generate a report for a scan
    
    Args:
        scan_type (str): Type of scan ('file', 'url', or 'port')
        scan_data (dict): Scan data
        
    Returns:
        str: ID of the generated report
    """
    # Generate a unique ID for the report
    report_id = str(uuid.uuid4())
    
    # Create report data
    report = {
        'id': report_id,
        'scan_type': scan_type,
        'scan_data': scan_data,
        'created_at': datetime.now().isoformat()
    }
    
    try:
        # Try to save to Supabase
        if supabase_url and supabase_key:
            supabase = create_client(supabase_url, supabase_key)
            
            # Insert report data
            response = supabase.table('reports').insert(report).execute()
            
            # Check for errors
            if hasattr(response, 'error') and response.error:
                raise Exception(f"Supabase error: {response.error}")
                
            return report_id
    except Exception as e:
        # Fall back to local storage if Supabase fails
        print(f"Warning: Failed to save report to Supabase: {e}")
    
    # Fall back to local JSON file
    report_path = os.path.join(REPORTS_DIR, f"{report_id}.json")
    
    with open(report_path, 'w') as f:
        json.dump(report, f, indent=2)
        
    return report_id

def get_report(report_id):
    """
    Get a report by ID
    
    Args:
        report_id (str): ID of the report
        
    Returns:
        dict: Report data or None if not found
    """
    try:
        # Try to get from Supabase
        if supabase_url and supabase_key:
            supabase = create_client(supabase_url, supabase_key)
            
            # Query report data
            response = supabase.table('reports').select('*').eq('id', report_id).execute()
            
            # Check for errors
            if hasattr(response, 'error') and response.error:
                raise Exception(f"Supabase error: {response.error}")
                
            if hasattr(response, 'data') and response.data and len(response.data) > 0:
                return response.data[0]
    except Exception as e:
        # Fall back to local storage if Supabase fails
        print(f"Warning: Failed to get report from Supabase: {e}")
    
    # Fall back to local JSON file
    report_path = os.path.join(REPORTS_DIR, f"{report_id}.json")
    
    if os.path.exists(report_path):
        with open(report_path, 'r') as f:
            return json.load(f)
            
    return None

def get_all_reports():
    """
    Get all reports
    
    Returns:
        list: List of report data
    """
    try:
        # Try to get from Supabase
        if supabase_url and supabase_key:
            supabase = create_client(supabase_url, supabase_key)
            
            # Query report data
            response = supabase.table('reports').select('*').order('created_at', desc=True).execute()
            
            # Check for errors
            if hasattr(response, 'error') and response.error:
                raise Exception(f"Supabase error: {response.error}")
                
            if hasattr(response, 'data') and response.data:
                return response.data
    except Exception as e:
        # Fall back to local storage if Supabase fails
        print(f"Warning: Failed to get reports from Supabase: {e}")
    
    # Fall back to local JSON files
    reports = []
    
    if os.path.exists(REPORTS_DIR):
        for filename in os.listdir(REPORTS_DIR):
            if filename.endswith('.json'):
                report_path = os.path.join(REPORTS_DIR, filename)
                with open(report_path, 'r') as f:
                    reports.append(json.load(f))
                    
    # Sort by created_at in descending order
    reports.sort(key=lambda x: x.get('created_at', ''), reverse=True)
    
    return reports
