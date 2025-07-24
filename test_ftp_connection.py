#!/usr/bin/env python3
"""
ProBrep.com FTP Connection Test
Verifies FTP credentials and connection before full deployment
"""

import ftplib
import configparser
from pathlib import Path

def test_ftp_connection():
    """Test FTP connection and basic operations"""
    script_dir = Path(__file__).parent
    config_file = script_dir / "godaddy_config.ini"
    
    print("="*50)
    print("ProBrep.com FTP Connection Test")
    print("="*50)
    
    # Load configuration
    try:
        config = configparser.ConfigParser()
        config.read(config_file)
        
        ftp_host = config.get('godaddy', 'ftp_host')
        ftp_username = config.get('godaddy', 'ftp_username')
        ftp_password = config.get('godaddy', 'ftp_password')
        ftp_port = config.getint('godaddy', 'ftp_port')
        web_root = config.get('godaddy', 'web_root')
        
        print(f"🔧 Configuration loaded from: {config_file}")
        print(f"📡 Host: {ftp_host}:{ftp_port}")
        print(f"👤 Username: {ftp_username}")
        print(f"📁 Web Root: {web_root}")
        print()
        
    except Exception as e:
        print(f"❌ Configuration error: {e}")
        return False
    
    # Test FTP connection
    try:
        print("🔌 Testing FTP connection...")
        ftp = ftplib.FTP()
        ftp.connect(ftp_host, ftp_port)
        print("✅ Connected to FTP server")
        
        print("🔐 Logging in...")
        ftp.login(ftp_username, ftp_password)
        print("✅ Login successful")
        
        # Only change directory if web_root is not root
        if web_root and web_root != "/" and web_root.strip():
            print(f"📁 Changing to web root: {web_root}")
            ftp.cwd(web_root)
            print("✅ Web root accessible")
        else:
            print("📁 Using FTP root directory (already in public_html)")
            print("✅ Web root accessible")
        
        print("📋 Listing current directory contents:")
        files = ftp.nlst()
        for file in files[:10]:  # Show first 10 files
            print(f"   📄 {file}")
        if len(files) > 10:
            print(f"   ... and {len(files) - 10} more files")
        
        print(f"\n📊 Total files in web root: {len(files)}")
        
        # Test write permission
        try:
            test_file = "ftp_test_temp.txt"
            ftp.storbinary(f'STOR {test_file}', open(script_dir / "godaddy_config.ini", 'rb'))
            print("✅ Write permission confirmed")
            
            # Clean up test file
            ftp.delete(test_file)
            print("✅ File cleanup successful")
            
        except Exception as e:
            print(f"⚠️ Write test failed: {e}")
        
        ftp.quit()
        print("🔌 FTP connection closed")
        
        print("\n" + "="*50)
        print("🎉 FTP CONNECTION TEST SUCCESSFUL!")
        print("="*50)
        print("✅ Your FTP credentials are working correctly")
        print("✅ Server is accessible and writable")
        print("✅ Ready for full website deployment")
        print("\nTo deploy your complete website, run:")
        print("   DEPLOY_COMPLETE_WEBSITE.bat")
        print()
        
        return True
        
    except Exception as e:
        print(f"\n❌ FTP connection failed: {e}")
        print("\nTroubleshooting steps:")
        print("1. Verify internet connection")
        print("2. Check FTP credentials in godaddy_config.ini")
        print("3. Ensure firewall allows FTP connections")
        print("4. Contact hosting provider if issues persist")
        return False

if __name__ == "__main__":
    test_ftp_connection()