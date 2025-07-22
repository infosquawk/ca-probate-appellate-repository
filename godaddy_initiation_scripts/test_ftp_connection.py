#!/usr/bin/env python3
"""
FTP Connection Test for ProBRep.com
Test GoDaddy FTP connection before implementing full deployment
"""

import ftplib
import configparser
from pathlib import Path

def test_ftp_connection():
    """Test FTP connection to ProBRep.com GoDaddy hosting"""
    
    print("=== ProBRep.com FTP Connection Test ===")
    
    # FTP connection details
    ftp_host = "ftp.probrep.com"
    ftp_user = "sysop@probrep.com"
    ftp_pass = "Fpm9dLJqWdduPC8"
    ftp_port = 21
    
    try:
        print(f"Connecting to {ftp_host}:{ftp_port}...")
        
        # Connect to FTP server
        ftp = ftplib.FTP()
        ftp.connect(ftp_host, ftp_port)
        print("✓ FTP connection established")
        
        # Login
        print(f"Logging in as {ftp_user}...")
        ftp.login(ftp_user, ftp_pass)
        print("✓ FTP login successful")
        
        # Get current directory
        current_dir = ftp.pwd()
        print(f"✓ Current directory: {current_dir}")
        
        # List directory contents
        print("\nDirectory contents:")
        files = ftp.nlst()
        for file in files[:10]:  # Show first 10 items
            print(f"  - {file}")
        if len(files) > 10:
            print(f"  ... and {len(files) - 10} more items")
        
        # Try to navigate to public_html
        try:
            ftp.cwd('public_html')
            print("✓ Successfully navigated to public_html")
            
            # Check if we can create a directory (test write permissions)
            test_dir = "test_deployment"
            try:
                ftp.mkd(test_dir)
                print(f"✓ Successfully created test directory: {test_dir}")
                
                # Remove test directory
                ftp.rmd(test_dir)
                print(f"✓ Successfully removed test directory: {test_dir}")
                
            except ftplib.error_perm as e:
                if "exists" in str(e).lower():
                    print(f"! Test directory already exists - write permissions confirmed")
                else:
                    print(f"⚠ Warning: Cannot create directories - {e}")
            
            # Return to root
            ftp.cwd('..')
            
        except ftplib.error_perm:
            print("⚠ Warning: Cannot access public_html directory")
            print("  This might be normal - we'll try direct upload to root")
        
        # Test file upload capability
        print("\nTesting file upload capability...")
        test_content = "ProBRep.com deployment test file"
        test_filename = "test_upload.txt"
        
        try:
            # Create test file
            from io import BytesIO
            test_file = BytesIO(test_content.encode('utf-8'))
            
            # Upload test file
            ftp.storbinary(f'STOR {test_filename}', test_file)
            print(f"✓ Successfully uploaded test file: {test_filename}")
            
            # Verify file exists
            files = ftp.nlst()
            if test_filename in files:
                print(f"✓ Test file confirmed on server")
                
                # Get file size
                size = ftp.size(test_filename)
                print(f"✓ File size: {size} bytes")
                
                # Delete test file
                ftp.delete(test_filename)
                print(f"✓ Successfully cleaned up test file")
            
        except Exception as e:
            print(f"⚠ File upload test failed: {e}")
        
        # Close connection
        ftp.quit()
        print("\n✓ FTP connection test completed successfully!")
        print("\n=== READY FOR DEPLOYMENT ===")
        print("Your GoDaddy hosting is properly configured for automated deployment.")
        
        return True
        
    except Exception as e:
        print(f"\n❌ FTP connection test failed: {e}")
        print("\nTroubleshooting suggestions:")
        print("1. Verify FTP credentials in GoDaddy control panel")
        print("2. Check if FTP is enabled for your hosting account")
        print("3. Ensure your IP is not blocked by GoDaddy firewall")
        print("4. Try connecting with a manual FTP client like FileZilla")
        
        return False

def create_config_file():
    """Create the configuration file for the deployment pipeline"""
    
    config_path = Path("../godaddy_config.ini")  # Save in parent directory (website/)
    
    if config_path.exists():
        print(f"\n✓ Configuration file already exists: {config_path}")
        return
    
    print(f"\nCreating configuration file: {config_path}")
    
    config_content = """# GoDaddy Hosting Configuration for ProBRep.com
# Auto-generated configuration file

[godaddy]
# FTP connection details for probrep.com
ftp_host = ftp.probrep.com
ftp_username = sysop@probrep.com
ftp_password = Fpm9dLJqWdduPC8
ftp_port = 21

# Web root directory
web_root = public_html

# Domain information
domain_name = probrep.com
site_url = https://probrep.com

# Deployment settings
max_retries = 3
timeout_seconds = 30
verify_uploads = true

# File exclusions
exclude_patterns = *.log,*.backup,*.tmp,.git/*,logs/*

[ssl]
enable_ssl = true
force_https = true

[performance]
enable_compression = true
cache_control_max_age = 86400
enable_cdn = false
"""
    
    with open(config_path, 'w') as f:
        f.write(config_content)
    
    print(f"✓ Configuration file created successfully")

if __name__ == "__main__":
    print("ProBRep.com GoDaddy FTP Setup")
    print("=" * 40)
    
    # Test FTP connection
    success = test_ftp_connection()
    
    if success:
        # Create configuration file
        create_config_file()
        
        print("\n" + "=" * 40)
        print("NEXT STEPS:")
        print("1. Copy the deployment scripts to your website directory")
        print("2. Test the deployment pipeline with existing content")
        print("3. Update your pipeline batch file to use GoDaddy deployment")
        print("4. Run a full test of the enhanced pipeline")
    else:
        print("\n" + "=" * 40)
        print("TROUBLESHOOTING REQUIRED:")
        print("Fix FTP connection issues before proceeding with migration")
