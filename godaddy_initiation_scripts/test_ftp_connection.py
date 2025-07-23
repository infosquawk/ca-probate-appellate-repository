#!/usr/bin/env python3
"""
FTP Connection Test for ProBRep.com - UPDATED CREDENTIALS
Test GoDaddy FTP connection with new sysop2 account
"""

import ftplib
import configparser
from pathlib import Path

def test_ftp_connection():
    """Test FTP connection to ProBRep.com GoDaddy hosting"""
    
    print("=== ProBRep.com FTP Connection Test ===")
    
    # Load config or use updated settings
    config_path = Path("godaddy_config.ini")
    
    if config_path.exists():
        config = configparser.ConfigParser()
        config.read(config_path)
        
        if 'godaddy_ftp' in config:
            ftp_host = config['godaddy_ftp']['host']
            ftp_user = config['godaddy_ftp']['username']
            ftp_pass = config['godaddy_ftp']['password']
            ftp_port = int(config['godaddy_ftp']['port'])
            web_root = config['godaddy_ftp']['web_root']
        else:
            print("⚠ Config file found but missing [godaddy_ftp] section")
            return False
    else:
        # Use updated working settings
        print("📝 Using updated FTP settings (sysop2 account)")
        ftp_host = "probrep.com"
        ftp_user = "sysop2@probrep.com"  # UPDATED
        ftp_pass = "nq6FRcSQk8i5chh"     # UPDATED  
        ftp_port = 21
        web_root = "/public_html"
    
    try:
        print(f"Connecting to {ftp_host}:{ftp_port}...")
        
        # Connect to FTP server
        ftp = ftplib.FTP()
        ftp.connect(ftp_host, ftp_port, timeout=10)
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
        
        # Check directory structure
        if web_root != "/":
            try:
                ftp.cwd(web_root.lstrip('/'))
                print(f"✓ Successfully navigated to {web_root}")
                ftp.cwd('..')  # Return to original directory
            except ftplib.error_perm:
                print(f"⚠ Warning: Cannot access {web_root} directory")
                print("  Will deploy to root directory instead")
        
        # Test file upload capability
        print("\nTesting file upload capability...")
        test_content = f"ProBRep.com deployment test - {ftp_user} account"
        test_filename = "probrep_test_sysop2.txt"
        
        try:
            # Create test file
            from io import BytesIO
            test_file = BytesIO(test_content.encode('utf-8'))
            
            # Upload test file to appropriate directory
            if web_root != "/" and web_root != "":
                try:
                    ftp.cwd(web_root.lstrip('/'))
                    upload_path = test_filename
                except:
                    upload_path = test_filename
                    print("  Using root directory for upload")
            else:
                upload_path = test_filename
            
            ftp.storbinary(f'STOR {upload_path}', test_file)
            print(f"✓ Successfully uploaded test file: {upload_path}")
            
            # Verify file exists
            files = ftp.nlst()
            if test_filename in files:
                print(f"✓ Test file confirmed on server")
                
                # Get file size
                try:
                    size = ftp.size(test_filename)
                    print(f"✓ File size: {size} bytes")
                except:
                    print("✓ File exists (size check not supported)")
                
                # Delete test file
                ftp.delete(test_filename)
                print(f"✓ Successfully cleaned up test file")
            
        except Exception as e:
            print(f"⚠ File upload test failed: {e}")
            return False
        
        # Close connection
        ftp.quit()
        print("\n✅ FTP CONNECTION TEST PASSED!")
        print(f"✅ Hostname: {ftp_host}")
        print(f"✅ Username: {ftp_user}")
        print(f"✅ Directory: {web_root or 'Root'}")
        print(f"✅ Upload/Delete: Working")
        print("\n🚀 READY FOR DEPLOYMENT!")
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

if __name__ == "__main__":
    print("ProBRep.com GoDaddy FTP Setup - UPDATED CREDENTIALS")
    print("=" * 60)
    
    # Test FTP connection with updated credentials
    success = test_ftp_connection()
    
    if success:
        print("\n" + "=" * 60)
        print("🎯 MIGRATION READY!")
        print("Next steps:")
        print("1. Run manual deployment test")
        print("2. Update your pipeline scripts")
        print("3. Test full integration")
        print("4. Deploy to production")
    else:
        print("\n" + "=" * 60)
        print("❌ TROUBLESHOOTING REQUIRED")
        print("Fix FTP connection issues before proceeding")
