#!/usr/bin/env python3
"""
Server Upload Diagnostic Script
Check where files were uploaded and verify server structure
"""

import json
import ftplib
import os
from pathlib import Path

def check_server_files():
    """Check what files are on the server and where"""
    
    # Load config
    config_files = [
        Path("../godaddy_config.json"),
        Path("godaddy_config.json")
    ]
    
    config = None
    for config_file in config_files:
        if config_file.exists():
            with open(config_file, 'r') as f:
                config = json.load(f)
            print(f"✓ Loaded config from {config_file}")
            break
    
    if not config:
        print("ERROR: No godaddy_config.json found!")
        return
    
    try:
        # Connect to FTP
        ftp = ftplib.FTP()
        ftp.connect(config['ftp_host'], 21)
        ftp.login(config['ftp_username'], config['ftp_password'])
        print("✓ Connected to FTP server")
        
        # Check root directory
        print("\n=== ROOT DIRECTORY ===")
        ftp.cwd('/')
        files = []
        ftp.retrlines('LIST', files.append)
        for file_info in files:
            print(f"  {file_info}")
        
        # Check if public_html exists and what's in it
        try:
            print("\n=== PUBLIC_HTML DIRECTORY ===")
            ftp.cwd('/public_html')
            files = []
            ftp.retrlines('LIST', files.append)
            for file_info in files:
                print(f"  {file_info}")
                
            # Check if index.html exists in public_html
            file_names = [line.split()[-1] for line in files if line.split()]
            if 'index.html' in file_names:
                print("\n✓ index.html found in /public_html")
                
                # Try to download first few bytes to verify content
                try:
                    def check_content(data):
                        check_content.content = data
                    check_content.content = b''
                    
                    ftp.retrbinary('RETR index.html', check_content, blocksize=1024)
                    content_preview = check_content.content[:500].decode('utf-8', errors='ignore')
                    print(f"Content preview: {content_preview[:100]}...")
                    
                    if 'const episodes' in content_preview:
                        print("✓ index.html contains episodes data")
                    else:
                        print("✗ index.html does NOT contain episodes data")
                        
                except Exception as e:
                    print(f"Could not check content: {e}")
            else:
                print("\n✗ index.html NOT found in /public_html")
                
        except Exception as e:
            print(f"Cannot access /public_html: {e}")
            
            # Check if index.html is in root
            ftp.cwd('/')
            files = []
            ftp.retrlines('LIST', files.append)
            file_names = [line.split()[-1] for line in files if line.split()]
            if 'index.html' in file_names:
                print("\n✓ index.html found in ROOT directory")
                print("⚠ This might be the issue - it should be in /public_html")
            else:
                print("\n✗ index.html not found in root either")
        
        # Check for other common directories
        for dir_name in ['www', 'html', 'htdocs']:
            try:
                ftp.cwd(f'/{dir_name}')
                print(f"\n=== {dir_name.upper()} DIRECTORY ===")
                files = []
                ftp.retrlines('LIST', files.append)
                for file_info in files[:10]:  # First 10 files
                    print(f"  {file_info}")
            except:
                pass
        
        ftp.quit()
        
    except Exception as e:
        print(f"ERROR: {e}")

if __name__ == "__main__":
    check_server_files()
