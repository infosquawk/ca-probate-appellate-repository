#!/usr/bin/env python3
"""
Deploy fixed index.html to GoDaddy hosting
"""

import ftplib
import json

try:
    print("🚀 Deploying fixed version to probrep.com...")
    
    # Load config with correct key names
    with open('../godaddy_config.json', 'r') as f:
        config = json.load(f)
    
    print(f"✅ Loaded config for {config['ftp_host']}")
    
    # Check if fixed file exists
    try:
        with open('index_FIXED.html', 'r') as f:
            content = f.read()
            print(f"✅ Found index_FIXED.html ({len(content):,} bytes)")
    except FileNotFoundError:
        print("❌ index_FIXED.html not found!")
        print("Run: python website_fix.py first")
        exit(1)
    
    # Connect to FTP with correct key names
    ftp = ftplib.FTP()
    ftp.connect(config['ftp_host'], 21)           # ✅ ftp_host
    ftp.login(config['ftp_username'], config['ftp_password'])  # ✅ ftp_username, ftp_password
    
    print("✅ Connected to FTP server")
    
    # Upload the fixed file as index.html
    with open('index_FIXED.html', 'rb') as f:
        ftp.storbinary('STOR index.html', f)
    
    print("✅ Fixed version deployed to probrep.com!")
    print("🌐 Test at: https://probrep.com")
    print("⏱️ Wait 2-3 minutes for changes to propagate")
    print("🔍 Then press F12 and type 'episodes' to verify it works")
    
    ftp.quit()
    
except Exception as e:
    print(f"❌ Error: {e}")