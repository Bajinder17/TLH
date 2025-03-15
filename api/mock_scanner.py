"""
Mock scanner functions for demonstration purposes.
Used when API keys are not configured or when in production environment.
"""
import os
import hashlib
import time
import random
import re
import socket

def mock_file_scan(file_path, file_hash):
    """Generate mock file scan results"""
    
    file_size = os.path.getsize(file_path)
    file_name = os.path.basename(file_path)
    extension = os.path.splitext(file_name)[1].lower()
    
    # Base the result on the file hash to make it consistent
    hash_int = int(file_hash[:8], 16)
    
    # Potentially risky extensions
    risky_extensions = ['.exe', '.dll', '.bat', '.ps1', '.vbs', '.js']
    
    # Determine if file should be classified as malicious
    if extension in risky_extensions and (hash_int % 10 < 3):
        status = 'malicious'
        detections = f"{random.randint(3, 20)} / 68"
        engines = {
            'total': 68,
            'malicious': random.randint(3, 20),
            'suspicious': random.randint(1, 5)
        }
    else:
        status = 'clean'
        detections = "0 / 68"
        engines = {
            'total': 68,
            'malicious': 0,
            'suspicious': 0
        }
    
    return {
        'status': status,
        'detections': detections,
        'engines': engines,
        'scan_date': int(time.time()),
        'source': 'Mock Scanner (Demo)'
    }

def mock_url_scan(url):
    """Generate mock URL scan results"""
    
    # Base the result on the URL to make it consistent
    url_hash = hashlib.md5(url.encode()).hexdigest()
    hash_int = int(url_hash[:8], 16)
    
    # List of potentially malicious domains for demo
    malicious_patterns = ['evil', 'hack', 'malware', 'phish', 'spam', 'virus']
    suspicious_patterns = ['free', 'win', 'discount', 'casino', 'prize']
    
    # Check if URL contains any malicious patterns
    status = 'safe'
    
    if any(pattern in url.lower() for pattern in malicious_patterns):
        status = 'malicious'
    elif any(pattern in url.lower() for pattern in suspicious_patterns) or (hash_int % 10 < 2):
        status = 'suspicious'
    
    # Generate mock categories
    categories = []
    if status == 'malicious':
        categories = random.sample(['phishing', 'malware', 'scam', 'spam'], k=random.randint(1, 3))
    elif status == 'suspicious':
        categories = random.sample(['suspicious', 'gambling', 'redirector', 'ads'], k=random.randint(1, 2))
    else:
        if hash_int % 5 == 0:
            categories = random.sample(['business', 'technology', 'news', 'shopping'], k=1)
    
    engines_total = 86
    engines_malicious = 0
    engines_suspicious = 0
    
    if status == 'malicious':
        engines_malicious = random.randint(5, 25)
    elif status == 'suspicious':
        engines_suspicious = random.randint(3, 10)
    
    return {
        'status': status,
        'detections': f"{engines_malicious + engines_suspicious} / {engines_total}",
        'engines': {
            'total': engines_total,
            'malicious': engines_malicious,
            'suspicious': engines_suspicious
        },
        'categories': categories,
        'scan_date': int(time.time()),
        'source': 'Mock Scanner (Demo)'
    }

def mock_port_scan(target, port_range_str):
    """Generate mock port scan results"""
    
    # Try to resolve hostname to IP - this is real functionality
    try:
        target_ip = socket.gethostbyname(target)
    except:
        # If resolution fails, generate a fake IP
        octets = [str(random.randint(1, 255)) for _ in range(4)]
        target_ip = ".".join(octets)
    
    # Parse the port range - simplified version
    ports = []
    parts = port_range_str.split(',')
    for part in parts:
        if '-' in part:
            start, end = map(int, part.split('-'))
            ports.extend(range(start, min(end + 1, 65536)))
        else:
            try:
                port = int(part.strip())
                if 1 <= port <= 65535:
                    ports.append(port)
            except:
                pass
    
    # Common ports that would typically be open
    common_open_ports = [22, 80, 443, 25, 21, 110, 143, 3389, 3306]
    
    # Generate mock open ports
    open_ports = []
    
    # Ensure consistent results for same target
    random.seed(target)
    
    # Decide which common ports are "open"
    for port in common_open_ports:
        if port in ports and random.random() < 0.6:  # 60% chance for common ports
            service = {
                22: "SSH",
                80: "HTTP",
                443: "HTTPS",
                25: "SMTP",
                21: "FTP",
                110: "POP3",
                143: "IMAP",
                3389: "RDP",
                3306: "MySQL"
            }.get(port, "Unknown")
            
            open_ports.append({
                'port': port,
                'service': service
            })
    
    # Add a few random ports
    other_ports = [p for p in ports if p not in common_open_ports]
    if other_ports and random.random() < 0.3:  # 30% chance to have additional open ports
        num_random = min(random.randint(1, 3), len(other_ports))
        for port in random.sample(other_ports, num_random):
            open_ports.append({
                'port': port,
                'service': 'Unknown'
            })
    
    # Sort by port number
    open_ports.sort(key=lambda x: x['port'])
    
    return {
        'status': 'completed',
        'target_ip': target_ip,
        'open_ports': open_ports,
        'total_ports_scanned': len(ports),
        'scan_date': int(time.time())
    }
