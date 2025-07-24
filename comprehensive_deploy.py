#!/usr/bin/env python3
"""
Comprehensive ProBrep.com Deployment with Verification
"""

import ftplib
import json
import os
import time

def deploy_website():
    """Deploy the fixed website with comprehensive verification"""
    
    print("=" * 60)
    print("🚀 PROBREP.COM DEPLOYMENT WITH VERIFICATION")
    print("=" * 60)
    
    # Configuration
    config = {
        "ftp_host": "probrep.com",
        "ftp_username": "sysop2@probrep.com", 
        "ftp_password": "nq6FRcSQk8i5chh",
        "website_url": "https://probrep.com"
    }
    
    # Step 1: Verify local file
    print("📋 Step 1: Verifying local index.html...")
    
    if not os.path.exists('index.html'):
        print("❌ ERROR: index.html not found in current directory")
        return False
    
    # Read and check the file
    with open('index.html', 'r', encoding='utf-8') as f:
        content = f.read()
    
    file_size = len(content)
    print(f"✅ File found: {file_size:,} characters")
    
    # Check for episodes array
    if 'const episodes = [' in content:
        print("✅ Episodes array found")
    else:
        print("❌ ERROR: Episodes array not found")
        return False
    
    # Check for problematic descriptions
    if 'Here is a professional 2-3 sentence description suitable for podcast and website listings:' in content:
        print("❌ ERROR: Problematic descriptions still present")
        return False
    else:
        print("✅ No problematic descriptions found")
    
    # Step 2: FTP Connection
    print("\n📡 Step 2: Connecting to FTP server...")
    
    try:
        ftp = ftplib.FTP()
        ftp.set_debuglevel(0)  # Disable debug output
        print(f"  Connecting to: {config['ftp_host']}")
        ftp.connect(config['ftp_host'], 21)
        
        print(f"  Authenticating as: {config['ftp_username']}")
        ftp.login(config['ftp_username'], config['ftp_password'])
        
        print("✅ FTP connection successful")
        
    except Exception as e:
        print(f"❌ FTP connection failed: {e}")
        return False
    
    # Step 3: Upload file
    print("\n📤 Step 3: Uploading index.html...")
    
    try:
        # Check current directory
        try:
            current_dir = ftp.pwd()
            print(f"  Current FTP directory: {current_dir}")
        except:
            pass
        
        # Create backup of existing file
        try:
            ftp.rename('index.html', f'index_backup_{int(time.time())}.html')
            print("  Created backup of existing index.html")
        except:
            print("  No existing index.html to backup")
        
        # Upload new file
        print(f"  Uploading {file_size:,} bytes...")
        with open('index.html', 'rb') as f:
            result = ftp.storbinary('STOR index.html', f)
        
        print(f"  Upload result: {result}")
        print("✅ Upload completed successfully")
        
    except Exception as e:
        print(f"❌ Upload failed: {e}")
        ftp.quit()
        return False
    
    # Step 4: Verify upload
    print("\n🔍 Step 4: Verifying upload...")
    
    try:
        # Check file exists
        files = ftp.nlst()
        if 'index.html' in files:
            print("✅ index.html found on server")
            
            # Get file size
            try:
                ftp.voidcmd('TYPE I')  # Binary mode
                size = ftp.size('index.html')
                print(f"  Server file size: {size:,} bytes")
                print(f"  Local file size:  {file_size:,} bytes")
                
                if size == file_size:
                    print("✅ File sizes match")
                else:
                    print("⚠️  File sizes don't match - upload may be incomplete")
                    
            except:
                print("  Could not verify file size")
                
        else:
            print("❌ index.html not found on server after upload")
            ftp.quit()
            return False
            
    except Exception as e:
        print(f"⚠️  Verification error: {e}")
    
    # Close FTP connection
    ftp.quit()
    print("📡 FTP connection closed")
    
    # Step 5: Test website
    print("\n🌐 Step 5: Testing website...")
    
    try:
        import urllib.request
        
        print(f"  Testing: {config['website_url']}")
        
        # Add headers to bypass potential caching
        request = urllib.request.Request(
            config['website_url'],
            headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                'Cache-Control': 'no-cache',
                'Pragma': 'no-cache'
            }
        )
        
        response = urllib.request.urlopen(request, timeout=15)
        
        if response.getcode() == 200:
            print("✅ Website is accessible")
            
            # Check content
            page_content = response.read().decode('utf-8', errors='ignore')
            
            if len(page_content) > 10000:  # Should be substantial
                print(f"✅ Substantial content loaded ({len(page_content):,} characters)")
                
                # Check for key elements
                if 'const episodes = [' in page_content:
                    print("✅ Episodes array found in live website")
                else:
                    print("❌ Episodes array not found in live website")
                    
            else:
                print(f"⚠️  Limited content loaded ({len(page_content)} characters)")
        else:
            print(f"⚠️  Website returned status: {response.getcode()}")
            
    except Exception as e:
        print(f"⚠️  Website test failed: {e}")
    
    print("\n" + "=" * 60)
    print("🎉 DEPLOYMENT COMPLETED!")
    print("=" * 60)
    print(f"🌐 Website: {config['website_url']}")
    print("🔍 Check episodes are now displaying correctly")
    print("💡 If episodes still don't show, try:")
    print("   - Clear browser cache (Ctrl+F5)")
    print("   - Check browser console for JavaScript errors")
    print("   - Wait 2-3 minutes for CDN cache to update")
    
    return True

if __name__ == "__main__":
    success = deploy_website()
    exit(0 if success else 1)
