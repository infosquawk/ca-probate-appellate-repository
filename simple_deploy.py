import ftplib
import json

# FTP Configuration
config = {
    "ftp_host": "probrep.com",
    "ftp_username": "sysop2@probrep.com", 
    "ftp_password": "nq6FRcSQk8i5chh",
    "website_url": "https://probrep.com"
}

print("🚀 Deploying fixed website to ProBrep.com...")

try:
    # Connect to FTP
    print("📡 Connecting to FTP server...")
    ftp = ftplib.FTP()
    ftp.connect(config['ftp_host'], 21)
    ftp.login(config['ftp_username'], config['ftp_password'])
    print("✅ FTP connection successful!")
    
    # Navigate to public_html directory
    try:
        ftp.cwd('public_html')
        print("📁 Changed to public_html directory")
    except:
        print("⚠️ Using root directory")
    
    # Upload the fixed index.html
    print("📤 Uploading fixed index.html...")
    with open('index.html', 'rb') as f:
        ftp.storbinary('STOR index.html', f)
    
    print("✅ index.html uploaded successfully!")
    
    # Close FTP connection
    ftp.quit()
    
    print("🎉 Deployment completed successfully!")
    print("🌐 Test the website: https://probrep.com")
    print("🔍 Episodes should now display correctly")
    
except Exception as e:
    print(f"❌ Deployment failed: {e}")
    print("💡 Try running the script again or check FTP credentials")
