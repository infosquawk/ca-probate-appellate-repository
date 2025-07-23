#!/usr/bin/env python3
"""
FTP Connection Diagnostic Script
Tests different connection methods to troubleshoot FTP issues
"""

import socket
import ftplib
import json
from pathlib import Path

def test_ftp_connection():
    """Test FTP connection with various methods"""
    
    # Load config
    config_file = Path("../godaddy_config.json")
    if not config_file.exists():
        config_file = Path("godaddy_config.json")
    
    if not config_file.exists():
        print("ERROR: No config file found!")
        return
    
    with open(config_file, 'r') as f:
        config = json.load(f)
    
    host = config['ftp_host']
    username = config['ftp_username']
    password = config['ftp_password']
    
    print(f"Testing connection to: {host}")
    print(f"Username: {username}")
    print("="*50)
    
    # Test 1: Basic DNS resolution
    print("\n1. Testing DNS resolution...")
    try:
        ip = socket.gethostbyname(host)
        print(f"✓ DNS resolved: {host} -> {ip}")
    except Exception as e:
        print(f"✗ DNS resolution failed: {e}")
        
        # Try alternative hostnames
        alternative_hosts = [
            "probrep.com",
            "www.probrep.com", 
            "ftp.godaddy.com",
            host.replace("ftp.", "")
        ]
        
        print("\nTrying alternative hostnames...")
        for alt_host in alternative_hosts:
            try:
                ip = socket.gethostbyname(alt_host)
                print(f"✓ Alternative DNS: {alt_host} -> {ip}")
                # Update host for further testing
                host = alt_host
                break
            except:
                print(f"✗ Failed: {alt_host}")
        else:
            print("All DNS lookups failed - check network connection")
            return
    
    # Test 2: Basic socket connection
    print(f"\n2. Testing socket connection to {host}:21...")
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(10)
        result = sock.connect_ex((host, 21))
        sock.close()
        
        if result == 0:
            print("✓ Socket connection successful")
        else:
            print(f"✗ Socket connection failed: {result}")
    except Exception as e:
        print(f"✗ Socket connection error: {e}")
    
    # Test 3: FTP connection
    print(f"\n3. Testing FTP connection to {host}...")
    try:
        ftp = ftplib.FTP()
        ftp.set_debuglevel(1)  # Show FTP debug info
        ftp.connect(host, 21, timeout=30)
        print("✓ FTP connection established")
        
        # Test login
        print(f"\n4. Testing FTP login...")
        ftp.login(username, password)
        print("✓ FTP login successful")
        
        # Test directory listing
        print(f"\n5. Testing directory listing...")
        files = []
        ftp.retrlines('LIST', files.append)
        print(f"✓ Directory listing successful ({len(files)} items)")
        
        for file_info in files[:5]:  # Show first 5 files
            print(f"  {file_info}")
        
        ftp.quit()
        print("\n✓ ALL TESTS PASSED - FTP connection is working!")
        
    except Exception as e:
        print(f"✗ FTP connection/login failed: {e}")
        
        # Try alternative ports
        print(f"\nTrying alternative FTP configurations...")
        
        alternative_configs = [
            {"host": host, "port": 22, "desc": "SFTP port"},
            {"host": host.replace("ftp.", ""), "port": 21, "desc": "Without ftp prefix"},
            {"host": "probrep.com", "port": 21, "desc": "Direct domain"},
        ]
        
        for alt_config in alternative_configs:
            try:
                print(f"\nTrying {alt_config['desc']}: {alt_config['host']}:{alt_config['port']}")
                ftp = ftplib.FTP()
                ftp.connect(alt_config['host'], alt_config['port'], timeout=10)
                ftp.login(username, password)
                print(f"✓ SUCCESS with {alt_config['desc']}")
                ftp.quit()
                
                # Update config file with working settings
                config['ftp_host'] = alt_config['host']
                with open(config_file, 'w') as f:
                    json.dump(config, f, indent=4)
                print(f"✓ Updated config file with working hostname")
                break
                
            except Exception as alt_e:
                print(f"✗ Failed: {alt_e}")

if __name__ == "__main__":
    test_ftp_connection()
