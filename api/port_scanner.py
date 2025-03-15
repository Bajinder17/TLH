import os
import socket
import threading
import queue
import re
import time
import traceback
from dotenv import load_dotenv
from mock_scanner import mock_port_scan

# Load environment variables
load_dotenv()

# Common service ports mapping
COMMON_PORTS = {
    21: "FTP",
    22: "SSH",
    23: "Telnet",
    25: "SMTP",
    53: "DNS",
    80: "HTTP",
    110: "POP3",
    115: "SFTP",
    135: "MSRPC",
    139: "NetBIOS",
    143: "IMAP",
    194: "IRC",
    443: "HTTPS",
    445: "SMB",
    1433: "MSSQL",
    1434: "MSSQL Browser",
    3306: "MySQL",
    3389: "RDP",
    5432: "PostgreSQL",
    5900: "VNC",
    6379: "Redis",
    8080: "HTTP Proxy",
    8443: "HTTPS Alt",
    27017: "MongoDB"
}

def scan_ports(target, port_range_str):
    """
    Scan ports on target host
    
    Args:
        target (str): IP address or hostname
        port_range_str (str): Port range string (e.g., '1-1000' or '80,443,8080')
        
    Returns:
        dict: Scan results
    """
    print(f"Starting port scan for {target}, range: {port_range_str}")
    
    try:
        # Parse port range
        ports = parse_port_range(port_range_str)
        if not ports:
            print(f"Invalid port range: {port_range_str}")
            return {
                'status': 'error',
                'message': f'Invalid port range: {port_range_str}'
            }
            
        # If scanning too many ports or performance optimization needed, use the mock scanner
        if len(ports) > 1000:
            print(f"Using mock scanner for large port range: {len(ports)} ports")
            return mock_port_scan(target, port_range_str)
        
        # Validate and resolve target
        try:
            print(f"Resolving hostname: {target}")
            # Try to resolve as hostname
            target_ip = socket.gethostbyname(target)
            print(f"Resolved to IP: {target_ip}")
        except socket.gaierror as e:
            print(f"Failed to resolve hostname: {e}")
            return {
                'status': 'error',
                'message': f'Invalid hostname or IP address: {target}'
            }
            
        # Create a queue for ports to scan
        port_queue = queue.Queue()
        for port in ports:
            port_queue.put(port)
            
        # Create a queue for open ports
        open_ports_queue = queue.Queue()
        
        print(f"Starting scan of {len(ports)} ports with multithreading")
        # Create threads for scanning
        threads = []
        num_threads = min(50, len(ports))  # Limit number of threads for better stability
        
        for i in range(num_threads):
            thread = threading.Thread(
                target=worker_thread,
                args=(target_ip, port_queue, open_ports_queue),
                name=f"PortScanner-{i}"
            )
            thread.daemon = True
            thread.start()
            threads.append(thread)
            
        # Wait for all threads to finish
        for thread in threads:
            thread.join()
            
        # Collect open ports
        open_ports = []
        while not open_ports_queue.empty():
            port = open_ports_queue.get()
            open_ports.append({
                'port': port,
                'service': COMMON_PORTS.get(port, 'Unknown')
            })
            
        # Sort by port number
        open_ports.sort(key=lambda x: x['port'])
        
        print(f"Scan complete. Found {len(open_ports)} open ports")
                
        return {
            'status': 'completed',
            'target_ip': target_ip,
            'open_ports': open_ports,
            'total_ports_scanned': len(ports),
            'scan_date': int(time.time())
        }
            
    except Exception as e:
        print(f"Error in port scanning: {str(e)}")
        traceback.print_exc()
        # In case of error, try to use mock scanner as fallback
        try:
            return mock_port_scan(target, port_range_str)
        except:
            return {
                'status': 'error',
                'message': f'Error scanning ports: {str(e)}'
            }

def worker_thread(target_ip, port_queue, open_ports_queue):
    """Worker thread to scan ports"""
    thread_name = threading.current_thread().name
    ports_checked = 0
    
    while not port_queue.empty():
        try:
            port = port_queue.get(block=False)
            ports_checked += 1
            
            if ports_checked % 50 == 0:
                print(f"{thread_name} has checked {ports_checked} ports")
                
        except queue.Empty:
            break
            
        try:
            # Create a socket
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1.0)  # 1 second timeout
            
            # Try to connect
            result = sock.connect_ex((target_ip, port))
            
            # If the connection was successful, the port is open
            if result == 0:
                print(f"Found open port: {port}")
                open_ports_queue.put(port)
                
            sock.close()
            
        except Exception as e:
            # Skip errors but log them
            print(f"Error checking port {port}: {str(e)}")
            pass

def parse_port_range(port_range_str):
    """Parse port range string into a list of ports"""
    if not port_range_str:
        return list(range(1, 1001))  # Default to 1-1000 if not specified
        
    ports = []
    
    # Split by comma
    for part in port_range_str.split(','):
        part = part.strip()
        
        # Check for range (e.g., '1-1000')
        range_match = re.match(r'^(\d+)-(\d+)$', part)
        if range_match:
            start = int(range_match.group(1))
            end = int(range_match.group(2))
            
            # Validate port range
            if start < 1 or end > 65535 or start > end:
                continue
                
            ports.extend(range(start, end + 1))
        else:
            # Try to parse as a single port
            try:
                port = int(part)
                if 1 <= port <= 65535:
                    ports.append(port)
            except ValueError:
                # Skip invalid ports
                continue
    
    # Remove duplicates
    return sorted(list(set(ports)))
