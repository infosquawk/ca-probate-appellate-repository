#!/usr/bin/env python3
"""
DNS Resolution Check for ProBRep.com
Quick diagnostic to check domain resolution
"""

import socket
import sys

def check_dns_resolution():
    hostnames_to_test = [
        'probrep.com',
        'ftp.probrep.com', 
        'www.probrep.com',
        'mail.probrep.com'
    ]
    
    print("ProBRep.com DNS Resolution Check")
    print("="*40)
    
    for hostname in hostnames_to_test:
        try:
            ip = socket.gethostbyname(hostname)
            print(f"✓ {hostname} → {ip}")
        except socket.gaierror as e:
            print(f"❌ {hostname} → DNS resolution failed")
    
    print("\n" + "="*40)
    print("If all fail: Domain may not be configured yet")
    print("If some work: Use working hostname for FTP")

if __name__ == "__main__":
    check_dns_resolution()
