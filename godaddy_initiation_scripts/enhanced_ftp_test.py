#!/usr/bin/env python3
"""
Enhanced FTP Connection Test for GoDaddy - UPDATED CREDENTIALS
Tests multiple common hostname formats with sysop2 account
"""

import ftplib
import configparser
import socket
from pathlib import Path

def test_multiple_ftp_hosts():
    """Test FTP connection with multiple hostname formats"""
    
    # Updated FTP credentials
    username = "sysop2@probrep.com"  # UPDATED
    password = "nq6FRcSQk8i5chh"     # UPDATED
    
    # Common GoDaddy hostname formats to try
    hostnames_to_test = [
        "probrep.com",           # This worked before
        "ftp.probrep.com",
        "www.probrep.com",
        "ftp.secureserver.net",  # Common GoDaddy FTP server
        "secureserver.net"
    ]
    
    print("Enhanced GoDaddy FTP Connection Test - UPDATED CREDENTIALS")
    print("="*65)
    print(f"Username: {username}")
    print(f"Testing {len(hostnames_to_test)} hostname formats...")
    print()
    
    successful_host = None
    
    for hostname in hostnames_to_test:
        print(f"Testing: {hostname}")
        try:
            # Test DNS resolution first
            ip = socket.gethostbyname(hostname)
            print(f"  ✓ DNS: {hostname} → {ip}")
            
            # Test FTP connection
            ftp = ftplib.FTP()
            ftp.connect(hostname, 21, timeout=10)
            ftp.login(username, password)
            
            # Test basic operations
            current_dir = ftp.pwd()
            file_list = ftp.nlst()
            
            print(f"  ✓ FTP: Connected successfully!")
            print(f"  ✓ Current directory: {current_dir}")
            print(f"  ✓ Files found: {len(file_list)}")
            
            # Check if public_html exists
            try:
                ftp.cwd('public_html')
                print(f"  ✓ public_html directory found")
                ftp.cwd('..')  # Go back
            except ftplib.error_perm:
                print(f"  ⚠ public_html directory not found - using root")
            
            # Test file upload
            test_content = f"FTP test with {username}"
            test_filename = f"test_{username.split('@')[0]}.txt"
            try:
                from io import BytesIO
                test_file = BytesIO(test_content.encode('utf-8'))
                ftp.storbinary(f'STOR {test_filename}', test_file)
                print(f"  ✓ Upload test successful")
                
                # Clean up
                ftp.delete(test_filename)
                print(f"  ✓ Cleanup successful")
            except Exception as e:
                print(f"  ⚠ Upload test failed: {e}")
            
            ftp.quit()
            successful_host = hostname
            print(f"  🎯 SUCCESS: Use '{hostname}' as FTP host")
            break
            
        except socket.gaierror:
            print(f"  ❌ DNS: Cannot resolve {hostname}")
        except ftplib.error_perm as e:
            print(f"  ❌ FTP Auth: {e}")
        except Exception as e:
            print(f"  ❌ FTP Error: {e}")
        
        print()
    
    print("="*65)
    if successful_host:
        print(f"✅ SOLUTION FOUND!")
        print(f"Use hostname: {successful_host}")
        print(f"Account: {username}")
        print()
        print("Next steps:")
        print("1. Updated configuration saved")
        print("2. Run test_ftp_connection.py to verify")
        print("3. Run manual_deployment_test.py to test website")
        
        # Update config automatically
        update_config_with_working_host(successful_host)
        
    else:
        print("❌ NO WORKING FTP HOST FOUND")
        print()
        print("Possible issues:")
        print("1. New FTP account not activated yet")
        print("2. Incorrect password for sysop2 account") 
        print("3. FTP access disabled for the account")
        print("4. GoDaddy hosting not fully provisioned")
        print()
        print("Manual check required:")
        print("1. Login to GoDaddy control panel")
        print("2. Go to Web Hosting → Manage")
        print("3. Verify sysop2@probrep.com account exists")
        print("4. Check FTP settings and permissions")

def update_config_with_working_host(hostname):
    """Update config file with working hostname and new credentials"""
    config_path = Path("godaddy_config.ini")
    
    if config_path.exists():
        config = configparser.ConfigParser()
        config.read(config_path)
        
        # Update both sections
        for section in ['godaddy_ftp', 'godaddy']:
            if section in config:
                config[section]['host'] = hostname
                config[section]['ftp_host'] = hostname
                config[section]['username'] = 'sysop2@probrep.com'
                config[section]['ftp_username'] = 'sysop2@probrep.com'
                config[section]['password'] = 'nq6FRcSQk8i5chh'
                config[section]['ftp_password'] = 'nq6FRcSQk8i5chh'
        
        with open(config_path, 'w') as f:
            config.write(f)
        
        print(f"📝 Updated godaddy_config.ini with:")
        print(f"   Hostname: {hostname}")
        print(f"   Account: sysop2@probrep.com")

if __name__ == "__main__":
    test_multiple_ftp_hosts()
